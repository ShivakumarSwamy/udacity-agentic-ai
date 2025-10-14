import json
from typing import List, Literal, Optional

import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic.v1 import Field

from app.util import openai_client, get_completion_v2

load_dotenv()
client = openai_client()

# First Notion of Loss - FONL
sample_fnols = [
    """
    Claim ID: C001
    Customer: John Smith
    Vehicle: 2018 Toyota Camry
    Incident: While driving on the highway, a rock hit my windshield and caused a small chip
    about the size of a quarter. No other damage was observed.
    """,
    """
    Claim ID: C002
    Customer: Sarah Johnson
    Vehicle: 2020 Honda Civic
    Incident: I was parked at the grocery store and returned to find someone had hit my car and
    dented the rear bumper and taillight. The taillight is broken and the bumper has a large dent.
    """,
    """
    Claim ID: C003
    Customer: Michael Rodriguez
    Vehicle: 2022 Ford F-150
    Incident: I was involved in a serious collision at an intersection. The front of my truck is
    severely damaged, including the hood, bumper, radiator, and engine compartment. The airbags
    deployed and the vehicle is not drivable.
    """,
    """
    Claim ID: C004
    Customer: Emma Williams
    Vehicle: 2019 Subaru Outback
    Incident: My car was damaged in a hailstorm. There are multiple dents on the hood, roof, and
    trunk. The side mirrors were also damaged and one window has a small crack.
    """,
    """
    Claim ID: C005
    Customer: David Brown
    Vehicle: 2021 Tesla Model 3
    Incident: Someone keyed my car in the parking lot. There are deep scratches along both doors
    on the driver's side.
    """
]


class ClaimInformation(BaseModel):
    claim_id: str = Field(..., min_length=2, max_length=10)
    name: str = Field(..., min_length=2, max_length=100)
    vehicle: str = Field(..., min_length=2, max_length=100)
    loss_desc: str = Field(..., min_length=10, max_length=500)
    damage_area: List[
        Literal[
            "windshield",
            "front",
            "rear",
            "side",
            "roof",
            "hood",
            "door",
            "bumper",
            "fender",
            "quarter panel",
            "trunk",
            "glass",
        ]
    ] = Field(..., min_items=1)


class SeverityAssessment(BaseModel):
    severity: Literal["Minor", "Moderate", "Major"]
    est_cost: float = Field(..., gt=0)


class ClaimRouting(BaseModel):
    claim_id: str
    queue: Literal["glass", "fast_track", "material_damage", "total_loss"]


def gate1_validate_claim_info(claim_info_json: str) -> ClaimInformation:
    """
    Gate 1: Validates claim information extracted from FNOL text.
    Returns validated ClaimInformation object or raises validation error.
    """
    try:
        # Parse the JSON string
        claim_info_dict = json.loads(claim_info_json)
        # Validate with Pydantic model
        validated_info = ClaimInformation(**claim_info_dict)
        return validated_info
    except Exception as e:
        raise ValueError(f"Gate 1 validation failed: {str(e)}")


def extract_claim_info(fnol_text, system_prompt):
    """
    Stage 1: Extract structured information from FNOL text
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": fnol_text},
    ]

    response = get_completion_v2(client, messages)

    # Gate check: validate the extracted information
    try:
        validated_info = gate1_validate_claim_info(response)
        return validated_info
    except ValueError as e:
        print(f"Gate 1 failed: {e}")
        return None


def gate2_cost_range_ok(severity_json: str) -> SeverityAssessment:
    """
    Gate 2: Validates that the estimated cost is within reasonable range for the severity.
    Returns validated SeverityAssessment object or raises validation error.
    """
    try:
        # Parse the JSON string
        severity_dict = json.loads(severity_json)
        # Validate with Pydantic model
        validated_severity = SeverityAssessment(**severity_dict)

        # Check cost range based on severity
        if (
                validated_severity.severity == "Minor"
                and (validated_severity.est_cost < 100 or validated_severity.est_cost > 1000
                # ********** <-- est_cost outside of heuristic range for Minor will raise ValueError
        )
        ):
            raise ValueError(
                f"Minor damage should cost between $100-$1000, got ${validated_severity.est_cost}"
            )
        elif (
                validated_severity.severity == "Moderate"
                and (validated_severity.est_cost < 1000 or validated_severity.est_cost > 5000
                        # ********** <-- est_cost outside of heuristic range for Moderate will raise ValueError
                )
        ):
            raise ValueError(
                f"Moderate damage should cost between $1000-$5000, got ${validated_severity.est_cost}"
            )
        elif (
                validated_severity.severity == "Major"
                and (validated_severity.est_cost < 5000 or validated_severity.est_cost > 50000
                        # ********** <-- est_cost outside of heuristic range for Major will raise ValueError
                )
        ):
            raise ValueError(
                f"Major damage should cost between $5000-$50000, got ${validated_severity.est_cost}"
            )

        return validated_severity
    except Exception as e:
        raise ValueError(f"Gate 2 validation failed: {str(e)}")


def assess_severity(claim_info: ClaimInformation, system_prompt) -> Optional[SeverityAssessment]:
    """
    Stage 2: Assess severity based on damage description
    """

    # Convert Pydantic model to JSON string
    claim_info_json = claim_info.model_dump_json()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": claim_info_json},
    ]

    response = get_completion_v2(client, messages)

    # Gate check: validate the severity assessment
    try:
        validated_severity = gate2_cost_range_ok(response)
        return validated_severity
    except ValueError as e:
        print(f"Gate 2 failed: {e}. Response: {response}: Claim: {claim_info_json}")
        return None


def gate3_validate_routing(routing_json: str) -> ClaimRouting:
    """
    Gate 3: Validates that the claim is routed to a valid queue.
    Returns validated ClaimRouting object or raises validation error.
    """
    try:
        # Parse the JSON string
        routing_dict = json.loads(routing_json)
        # Validate with Pydantic model
        validated_routing = ClaimRouting(**routing_dict)
        return validated_routing
    except Exception as e:
        raise ValueError(f"Gate 3 validation failed: {str(e)}")


def route_claim(
        claim_info: ClaimInformation, severity_assessment: Optional[SeverityAssessment], system_prompt
) -> Optional[ClaimRouting]:
    """
    Stage 3: Route claim to appropriate queue
    """
    if severity_assessment is None:
        return None

    # Create input for the routing model
    routing_input = claim_info.model_dump() | severity_assessment.model_dump()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(routing_input)},
    ]

    response = get_completion_v2(client, messages)

    # Gate check: validate the routing decision
    try:
        validated_routing = gate3_validate_routing(response)
        return validated_routing
    except ValueError as e:
        print(f"Gate 3 failed: {e}. Response: {response}")
        return None


def main():
    info_extraction_system_prompt = """
You are Insurance Claim Triage Specialist. Your task is to extract key information from First Notice of Loss (FNOL) reports.

Format your response as a valid JSON object with the following keys:
- claim_id (str): The claim ID. 
- name (str): Customer Name 
- vehicle (str): Vehicle to be claimed
- loss_desc (str): Incident description
- damage_area (array of string): Parts of vehicle area damage.

Instructions of determining damage_area field:
- Analyse the Incident description in-order to determine which parts of the vehicle are damaged.
- Allowed values of field are "windshield", "front", "rear", "side", "roof", "hood", "door", "bumper", "fender", "quarter panel", "trunk", "glass"
- Make sure at least one part of the car is present from allowed values.

Only respond with the JSON object, nothing else.
    """

    extracted_claim_info_items = [
        extract_claim_info(fnol_text, info_extraction_system_prompt) for fnol_text in sample_fnols
    ]
    print(extracted_claim_info_items)

    severity_assessment_system_prompt = """
You are an auto insurance damage assessor. Your task is to evaluate the severity of vehicle damage and estimate repair costs.

Format your response as a valid JSON object with the following keys:
- severity (str): severity of vehicle damage 
- est_cost (float): estimate repair costs 

Instructions of determining severity field:
- Use damage_area and loss_desc fields to analyse the severity of vehicle damage.
- Minor damage: Small dents, scratches, glass chips
- Moderate damage: Single panel damage, bumper replacement, door damage
- Major damage: Structural damage, multiple panel replacement, engine/drivetrain issues, total loss candidates 
- Post analysis and assessment, classify either "Minor" or "Moderate" or "Major".


Instructions of determining est_cost field:
- Based on the values of damage_area field estimate the cost. 
- If severity is "Minor", ensure est_cost is in cost range $100-$1,000.
- If severity is "Moderate", ensure est_cost is in cost range $1,000-$5,000.
- If severity is "Major", ensure est_cost is in cost range $5,000-$50,000.

Order of analysis:
- Analyse severity field first, then analyse est_cost field.

Only respond with the JSON object, nothing else.
    """

    severity_assessment_items = [
        assess_severity(item, severity_assessment_system_prompt) for item in extracted_claim_info_items
    ]

    print(severity_assessment_items)

    queue_routing_system_prompt = """
You are an auto insurance claim routing specialist. Your task is to determine the appropriate processing queue for each claim.

Format your response as a valid JSON object with the following keys:
- claim_id (str): The claim ID. 
- queue (str): claim processing queue  

Instructions of determining queue field:
- 'glass' queue: For Minor damage involving ONLY glass (windshield, windows)
- 'fast_track' queue: For other Minor damage
- 'material_damage' queue: For all Moderate damage
- 'total_loss' queue: For all Major damage
- Use severity field, to understand severity classification as Major or Minor or Moderate
- When, Minor severity use damage_area and loss_desc fields to analyse whether to route to "glass" or "fast_track" queue.
 

Only respond with the JSON object, nothing else.
    """

    routed_claim_items = [
        route_claim(claim, severity_assessment, queue_routing_system_prompt) for claim, severity_assessment in
        zip(extracted_claim_info_items, severity_assessment_items)
    ]

    print(routed_claim_items)

    records = []
    for claim, severity_assessment, routed_claim in zip(
            extracted_claim_info_items, severity_assessment_items, routed_claim_items
    ):
        record = {}
        record.update(claim)
        record.update(severity_assessment)
        record.update(routed_claim)
        records.append(record)

    # Show the entire dataframe since it is not too large
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)
    df = pd.DataFrame(records)
    print(df)


if __name__ == '__main__':
    main()

from dotenv import load_dotenv

from app.util import get_completion, openai_client, display_responses

load_dotenv()


def main():
    system_prompt_cot = """
    You are a diagnostic physician. Think step by step, correlating the symptoms with the provided patient date to form 
    a differential diagnosis. Explain your reasoning.
    """

    user_prompt_with_data = """
    A patient presents with a persistent cough and fatigue.
    
    Here is their patient chart:
    - Age: 45
    - History: Non-smoker, works indoors as an accountant. No recent travel.
    - Lab Results: White blood cell count is slightly elevated.
    - Vitals: Temperature is normal.
    
    Based on all this information, what is the likely diagnosis? 
    """

    client = openai_client()

    response = get_completion(client, system_prompt_cot, user_prompt_with_data)
    display_responses(
        {
            "system_prompt": system_prompt_cot,
            "user_prompt": user_prompt_with_data,
            "response": response,
        }
    )


if __name__ == '__main__':
    main()

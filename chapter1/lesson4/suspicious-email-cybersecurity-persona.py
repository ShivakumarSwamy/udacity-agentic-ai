from dotenv import load_dotenv

from app.util import get_completion, display_responses, MODEL, openai_client

load_dotenv()


def main():
    client = openai_client()

    suspicious_email_text = """
    From: SecureBank Support <support-update@secure-bank-net.com>
    Subject: Urgent: Your Account Requires Immediate Verification
    
    Dear Valued Customer,
    We have detected unusual activity on your account. For your security, you must verify your identity immediately 
    by clicking here: http://secure-bank-net.com/verify-now
    Failure to do so within 24 hours will result in account suspension.
    Thank you,
    SecureBank Team
    """

    plain_system_prompt = """
    You are a senior Cybersecurity Analyst providing a formal threat assessment. 
    Your tone is objective, cautious, and precise.
    
    When analyzing a potential phishing email, do the following:
    1.  State your overall assessment clearly (e.g., "High-Confidence Phishing Attempt").
    2.  Do not speculate or use casual language.
    3.  List the specific red flags you've identified as a bulleted list. For each flag, provide a brief explanation.
    4.  Conclude with a clear, actionable recommendation for the end-user.
    """

    user_prompt = f"""
        Please analyze the following email and tell me if it's safe:
        ---
        {suspicious_email_text}
        ---
    """

    print(f"Sending prompt to {MODEL} model...")
    baseline_response = get_completion(client, plain_system_prompt, user_prompt)
    print("Response received!\n")

    display_responses(
        {
            "system_prompt": plain_system_prompt,
            "user_prompt": user_prompt,
            "response": baseline_response,
        }
    )


if __name__ == '__main__':
    main()

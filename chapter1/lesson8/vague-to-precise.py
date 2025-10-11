from dotenv import load_dotenv

from app.util import openai_client, get_completion, print_in_box_all_prompts_and_response

load_dotenv()


def main():
    client = openai_client()

    customer_email = """
Hi, I'm writing because I was charged twice for my last order (Order #8675309).
I thought my subscription was paused. Can you please look into this and reverse the extra charge?
Thanks,
Alex    
    """

    system_prompt = """
You are a helpful assistant.
    """

    user_prompt = f"""
Please categorize the following email:\n\n{customer_email}
    """

    # response = get_completion(client, system_prompt, user_prompt)
    #
    # print_in_box_all_prompts_and_response(system_prompt, user_prompt, response)

    system_prompt = """
You are an expert customer support agent responsible for categorizing incoming emails for a ticketing system.

Your task is to analyze the user's email and provide a structured JSON output.

## Email Categories:
- **Billing:** For issues related to charges, subscriptions, or refunds.
- **Technical Support:** For problems with product functionality or bugs.
- **General Inquiry:** For questions that do not fit the other categories.

## Output Format:
You must respond with a single JSON object containing the following keys:
- `category`: (string) One of "Billing", "Technical Support", or "General Inquiry".
- `summary`: (string) A one-sentence summary of the user's issue.
- `urgency`: (string) "High", "Medium", or "Low".
- `customer_id`: (string) Extract the order number or customer ID if available, otherwise "N/A".    
    """

    response = get_completion(client, system_prompt, user_prompt)
    print_in_box_all_prompts_and_response(system_prompt, user_prompt, response)


if __name__ == '__main__':
    main()

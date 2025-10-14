import ast

from dotenv import load_dotenv

from app.util import openai_client, get_completion, print_in_box_all_prompts_and_response

load_dotenv()


def check_python_syntax(code):
    try:
        ast.parse(code)
        return True, "No syntax errors found."
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"


def main():
    client = openai_client()

    # Step 1: Generate the Outline
    user_prompt = """
You are a helpful programming assistant.

I need a Python script to read a CSV file named 'input_data.csv',
calculate the average of a column named 'value', and write the
average to a new file named 'output.txt'.

Please provide a simple, step-by-step outline for this script.
    """

    response = get_completion(client, None, user_prompt)
    print_in_box_all_prompts_and_response("N/A", user_prompt, response)

    # Step 2: Generate the Code from the Outline
    user_prompt = f"""
You are a helpful programming assistant.

Based on the following outline, please write the complete Python code for the script.
Ensure you use standard libraries and include comments.

Outline:
---
{response}
---

Output only python script in plain text.
    """

    response = get_completion(client, None, user_prompt)
    print_in_box_all_prompts_and_response("N/A", user_prompt, response)

    # Step 3: The "Gate Check"
    is_valid, message = check_python_syntax(response)
    print(f"\n--- Gate Check Result ---")
    print(f"Code is valid: {is_valid}")
    print(message)


if __name__ == '__main__':
    main()

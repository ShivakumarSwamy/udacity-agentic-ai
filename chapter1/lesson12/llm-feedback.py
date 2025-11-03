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

    # Attempt 1: The Initial (Flawed) Generation
    prompt_initial = """
You are a web developer. Generate the HTML and CSS for a user profile card.
It should have:
- A container with a light grey background and a subtle shadow.
- An avatar image placeholder.
- The user's name and title below the avatar.
    """

    prompt_initial_response = get_completion(client, None, prompt_initial)
    print_in_box_all_prompts_and_response("", prompt_initial, prompt_initial_response)

    # Step 2: The Feedback Mechanism
    feedback = """
The generated code is a good start, but it has a design flaw: 
The user's name and title text are not centered within the card. Please fix the CSS to center-align the text.
"""

    # response = get_completion(client, feedback, prompt_initial_response)
    # print_in_box_all_prompts_and_response(feedback, feedback, response)

    # Step 3: The Feedback Loop (The Corrective Prompt)

    prompt_corrective = f"""
You are a web developer. You previously generated some code that had an error.
Please revise the code to fix the issue described in the feedback.

Your previous code:
---
{prompt_initial_response}
---

Feedback on your code:
---
{feedback}
---

Please provide the complete, corrected HTML and CSS.
    """

    response = get_completion(client, None, prompt_corrective)
    print_in_box_all_prompts_and_response("", prompt_corrective, response)


if __name__ == '__main__':
    main()

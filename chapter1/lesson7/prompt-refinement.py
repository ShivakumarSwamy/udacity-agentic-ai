from dotenv import load_dotenv

from app.util import openai_client, get_completion, print_in_box_all_prompts_and_response

load_dotenv()


def main():
    client = openai_client()

    system_prompt_role_v1 = """
You are a cheerful food blogger.
    """

    user_prompt_template = """
Recommend a unique local dish in Bengaluru, India for first-time visitors seeking unique fusion flavors.
The response should be under {word_length} words, focus on taste, not name specific restaurants, be a single paragraph with a hook.
    """
    user_prompt = user_prompt_template.format(word_length=75)

    response_role_v1 = get_completion(client, system_prompt_role_v1, user_prompt)
    print_in_box_all_prompts_and_response(system_prompt_role_v1, user_prompt, response_role_v1)

    system_prompt_role_v2 = """
You are a High-Dining Food Critic and Connoisseur    
    """

    response_role_v2 = get_completion(client, system_prompt_role_v2, user_prompt)
    print_in_box_all_prompts_and_response(system_prompt_role_v2, user_prompt, response_role_v2)

    user_prompt = user_prompt_template.format(word_length=15)

    response_role_v1 = get_completion(client, system_prompt_role_v1, user_prompt)
    print_in_box_all_prompts_and_response(system_prompt_role_v1, user_prompt, response_role_v1)

    user_prompt = user_prompt_template.format(word_length=15) + """
Output JSON of the format {"dish_title": ..., "description": ...}    
    """

    response_role_v1 = get_completion(client, system_prompt_role_v1, user_prompt)
    print_in_box_all_prompts_and_response(system_prompt_role_v1, user_prompt, response_role_v1)


if __name__ == '__main__':
    main()

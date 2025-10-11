from dotenv import load_dotenv

from app.util import openai_client, get_completion, print_in_box_all_prompts_and_response

load_dotenv()


def main():
    client = openai_client()

    system_prompt = """
You are bond analyst who specialise in Non-convertible debentures (NCD)
    """

    user_prompt = """
Write an article about the new Navi Finserv Limited Feb 2024 NCD. 

Public issue of Secured, rated, listed, redeemable, non-convertible debentures for an amount aggregating up to ₹ 3,000 Million
(“Base Issue Size”) with an option to retain oversubscription up to ₹ 3,000 Million (“Green Shoe Option”) aggregating up to ₹ 6,000 Million
(“Issue Size”).

Keep article positive and encouraging for investors to invest. 
    """

    response = get_completion(client, system_prompt, user_prompt)

    print_in_box_all_prompts_and_response(system_prompt, user_prompt, response)


if __name__ == '__main__':
    main()

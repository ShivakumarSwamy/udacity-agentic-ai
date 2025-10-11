from enum import Enum

from openai import OpenAI


class OpenAIModels(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"


MODEL = OpenAIModels.GPT_41_NANO
SINGLE_TAB_LEVEL = 4


def get_completion_v2(client, messages, model=MODEL):
    """
    Function to get a completion from the OpenAI API.
    Args:
        client: open api client
        messages: array of role message
        model: The model to use (default is gpt-4.1-mini)
    Returns:
        The completion text
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


def get_completion(client, system_prompt, user_prompt, model=MODEL):
    """
    Function to get a completion from the OpenAI API.
    Args:
        client: open api client
        system_prompt: The system prompt
        user_prompt: The user prompt
        model: The model to use (default is gpt-4.1-mini)
    Returns:
        The completion text
    """
    messages = [
        {"role": "user", "content": user_prompt},
    ]
    if system_prompt is not None:
        messages = [
            {"role": "system", "content": system_prompt},
            *messages,
        ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


def display_responses(*args):
    """Helper function to display responses as Markdown, horizontally."""
    markdown_string = "<table><tr>"
    # Headers
    for arg in args:
        markdown_string += f"<th>System Prompt:<br />{arg['system_prompt']}<br /><br />"
        markdown_string += f"User Prompt:<br />{arg['user_prompt']}</th>"
    markdown_string += "</tr>"
    # Rows
    markdown_string += "<tr>"
    for arg in args:
        markdown_string += f"<td>Response:<br />{arg['response']}</td>"
    markdown_string += "</tr></table>"
    print(markdown_string)


def openai_client():
    return OpenAI()


def print_in_box(text, title="", cols=100, tab_level=0):
    """
    Prints the given text in a box with the specified title and dimensions.

    Args:
        text: The text to print in the box.
        title: The title of the box.
        cols: The width of the box.
        tab_level: The level of indentation for the box.
    """
    import textwrap

    text = str(text)

    # Make a box using extended ASCII characters
    if cols < 4 + tab_level * SINGLE_TAB_LEVEL:
        cols = 4 + tab_level * SINGLE_TAB_LEVEL

    tabs = " " * tab_level * SINGLE_TAB_LEVEL

    top = (
            tabs
            + "\u2554"
            + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
            + "\u2557"
    )
    if tab_level == 0:
        print()  # Print a newline before any box at level 0

    if title:
        # replace the middle of the top with the title
        title = "[ " + title + " ]"
        top = top[: (cols - len(title)) // 2] + title + top[(cols + len(title)) // 2:]
    print(top)

    for line in text.split("\n"):
        for wrapped_line in textwrap.wrap(
                line, cols - 4 - tab_level * SINGLE_TAB_LEVEL
        ):
            print(
                f"{tabs}\u2551 {wrapped_line:<{cols - 4 - tab_level * SINGLE_TAB_LEVEL}} \u2551"
            )

    print(
        f"{tabs}\u255a"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u255d"
    )


def print_in_box_all_prompts_and_response(system_prompt, user_prompt, response):
    print_in_box(system_prompt, "System Prompt")
    print_in_box(user_prompt, "User Prompt")
    print_in_box(response, "Response")

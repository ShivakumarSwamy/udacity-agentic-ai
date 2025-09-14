from dotenv import load_dotenv

from app.util import openai_client, OpenAIModels

load_dotenv()

client = openai_client()


def traditional_generate_response(query):
    """
    A traditional function that returns predefined responses based on keywords.
    """
    qry = query.lower()

    if "weather" in qry:
        return "The weather today in sunny with a high of 75°F."
    elif "time" in qry:
        return "The current time is 12:00PM."
    elif "hello" in qry or "hi" in qry:
        return "Hello! How can I help you today?"
    return "I'm not sure how to respond to that query"


def openai_generate_response(query):
    """
    Uses the OpenAI API to generate a response to the user's query.
    """
    if not client:
        return "OpenAI client not initialized. Please set your API key."

    try:
        response = client.chat.completions.create(model=OpenAIModels.GPT_4O_MINI,
                                                  messages=[
                                                      {"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": query},
                                                  ],
                                                  max_tokens=150
                                                  )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"


def main():
    # Sample queries
    queries = [
        "Hello there!",
        "What's the weather like?",
        "Tell me a short joke."
    ]

    print("=" * 50)
    print("DEMO: TRADITIONAL FUNCTION VS OPENAI AGENT")
    print("=" * 50)

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 30)

        traditional_response = traditional_generate_response(query)
        print(f"Traditional Function Response:\n{traditional_response}")
        print("-" * 30)

        print("OpenAI Agent would process this query similarly:")
        print("1. Take the query as input")
        print("2. Process it (send to OpenAI API)")
        print("3. Return a response")

        # Uncomment below to enable OpenAI API call (make sure your key is valid)
        ai_response = openai_generate_response(query)
        print(f"OpenAI Agent Response:\n{ai_response}")

        print("=" * 50)


if __name__ == '__main__':
    main()

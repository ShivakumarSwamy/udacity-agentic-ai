"""
Program Management Knowledge Agent - Starter Code

This program demonstrates two approaches to answering program management questions:
1. Using hardcoded knowledge
2. Using an LLM API

Complete the TODOs to build your knowledge agent.
"""
from dotenv import load_dotenv

from app.util import openai_client, OpenAIModels

load_dotenv()

client = openai_client()


def get_hardcoded_answer(question):
    """
    Return answers to program management questions using hardcoded knowledge.

    Args:
        question (str): The question about program management

    Returns:
        str: The answer to the question
    """
    ques = question.lower()

    if "gantt" in ques and "chart" in ques:
        return """
        A Gantt chart is a visual project schedule showing tasks, durations, and dependencies along a timeline, 
        helping managers plan, track progress, and meet deadlines efficiently.
        """
    elif "agile" in ques:
        return """
        Agile is an iterative project approach emphasizing collaboration, flexibility, and incremental delivery 
        through short, adaptive cycles to quickly respond to changing needs.
        """
    elif "sprint" in ques:
        return """
        A sprint is a fixed-length work cycle in Agile, usually 1–4 weeks, where teams deliver prioritized tasks, 
        review progress, and adapt plans for continuous improvement.
        """
    elif "critical" in ques and "path" in ques:
        return """
        The critical path is the sequence of dependent project tasks that dictates the minimum completion time, 
        where delays directly affect the overall project delivery date.
        """
    elif "milestone" in ques:
        return """
        Milestones are zero-duration checkpoints in a project marking key achievements or decision points, 
        used to measure progress and maintain alignment with objectives.
        """

    return """
        I'm sorry, I only have information on a few specific program management topics. 
        Could you ask about Gantt charts, Agile, sprints, critical path, or milestones?
    """


def get_llm_answer(question):
    """
    Get answers to program management questions using an LLM API.

    Args:
        question (str): The question about program management

    Returns:
        str: The answer from the LLM
    """
    if not client:
        return "OpenAI client not initialized. Please set your API key."

    try:
        response = client.chat.completions.create(model=OpenAIModels.GPT_4O_MINI,
                                                  messages=[
                                                      {
                                                          "role": "system",
                                                          "content": """
                        You are an expert assistant specializing in program management. 
                        Provide clear and concise answers to program management questions.
                    """
                                                      }, {
                                                          "role": "user",
                                                          "content": question
                                                      }
                                                  ], max_tokens=150
                                                  )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with LLM: {str(e)}"


# Demo function to compare both approaches
def compare_answers(question):
    """Compare answers from both approaches for a given question."""
    print(f"\nQuestion: {question}")
    print("-" * 50)

    hardcoded_answer = get_hardcoded_answer(question)
    print(f"Hardcoded Answer:\n{hardcoded_answer}")
    print("-" * 30)


    print("OpenAI Agent would process this query similarly:")
    print("1. Take the query as input")
    print("2. Process it (send to OpenAI API)")
    print("3. Return a response")
    llm_answer = get_llm_answer(question)
    print(f"LLM Answer:\n{llm_answer}")

    print("=" * 50)


def main():
    print("PROGRAM MANAGEMENT KNOWLEDGE AGENT DEMO")
    print("=" * 50)

    sample_questions = [
        "What is a Gantt chart?",
        "Tell me about Agile methodology.",
        "What are key project milestones?",
        "What is risk management in projects?",  # This one might not be hardcoded
        "Can you explain a sprint review?"
    ]

    for question in sample_questions:
        compare_answers(question)


if __name__ == '__main__':
    main()

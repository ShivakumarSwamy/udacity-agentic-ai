## Prompt Refinement Best Practices

- Write Clear and Detailed Instructions: The more precise and descriptive your instructions, the better the model will
  understand your intent. Don't assume the model can read your mind; tell it everything you want it to do.
- Use Roles or Personas: Assigning a specific role can help the model adopt the desired tone and style for the task.
- Break Down Complex Tasks: If a task is too complex, break it into smaller, simpler stages. Avoiding overly convoluted
  requests can help. In fact, asking the model to think about the problem before providing the final answer can be
  useful. If you ask it to "think in steps," it's called Chain-of-Thought, and you can even suggest the steps it should
  take.
- Specify Output Format and Constraints: Clearly state how you want the output structured (e.g., JSON, bullet points)
  and any limitations, like word count or phrases to include.
- Include Few-Shot Examples: Providing input-output examples is often extremely helpful for guiding the model's response
  style, format, and task execution.
- Provide Relevant Context: Give the model the information it needs to perform the task accurately, especially for
  factual information or tasks requiring specific knowledge.
- Optimize Tool Descriptions: If your prompt is part of an agentic system using tools, spend significant time making
  sure the tool descriptions and their input/output formats are clear. This helps the LLM make correct decisions about
  when and how to use them.

## Common Pitfalls to avoid

- Ambiguity: This is perhaps the most common pitfall. If your instructions are unclear or open to multiple
  interpretations, the LLM might choose one you didn't intend. Better models of the future still won't know about the
  instructions you didn't write down.
- Insufficient Context: Expecting the LLM to know information it hasn't been given is a guaranteed way to get incorrect
  or hallucinated outputs. Remember, it doesn't have access to your personal files or real-time private data.
- Too Much Context or Competing Instructions: While context is good, overwhelming the model with irrelevant information
  or giving conflicting instructions can degrade performance. Finding the right balance is key.
- Poor Tool Descriptions: As mentioned before, poorly described tools mean the LLM won't know how or when to use them
  correctly.
- Expecting Magical Understanding: Don't trust the hype. These are not omniscient systems that understand your
  underlying intent perfectly. They are probabilistic systems that rely heavily on your explicit instructions. Prompting
  requires precision.
- Bias and Factuality Issues: LLMs can generate incorrect information and reflect biases present in their training data.
  Always validate their output, especially for critical tasks.
- Adversarial Prompting Risks: Be aware that prompts can be exploited for prompt injection, leaking, or jailbreaking.
  Always expect a model to be used in unintended ways.
## Chaining Prompts for Agentic Reasoning

- Traditional LLMs are optimized for single-task input-output.
- A single, massive prompt for a complex task often leads to confusion and missed details.
- Asking an LLM to manage multiple dependencies, execute actions, and verify outcomes all at once can lead to errors.

Prompt chaining connects the inputs and outputs of prompts programmatically. The output of one LLM call becomes input
for the next, running in code or via an orchestrator. This builds sophisticated, scalable workflows.

## Sequential Prompting

Sequential Prompting, or multi-step reasoning, is breaking down a complex task into a series of smaller,
manageable sub-tasks (Task 1, Task 2, Task 3). Each sub-task is handled by its own prompt.
This is fundamental to agentic workflows.

## Output validate: Gate Checks

Gate checks are programmatic validations placed between steps in a prompt chain.
They act as quality control points, ensuring an output meets criteria before being passed on.
They rein in the stochastic and unpredictable behavior of LLMs

- If checks pass: Continue.
- If a check fails: The system can trigger an error and halt, retry the step, or retry the step including the reason
  for failure in the prompt (to make errors less likely on retry).

### Types of Gate Checks:

Format Checks:
Structure (JSON, XML), length, required fields. Libraries like Pydantic or LLM offerings with structured outputs can
help.

Content Checks:
Keywords, phrases, topics, relevancy. Regex, semantic embeddings, or other LLMs can be used.

Logic Checks:
Numerical/logical sense.
If generating code: does it compile? Does it import restricted libraries? Are extracted numeric values reasonable?

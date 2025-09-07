## Role Based Prompting

- A persona or role defines how an agent should behave - it's personality, tone, and perspective.

- **Role-Based Prompting (Agent Personas)**: A technique to guide a Large Language Model by giving it a specific
  identity or "persona" to inhabit, which helps produce outputs that are specialized and consistent with the traits
  of that defined role.

- **Role (or Persona):** A specific identity or character background provided to an LLM in a prompt to shape
  its behavior and output style.

## Prompt Components

- Role: The persona the LLM should adopt (e.g., "Act as a pirate").
- Task: The specific instruction or question (e.g., "Perform the calculation: 1+1?").
- Output Format: How the response should be structured (e.g., "A sentence in Markdown.").
- Examples: Sample input/output pairs (e.g., "Q: 1+3? / A: Tis 4, yar!").
- Context: Additional information needed for the task (e.g., current date, if asking for the date).

```text
Act like a pirate! #[Role]
Perform the calculation: 1 + 1? #[Task]
Output only one sentence in Markdown. #[Output Format]
Here’s an example: Q: 1 + 3? / A: Tis 4, yar!" #[Example]
```

## API vs LLM APP

- When working with API's, we provide system prompt before asking the real question with user prompt.
- While with LLM APP, you will provide both system and user prompt together.
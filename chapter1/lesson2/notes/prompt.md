## Prompt

- A prompt is a set of instructions provided to an LLM that customizes, enhances, or refines its capabilities
- Prompting is the method by which we "program" the LLM.

## Guide

- Assign a professional persona
- Introduce concrete constraints
- Request Step-by-Step Reasoning

### Example Organize My Workspace

user prompt

```
Give me a simple plan to declutter and organize my workspace.
```

system prompt:
generic/plain prompt

```
You are a helpful assistant.
```

professional persona

```
You are an expert professional organizer and productivity coach.
```

constraint

```
You are an expert professional organizer and productivity coach.
The plan must be achievable in one hour and require no purchases, using only existing household items.
```

step-by-step reasoning

```
You are an expert professional organizer and productivity coach.
The plan must be achievable in one hour and require no purchases, using only existing household items.
Explain your reasoning for each step of the plan in a thoughtful way before presenting the final checklist.
```

## Prompting & Efficiency

> you can try to solve a complex problem by giving a vague instruction to a very large, expensive model
> (like OpenAI o3) and hoping it correctly infers all the necessary steps.
> This approach is slow and costly to run for every user request.
>
> The alternative is what this course teaches: you, the engineer, use prompting techniques
> like **Chain-of-Thought and Prompt Chaining** to explicitly break the problem down into a series of logical steps.
> Because each individual step is simpler and more focused, you can often use a smaller, faster,
> and much cheaper model (like GPT-4.1 mini) to successfully execute each one.
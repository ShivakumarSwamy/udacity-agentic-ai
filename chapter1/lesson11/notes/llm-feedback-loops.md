## LLM Feedback Loops

The core mechanism is "prompt chaining". The output of one step becomes input for the next. In a feedback loop,
the "feedback" from evaluating an LLM's output is incorporated into a new prompt for the next iteration, guiding the
model towards a better result.

### Sources of Feedback for LLMs:

- Self-Correction: Prompt the LLM to evaluate its own previous response based on your criteria. For example, asking the
  same LLM to review our coffee email for politeness and then correct it. Its suggestions become feedback for the next
  iteration.

- External Tools: If it generates code, running that code and getting errors or test results provides concrete feedback.

- Validation Checks: Programmatic checks. If extracting info into JSON, code can parse the output and check validity or
  missing fields. The result (e.g., "Missing 'email_address' field") becomes feedback.

- User Input: Direct feedback. A user might say, "This itinerary doesn't include any outdoor activities." This is sent
  back to the LLM agent to regenerate. A blocking tool call can wait for user input.

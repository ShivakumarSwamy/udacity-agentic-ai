## Ground Truth Evaluations of Prompts

The most straightforward, effective, and reliable way is to create a ground truth set for scoring future outputs.

1. Start by defining the task and identifying the criteria for success. What does "good" output look like? Does it
   require
   factual accuracy, specific formatting, or a particular tone?
2. Based on this, develop a set of test inputs and the ideal outputs – your ground truth.
3. When your AI Agent generates a response, compare it to the ground truth.
    * For structured data like JSON, use checks to ensure the agent adheres to the expected format and values. Start
      with
      traditional Machine Learning evaluation metrics such as completeness, accuracy, precision, and recall.
    * For textual responses or even images, which are more freeform, you may employ another LLM as a judge (
      LLM-as-a-judge),
      feeding it both the agent's output and the ground truth and asking it to score the agent based on your provided
      criteria. Note, in this case, you will need to evaluate the evaluator!
4. In all these cases, it’s important to continue to view the raw inputs and outputs of your models, sometimes called
   traces. This will give you a better understanding of what is actually going on and help you catch errors your
   evaluation
   pipeline may miss.

## Other Evaluation Types

Other evaluation methods not always based on a ground truth dataset are also important:

* Consistency & Persona Adherence: Is the agent staying within its defined role? This is essential, for instance, in the
  case of a Customer Support agent. If the agent is supposed to be a hospital assistant, does it stay within that role,
  even if asked about non-medical topics? A mock conversation can be passed to the Agent and the output can be evaluated
  by another LLM.
* Robustness Testing: Assess resilience against adversarial attacks. This is critical if the agent handles sensitive
  information or could cause harm.
* Simple Metrics: Easy-to-implement measures like median response length are good for evaluating and monitoring language
  models for improved usability and cost efficiency.

## Terms

**Ground Truth Evaluations:** A method of evaluation where you create a set of test inputs and their corresponding ideal
outputs (the ground truth) to score an agent's responses against.

**LLM-as-a-judge:** An evaluation technique where another LLM is used as a "judge" to score an agent's output against
the
ground truth based on your provided criteria.

**Traces:** The raw inputs and outputs of a model for a given interaction, which are important to view to understand the
model's behavior and catch potential errors.

**Consistency & Persona Adherence:** An evaluation method that assesses whether an agent is staying within its defined
role,
even when asked about non-medical or other out-of-scope topics.

**Robustness Testing:** The process of assessing an agent's resilience against adversarial attacks, which is critical
for
agents that handle sensitive information.

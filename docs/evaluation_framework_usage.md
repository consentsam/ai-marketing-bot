# YieldFi AI Agent - Evaluation Framework Usage Guide

This document provides guidance on how to use the evaluation framework created in Step 21 to assess the quality of AI-generated responses.

## Overview

The evaluation framework provides metrics to assess AI-generated responses against three key dimensions:

1. **Tone Match**: How well the AI's tone matches the expected tone
2. **Relevance**: How relevant the response is to the original input context
3. **Factual Accuracy**: How accurately the response includes expected facts

## Getting Started

### Prerequisites

- Ensure NLTK resources are installed:

```bash
python -m nltk.downloader stopwords punkt
```

- The evaluation framework uses the following files:
  - `src/evaluation/metrics.py`: Contains the metrics functions
  - `src/evaluation/evaluator.py`: Contains the `Evaluator` class
  - `data/input/evaluation_golden_set.json`: Sample evaluation data

### Basic Usage

Here's a basic example of how to use the evaluator:

```python
from src.models.response import AIResponse
from src.evaluation.evaluator import Evaluator

# Create or load an AIResponse object
ai_response = AIResponse(
    content="YieldFi offers competitive APYs and strong security features. Launched in 2023.",
    tone="positive",
    model_used="gpt-4",
    prompt_used="sample prompt",
    response_type="TWEET_REPLY",
    source_tweet_id="123456",
    responding_as="OFFICIAL",
    target_account="community"
)

# Original tweet content that generated this response
original_content = "Is YieldFi secure and does it offer good yields?"

# Knowledge snippet that was used
knowledge_snippet = "YieldFi launched in 2023 with a focus on security and competitive yields."

# Ground truth data for evaluation
ground_truth = {
    "expected_tone": "positive",
    "ground_truth_facts": [
        "competitive APYs",
        "security features",
        "launched in 2023"
    ]
}

# Create an evaluator with default metrics
evaluator = Evaluator()

# Evaluate the response
scores = evaluator.evaluate_response(
    ai_response=ai_response,
    original_tweet_content=original_content,
    knowledge_snippet_used=knowledge_snippet,
    ground_truth_data=ground_truth
)

print(f"Evaluation scores: {scores}")
```

### Batch Evaluation

You can evaluate multiple responses at once:

```python
# Prepare a list of evaluation data (AIResponse, context, knowledge, ground_truth)
batch_data = [
    (ai_response1, original_content1, knowledge1, ground_truth1),
    (ai_response2, original_content2, knowledge2, ground_truth2),
    # ... more items
]

# Run batch evaluation
batch_results = evaluator.run_batch_evaluation(batch_data)

# Process results
for i, result in enumerate(batch_results):
    print(f"Response {i+1} scores: {result}")
```

## Metrics Details

### Tone Match Score

- Range: 0.0 to 1.0 (binary match/no-match)
- Calculation: 1.0 if tones match exactly (case-insensitive), 0.0 otherwise
- Special cases: Returns 0.0 if either tone is None or empty

### Relevance Score

- Range: 0.0 to 1.0
- Calculation: Jaccard index of preprocessed tokens (intersection / union)
- Preprocessing: Tokenization, lowercasing, stopword removal, alphanumeric filtering
- Requirements: NLTK resources (fallback logic exists if unavailable)

### Factual Accuracy Score

- Range: 0.0 to 1.0
- Calculation: (Number of facts found) / (Total number of facts)
- Matching: Case-insensitive substring matching
- Special cases: Returns 1.0 if no facts to check (vacuously true)

## Advanced Usage

### Custom Metrics Set

You can select which metrics to run:

```python
# Only use tone match and factual accuracy
evaluator = Evaluator(metrics_to_run=["tone_match", "factual_accuracy"])
```

### Custom Golden Set

Create your own evaluation data set similar to `evaluation_golden_set.json`:

```json
[
    {
        "id": "custom_eval_1",
        "description": "Description of the test case",
        "original_tweet_content": "Original query or tweet content",
        "knowledge_snippet_used": "Knowledge that was used for generation",
        "ai_response_content": "The AI's generated response content",
        "ai_response_analyzed_tone": "positive",
        "ground_truth_data": {
            "expected_tone": "positive",
            "ground_truth_facts": [
                "fact 1",
                "fact 2"
            ]
        }
    }
]
```

## Debugging

If you encounter issues:

1. Ensure NLTK resources are installed properly
2. Verify that the AIResponse objects have both `content` and `tone` attributes
3. Check that ground truth data contains the expected keys
4. Review the output for any "N/A" or "Error" messages, which indicate missing or problematic inputs

## Using for Continuous Monitoring

Consider adding the evaluation framework to your CI/CD pipeline or as a scheduled job to track performance over time:

```python
import json
import datetime

# Load test cases
with open("data/input/evaluation_golden_set.json", "r") as f:
    test_cases = json.load(f)

# Run evaluations
evaluator = Evaluator()
results = []

for case in test_cases:
    # Create response object from test case (details omitted)
    # ...
    
    # Run evaluation
    score = evaluator.evaluate_response(...)
    results.append({
        "id": case["id"],
        "timestamp": datetime.datetime.now().isoformat(),
        "scores": score
    })

# Log or store results
with open(f"data/output/eval_results_{datetime.date.today()}.json", "w") as f:
    json.dump(results, f, indent=2)
```

## Conclusion

The evaluation framework provides a quantitative way to assess AI-generated responses. By using it consistently, you can track improvements, identify issues, and ensure the quality of responses remains high as you develop the YieldFi AI Agent further. 
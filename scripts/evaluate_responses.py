#!/usr/bin/env python3
"""
YieldFi AI Agent - Response Evaluation Script

This script demonstrates how to use the evaluation framework to assess the quality
of AI-generated responses using the predefined golden set.
"""

import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Add src directory to Python path if needed
if not any(p.endswith("src") for p in sys.path):
    sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.models.response import AIResponse
    from src.evaluation.evaluator import Evaluator
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you're running this script from the project root or that src is in PYTHONPATH")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("evaluate_responses")

def load_golden_set(file_path: str = "data/input/evaluation_golden_set.json") -> List[Dict[str, Any]]:
    """Load the evaluation golden set from the specified JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} test cases from {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Golden set file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in golden set file: {file_path}")
        return []

def create_ai_response_from_case(case: Dict[str, Any]) -> AIResponse:
    """Create an AIResponse object from a test case in the golden set."""
    return AIResponse(
        content=case["ai_response_content"],
        tone=case["ai_response_analyzed_tone"],
        response_type="TWEET_REPLY",  # Assuming this for test cases
        model_used="test_model",
        prompt_used="test_prompt",
        source_tweet_id=f"test_{case['id']}",
        responding_as="OFFICIAL",
        target_account="COMMUNITY_MEMBER",
        generation_time=datetime.now()
    )

def prepare_evaluation_batch(cases: List[Dict[str, Any]]) -> List[Tuple[AIResponse, Optional[str], Optional[str], Optional[Dict[str, Any]]]]:
    """Prepare a batch of evaluation data from the test cases."""
    batch_data = []
    for case in cases:
        ai_response = create_ai_response_from_case(case)
        original_content = case["original_tweet_content"]
        knowledge_snippet = case.get("knowledge_snippet_used")
        ground_truth = case["ground_truth_data"]
        
        batch_data.append((ai_response, original_content, knowledge_snippet, ground_truth))
    
    return batch_data

def save_results(results: List[Dict[str, Any]], cases: List[Dict[str, Any]], output_dir: str = "data/output"):
    """Save the evaluation results to a JSON file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    output_data = []
    for i, (result, case) in enumerate(zip(results, cases)):
        output_data.append({
            "id": case["id"],
            "description": case["description"],
            "timestamp": datetime.now().isoformat(),
            "scores": result
        })
    
    output_file = Path(output_dir) / f"eval_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"Results saved to {output_file}")
    return output_file

def summarize_results(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate average scores across all test cases."""
    summary = {}
    
    # Initialize counters for each metric
    metrics = set()
    for result in results:
        metrics.update(result.keys())
    
    for metric in metrics:
        valid_scores = []
        for result in results:
            if metric in result and isinstance(result[metric], (int, float)):
                valid_scores.append(result[metric])
        
        if valid_scores:
            summary[f"avg_{metric}"] = sum(valid_scores) / len(valid_scores)
            summary[f"min_{metric}"] = min(valid_scores)
            summary[f"max_{metric}"] = max(valid_scores)
    
    return summary

def main():
    logger.info("Starting evaluation process")
    
    # Load the golden set
    cases = load_golden_set()
    if not cases:
        logger.error("No test cases found. Exiting.")
        return
    
    # Create the evaluator with default metrics
    evaluator = Evaluator()
    logger.info(f"Evaluator initialized with metrics: {evaluator.metrics_to_run}")
    
    # Prepare the evaluation batch
    batch_data = prepare_evaluation_batch(cases)
    logger.info(f"Prepared {len(batch_data)} test cases for evaluation")
    
    # Run batch evaluation
    logger.info("Running batch evaluation...")
    batch_results = evaluator.run_batch_evaluation(batch_data)
    
    # Save results
    output_file = save_results(batch_results, cases)
    
    # Summarize results
    summary = summarize_results(batch_results)
    logger.info(f"Evaluation summary: {summary}")
    
    # Print detailed results for demonstration
    print("\n===== Evaluation Results =====")
    for i, (result, case) in enumerate(zip(batch_results, cases)):
        print(f"\nCase {i+1}: {case['id']} - {case['description']}")
        print("Original Tweet: " + case["original_tweet_content"][:50] + "..." if len(case["original_tweet_content"]) > 50 else case["original_tweet_content"])
        print("AI Response: " + case["ai_response_content"][:50] + "..." if len(case["ai_response_content"]) > 50 else case["ai_response_content"])
        print("Scores:")
        for metric, score in result.items():
            print(f"  - {metric}: {score}")
    
    print(f"\nDetailed results saved to: {output_file}")
    print("\n===== Summary =====")
    for metric, value in summary.items():
        print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    main() 
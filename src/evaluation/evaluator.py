# Changelog:
# - 2025-05-16: Initial creation for Step 21 (Evaluation Framework).
#   - Added Evaluator class to orchestrate metric calculations based on calculate_* functions from metrics.py.

"""
Evaluation framework for AI responses.
Defines Evaluator to run configured metrics against AIResponse objects.
"""

from typing import List, Optional, Dict, Any, Callable, Tuple

# Attempt to import models and metrics from src, fallback for local running
try:
    # Ensure these imports point to the correct model definitions as per your project structure
    from src.models.response import AIResponse 
    # from src.models.tweet import Tweet # Not directly used in current Evaluator args, but good to keep in mind
    
    # Ensure these imports point to the refined metric functions
    from src.evaluation.metrics import (
        calculate_tone_match_score,
        calculate_relevance_score,
        calculate_factual_accuracy_score
    )
except ImportError:
    # This block is for local testing if src is not in PYTHONPATH.
    # In a real application run, the try block should succeed.
    # You might need to adjust these paths if your local test setup differs.
    print("Warning: Using fallback imports for Evaluator. Ensure PYTHONPATH is set for actual runs.")
    from models.response import AIResponse # type: ignore
    # from models.tweet import Tweet # type: ignore
    from evaluation.metrics import (
        calculate_tone_match_score, # type: ignore
        calculate_relevance_score, # type: ignore
        calculate_factual_accuracy_score # type: ignore
    )

class Evaluator:
    """
    Orchestrates the evaluation of AI-generated responses using a set of metrics
    as defined in Step 21 of the implementation plan.
    """
    def __init__(self, metrics_to_run: Optional[List[str]] = None):
        """
        Initializes the Evaluator.

        Args:
            metrics_to_run: A list of metric names to run. 
                            If None, all available default metrics will be run.
                            Available metrics: 'tone_match', 'relevance', 'factual_accuracy'.
        """
        self.available_metrics: Dict[str, Callable[..., float]] = {
            'tone_match': calculate_tone_match_score,
            'relevance': calculate_relevance_score,
            'factual_accuracy': calculate_factual_accuracy_score,
        }

        if metrics_to_run is None:
            self.metrics_to_run = list(self.available_metrics.keys())
            print(f"Evaluator initialized to run default metrics: {self.metrics_to_run}")
        else:
            self.metrics_to_run = []
            unknown_metrics = []
            for m_name in metrics_to_run:
                if m_name in self.available_metrics:
                    self.metrics_to_run.append(m_name)
                else:
                    unknown_metrics.append(m_name)
            
            if unknown_metrics:
                print(f"Warning: Unknown metrics specified and ignored during Evaluator init: {unknown_metrics}")
            print(f"Evaluator initialized to run specified metrics: {self.metrics_to_run}")

    def evaluate_response(
        self,
        ai_response: AIResponse,
        original_tweet_content: Optional[str] = None,
        knowledge_snippet_used: Optional[str] = None,
        ground_truth_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates a single AIResponse object against the configured metrics.

        Args:
            ai_response: The AIResponse object to evaluate. Requires `content` and `tone` attributes.
            original_tweet_content: The content of the original tweet or input context (for relevance).
            knowledge_snippet_used: Any knowledge snippet used in generating the response (for relevance).
            ground_truth_data: A dictionary containing ground truth information. Expected keys:
                               - 'expected_tone' (str, optional): For 'tone_match' metric.
                               - 'ground_truth_facts' (List[str], optional): For 'factual_accuracy' metric.

        Returns:
            A dictionary containing the scores for each metric run. 
            Value can be a float score, 'N/A (reason)', or 'Error: (message)'.
        """
        if ground_truth_data is None:
            ground_truth_data = {}

        scores: Dict[str, Any] = {}

        if not self.metrics_to_run:
            return {"message": "No metrics configured to run."}

        for metric_name in self.metrics_to_run:
            metric_func = self.available_metrics[metric_name]
            score_value: Any = None
            try:
                if metric_name == 'tone_match':
                    expected_tone = ground_truth_data.get('expected_tone')
                    if not hasattr(ai_response, 'tone'):
                         score_value = "Error: AIResponse object missing 'tone' attribute."
                    elif expected_tone is not None:
                        score_value = metric_func(generated_tone=ai_response.tone, expected_tone=expected_tone)
                    else:
                        score_value = "N/A (no 'expected_tone' in ground_truth_data)"
                
                elif metric_name == 'relevance':
                    if original_tweet_content is not None:
                        if not hasattr(ai_response, 'content'):
                            score_value = "Error: AIResponse object missing 'content' attribute."
                        else:
                            score_value = metric_func(
                                generated_text=ai_response.content,
                                input_context=original_tweet_content,
                                knowledge_snippet=knowledge_snippet_used
                            )
                    else:
                        score_value = "N/A (no 'original_tweet_content' provided for relevance)"
                
                elif metric_name == 'factual_accuracy':
                    facts_to_check = ground_truth_data.get('ground_truth_facts')
                    if not hasattr(ai_response, 'content'):
                        score_value = "Error: AIResponse object missing 'content' attribute."
                    else:
                        score_value = metric_func(
                            generated_text=ai_response.content,
                            ground_truth_facts=facts_to_check # metric handles None/empty list
                        )
                else:
                    # This case should not be reached if metrics_to_run is properly filtered by available_metrics
                    score_value = f"Error: Unknown metric '{metric_name}' dispatch attempted."
            
            except Exception as e:
                print(f"Error calculating metric '{metric_name}': {e}")
                score_value = f"Error: {str(e)}"
            
            scores[metric_name] = score_value
        
        return scores

    def run_batch_evaluation(
        self,
        evaluation_data: List[Tuple[AIResponse, Optional[str], Optional[str], Optional[Dict[str, Any]]]]
    ) -> List[Dict[str, Any]]:
        """
        Evaluates a batch of AI responses.

        Args:
            evaluation_data: A list of tuples, where each tuple contains:
                - ai_response (AIResponse): The AI response object.
                - original_tweet_content (Optional[str]): Context for relevance.
                - knowledge_snippet_used (Optional[str]): Knowledge for relevance.
                - ground_truth_data (Optional[Dict[str, Any]]): Ground truth for metrics.

        Returns:
            A list of score dictionaries, one for each evaluated response.
        """
        batch_scores_results: List[Dict[str, Any]] = []
        for i, (ai_response, orig_content, knowledge_snippet, gt_data) in enumerate(evaluation_data):
            # print(f"Evaluating item {i+1}/{len(evaluation_data)}")
            scores = self.evaluate_response(
                ai_response=ai_response,
                original_tweet_content=orig_content,
                knowledge_snippet_used=knowledge_snippet,
                ground_truth_data=gt_data
            )
            batch_scores_results.append(scores)
        return batch_scores_results


if __name__ == '__main__':
    # This is a placeholder for local testing.
    # Proper testing should be done via unit tests with mocked models and comprehensive scenarios.

    print("--- Evaluator Basic End-to-End Tests ---")

    # Mock AIResponse (must have 'content' and 'tone' attributes as expected by Evaluator)
    class MockAIResponse:
        def __init__(self, content: str, tone: Optional[str], other_data: Optional[Dict] = None):
            self.content = content
            self.tone = tone # Analyzed tone of the AI's own response
            self.other_data = other_data if other_data is not None else {}

        def __str__(self):
            return f"MockAIResponse(content='{self.content[:30]}...', tone='{self.tone}')"

    # Test case 1: All metrics, good response
    response1 = MockAIResponse(
        content="YieldFi is an excellent platform, providing high yields. It was established in 2023 and is secure.", 
        tone="positive"
    )
    gt1 = {
        'expected_tone': 'positive',
        'ground_truth_facts': ["established in 2023", "high yields", "secure"]
    }
    original_content1 = "Tell me about YieldFi and its key benefits and features."
    knowledge1 = "YieldFi is known for high yields. Established in 2023. Security is a priority."

    evaluator_all = Evaluator() # Uses all default metrics ['tone_match', 'relevance', 'factual_accuracy']
    scores1 = evaluator_all.evaluate_response(response1, original_content1, knowledge1, gt1)
    print(f"\nScores for Response 1 (all metrics, good): {scores1}")
    # Expected rough values: tone_match: 1.0, factual_accuracy: 1.0, relevance: >0.5 (actual depends on NLTK processing)

    # Test case 2: Tone mismatch and missing fact
    response2 = MockAIResponse(content="The platform is okay, but could be better.", tone="neutral")
    gt2 = {
        'expected_tone': 'very positive', # Mismatch
        'ground_truth_facts': ["offers amazing rates", "user-friendly interface"] # Facts likely missing
    }
    original_content2 = "Is YieldFi good?"
    scores2 = evaluator_all.evaluate_response(response2, original_content2, None, gt2)
    print(f"\nScores for Response 2 (tone mismatch, facts missing): {scores2}")
    # Expected: tone_match: 0.0, factual_accuracy: 0.0, relevance: some value

    # Test case 3: Specified metrics (relevance only), no original content for relevance
    evaluator_relevance = Evaluator(metrics_to_run=['relevance', 'non_existent_metric'])
    response3 = MockAIResponse(content="This is a test.", tone="neutral")
    gt3 = {'ground_truth_facts': ["test fact"]}
    scores3 = evaluator_relevance.evaluate_response(response3, None, None, gt3)
    print(f"\nScores for Response 3 (relevance only, no context): {scores3}")
    # Expected: relevance: "N/A (no 'original_tweet_content' provided for relevance)". Warning for non_existent_metric.
    
    # Test case 4: AIResponse missing 'tone' attribute
    class MockAIResponseNoTone:
        def __init__(self, content: str):
            self.content = content
    response4_no_tone = MockAIResponseNoTone(content="Test content.")
    gt4 = {'expected_tone': 'positive'}
    # Need to cast to AIResponse for type checker if strict, but for runtime test this is fine.
    scores4 = evaluator_all.evaluate_response(response4_no_tone, "A question", None, gt4) # type: ignore
    print(f"\nScores for Response 4 (AIResponse missing tone): {scores4}")
    # Expected: tone_match: "Error: AIResponse object missing 'tone' attribute."

    # Batch evaluation example
    print("\n--- Batch Evaluation Test ---")
    batch_data_items = [
        (response1, original_content1, knowledge1, gt1),
        (response2, original_content2, None, gt2),
        (MockAIResponse("Third response", "neutral"), "Topic 3", "Knowledge for 3", {'expected_tone': 'neutral'})
    ]
    batch_scores_result = evaluator_all.run_batch_evaluation(batch_data_items)
    for i, item_scores in enumerate(batch_scores_result):
        print(f"Batch item {i+1} scores: {item_scores}") 
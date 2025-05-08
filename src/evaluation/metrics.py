# Changelog:
# - 2025-05-17: Removed runtime NLTK download attempts. Added check for resources.
# - 2025-05-17: Made NLTK resource download more verbose for diagnostics.
# - 2025-05-16: Refined for Step 21 (Evaluation Framework).
#   - Kept calculate_tone_match_score, calculate_relevance_score, calculate_factual_accuracy_score.
#   - Removed older/redundant metric functions.
#   - Updated __main__ for new functions.
# - 2025-05-16: Initial creation for Step 21 (Evaluation Framework) (previous attempt, merged).
# - 2025-05-07 12:00 - Step 21 - Create evaluation metrics module (original changelog entry from file).

"""
Evaluation metrics for AIResponse objects.
Provides functions to assess response quality based on the Step 21 Implementation Plan:
- Tone Match: Consistency of AI response tone with an expected tone.
- Relevance: How relevant the AI response is to the input context and knowledge.
- Factual Accuracy: Basic check against a list of ground truth facts.
"""

from typing import List, Optional, Set, Dict, Any # Added Dict, Any for broader use if Evaluator needs them
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys # For printing to stderr
import re  # Added for regex-based fallback tokenization

# --- NLTK Resource Check ---
# Ensure required NLTK resources are available; download if missing.
_resources_to_download = [
    ('tokenizers/punkt', 'punkt'),
    ('corpora/stopwords', 'stopwords'),
]
for resource_path, download_name in _resources_to_download:
    try:
        nltk.data.find(resource_path)
    except LookupError:
        print(f"NLTK resource '{download_name}' not found. Downloading...", file=sys.stderr)
        nltk.download(download_name, quiet=True)
# Define default stopwords list, falling back to manual if NLTK resources not available
try:
    _stopwords = stopwords.words('english')
    word_tokenize("Test sentence.")
    NLTK_RESOURCES_AVAILABLE = True
    DEFAULT_STOP_WORDS: Set[str] = set(_stopwords)
except LookupError:
    NLTK_RESOURCES_AVAILABLE = False
    # Fallback manual stopwords list (English stopwords + literal 'stopwords')
    DEFAULT_STOP_WORDS: Set[str] = {
        'i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves',
        'he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves',
        'what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being',
        'have','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while',
        'of','at','by','for','with','about','against','between','into','through','during','before','after','above','below',
        'to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when',
        'where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own',
        'same','so','than','too','very','s','t','can','will','just','don','should','now',
        'stopwords'
    }
    print("ERROR: Failed to load NLTK resources; using manual stopwords list.", file=sys.stderr)
# --- End NLTK Resource Check ---

def calculate_tone_match_score(generated_tone: Optional[str], expected_tone: Optional[str]) -> float:
    """
    Calculates the tone match score.
    Returns 1.0 if tones match (case-insensitive), 0.0 otherwise.
    If either tone is None or empty, returns 0.0.
    """
    if not generated_tone or not expected_tone:
        return 0.0
    return 1.0 if generated_tone.lower() == expected_tone.lower() else 0.0

def _preprocess_text(text: str, stop_words_set: Set[str]) -> Set[str]:
    """Helper function to tokenize, lowercase, and remove stopwords."""
    if not NLTK_RESOURCES_AVAILABLE:
        print("Warning: NLTK resources unavailable, using regex fallback for preprocessing.", file=sys.stderr)
        # Use regex to extract words, stripping punctuation
        tokens = re.findall(r"\b\w+\b", text.lower())
        return {word for word in tokens if word not in stop_words_set}
    
    tokens = word_tokenize(text.lower())
    # Keep alphanumeric words not in stopwords
    return {word for word in tokens if word.isalnum() and word not in stop_words_set}

def calculate_relevance_score(
    generated_text: str,
    input_context: str,
    knowledge_snippet: Optional[str] = None,
    stop_words: Optional[Set[str]] = None
) -> float:
    """
    Calculates a basic relevance score based on overlapping non-stop-words
    between the generated text and the combined input context + knowledge snippet.
    Score is Jaccard index: (intersection size) / (union size).
    """
    current_stop_words = stop_words if stop_words is not None else DEFAULT_STOP_WORDS

    processed_generated_text = _preprocess_text(generated_text, current_stop_words)
    
    combined_context_str = input_context
    if knowledge_snippet:
        combined_context_str = f"{combined_context_str} {knowledge_snippet}"
    
    processed_context = _preprocess_text(combined_context_str, current_stop_words)

    # Handle cases where one or both texts are empty after preprocessing
    if not processed_context and not processed_generated_text:
        return 1.0  # Both empty after processing: consider perfectly relevant or undefined. 1.0 for Jaccard.
    if not processed_context or not processed_generated_text: # One is empty, the other is not.
        return 0.0 # No overlap possible if one set is empty and the other is not.

    intersection = processed_generated_text.intersection(processed_context)
    union = processed_generated_text.union(processed_context)

    if not union: 
        return 1.0 if not processed_generated_text and not processed_context else 0.0
        
    return len(intersection) / len(union)

def calculate_factual_accuracy_score(
    generated_text: str,
    ground_truth_facts: Optional[List[str]] = None
) -> float:
    """
    Calculates a basic factual accuracy score.
    Checks for the presence of each ground_truth_fact (case-insensitive substring) in the generated_text.
    Score is (number of facts found) / (total number of facts).
    Returns 1.0 if ground_truth_facts is None or empty (vacuously true, as no facts to be wrong about).
    """
    if not ground_truth_facts: 
        return 1.0

    found_facts_count = 0
    generated_text_lower = generated_text.lower()
    for fact in ground_truth_facts:
        if fact.strip().lower() in generated_text_lower: 
            found_facts_count += 1
    
    # Avoid division by zero if len(ground_truth_facts) is 0 (though handled by the check above)
    return found_facts_count / len(ground_truth_facts) if ground_truth_facts else 1.0 


if __name__ == '__main__':
    # Check NLTK status first
    if not NLTK_RESOURCES_AVAILABLE:
        print("\nCannot run __main__ tests because NLTK resources are missing.", file=sys.stderr)
        print("Please download them first.", file=sys.stderr)
        sys.exit(1)
        
    print("--- Metric Function Tests (requires NLTK resources) ---")
    
    print("\n--- calculate_tone_match_score Tests ---")
    print(f"Match (positive, positive): {calculate_tone_match_score('positive', 'positive')} (Expected: 1.0)")
    print(f"Mismatch (positive, negative): {calculate_tone_match_score('positive', 'negative')} (Expected: 0.0)")
    print(f"Case Insensitive (Positive, positive): {calculate_tone_match_score('Positive', 'positive')} (Expected: 1.0)")
    print(f"None Input (None, positive): {calculate_tone_match_score(None, 'positive')} (Expected: 0.0)")
    print(f"Empty Input ('', positive): {calculate_tone_match_score('', 'positive')} (Expected: 0.0)")
    print(f"Both None: {calculate_tone_match_score(None, None)} (Expected: 0.0)")

    print("\n--- calculate_relevance_score Tests ---")
    text1 = "This is a great and awesome product with many features."
    context1 = "The product is awesome and has great features."
    knowledge1 = "It was released last year."
    # Expected intersection: {'product', 'awesome', 'great', 'features'} (4)
    # Expected union: {'great', 'awesome', 'product', 'many', 'features', 'has', 'released', 'last', 'year'} (9)
    # Score: 4/9 = 0.444...
    print(f"Example 1: {calculate_relevance_score(text1, context1, knowledge1)} (Expected: ~0.444)")

    text2 = "Weather is sunny today and very warm."
    context2 = "Is it raining today? What is the weather like?"
    # p_text2 = {'weather', 'sunny', 'today', 'warm'}
    # p_context2 = {'raining', 'today', 'weather', 'like'}
    # Inter: {'weather', 'today'} (2)
    # Union: {'weather', 'sunny', 'today', 'warm', 'raining', 'like'} (6)
    # Score: 2/6 = 0.333...
    print(f"Example 2: {calculate_relevance_score(text2, context2)} (Expected: ~0.333)")
    
    print(f"Empty Generated: {calculate_relevance_score('', 'some context')} (Expected: 0.0)")
    print(f"Empty Context (and no knowledge): {calculate_relevance_score('some generated', '')} (Expected: 0.0)")
    print(f"Both Empty: {calculate_relevance_score('', '')} (Expected: 1.0)")
    print(f"No Overlap: {calculate_relevance_score('completely different', 'topic is new')} (Expected: 0.0)")
    print(f"Full Overlap (processed): {calculate_relevance_score('yieldfi is great', 'yieldfi is great')} (Expected: 1.0)")

    print("\n--- calculate_factual_accuracy_score Tests ---")
    facts_text_ex = "The sky is blue and the grass is green. Our CEO is Alex. Founded in 2023."
    
    true_facts1 = ["sky is blue", "grass is green"]
    print(f"All Found: {calculate_factual_accuracy_score(facts_text_ex, true_facts1)} (Expected: 1.0)")
    
    true_facts2 = ["sky is blue", " grass is red "] 
    print(f"One Found (stripping fact): {calculate_factual_accuracy_score(facts_text_ex, true_facts2)} (Expected: 0.5)")

    true_facts3: List[str] = []
    print(f"No Facts to Check (Empty List): {calculate_factual_accuracy_score(facts_text_ex, true_facts3)} (Expected: 1.0)")
    
    print(f"No Facts to Check (None): {calculate_factual_accuracy_score(facts_text_ex, None)} (Expected: 1.0)")

    true_facts4 = ["CEO is Alex", "Founded in 2023"]
    print(f"Multiple specific facts: {calculate_factual_accuracy_score(facts_text_ex, true_facts4)} (Expected: 1.0)")

    true_facts5 = ["Our CEO is Alex.", "The company is YieldFi."] 
    print(f"Partial Match Complex: {calculate_factual_accuracy_score(facts_text_ex, true_facts5)} (Expected: 0.5)")

    facts_text_typo = "The sky is bluee and the grass is gren."
    true_facts_typo = ["sky is blue", "grass is green"]
    print(f"Typo in text, facts not found: {calculate_factual_accuracy_score(facts_text_typo, true_facts_typo)} (Expected: 0.0)") 
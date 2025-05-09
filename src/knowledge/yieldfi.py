# Changelog:
# 2025-05-07 20:12 - Step 10.3 - Implemented StaticJSONKnowledgeSource and YieldFiDocsKnowledgeSource.

import json
import logging
import os
from typing import List, Dict, Any, Optional

from .base import KnowledgeSource, RelevantChunk

logger = logging.getLogger(__name__)

class StaticJSONKnowledgeSource(KnowledgeSource):
    """Knowledge source that loads data from a static JSON file."""

    DEFAULT_FILE_PATH = "data/docs/yieldfi_knowledge.json"

    def __init__(self, file_path: Optional[str] = None):
        self._file_path = file_path or self.DEFAULT_FILE_PATH
        self._data: Dict[str, Any] = {}
        self.load_data()

    @property
    def name(self) -> str:
        return f"StaticJSONKnowledgeSource ({os.path.basename(self._file_path)})"

    def load_data(self):
        """Loads data from the JSON file."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            logger.info(f"Successfully loaded knowledge from {self._file_path}")
        except FileNotFoundError:
            logger.error(f"Knowledge file not found: {self._file_path}. {self.name} will operate with empty data.")
            self._data = {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {self._file_path}: {e}. {self.name} will operate with empty data.")
            self._data = {}
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading {self._file_path}: {e}. {self.name} will operate with empty data.")
            self._data = {}

    def _recursive_search(self, query_lower: str, data: Any, path: str) -> List[RelevantChunk]:
        """Recursively searches for query in nested dicts and lists."""
        results = []
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                results.extend(self._recursive_search(query_lower, value, current_path))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                results.extend(self._recursive_search(query_lower, item, current_path))
        elif isinstance(data, str):
            text_lower = data.lower()
            tokens = query_lower.split()
            # Match full phrase or any individual token
            if query_lower in text_lower or any(token in text_lower for token in tokens):
                # Simple scoring: 1.0 for direct match, could be improved
                score = 1.0 
                # Check if it's an answer to an FAQ, if so, prioritize the question as context
                if path.endswith('.answer'):
                    parent_dict = self._data
                    for p_key in path.rsplit('.',1)[0].split('.'):
                        if '[' in p_key: # list index
                            idx = int(p_key[p_key.find('[')+1:p_key.find(']')])
                            if isinstance(parent_dict, list) and idx < len(parent_dict):
                                parent_dict = parent_dict[idx]
                            else:
                                parent_dict = {}
                                break
                        elif isinstance(parent_dict, dict):
                            parent_dict = parent_dict.get(p_key, {})
                        else:
                            parent_dict = {}
                            break
                    question = parent_dict.get('question', '')
                    content = f"Q: {question}\nA: {data}"
                    metadata = {'path': path, 'type': 'faq_answer', 'question': question}
                else:
                    content = data
                    metadata = {'path': path, 'type': 'text_match'}
                
                results.append(RelevantChunk(content=content, source_name=self.name, score=score, metadata=metadata))
        return results

    def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]:
        if not self._data:
            return []
        
        # Prepare tokens for matching
        query_lower = query.lower()
        all_chunks = self._recursive_search(query_lower, self._data, "")
        
        # Sort by score (descending), then by typical relevance (FAQs first)
        all_chunks.sort(key=lambda x: (x.metadata.get('type') == 'faq_answer', x.score), reverse=True)
        return all_chunks[:top_k]


class YieldFiDocsKnowledgeSource(KnowledgeSource):
    """Knowledge source that loads data from YieldFi's Markdown documentation."""

    DEFAULT_FILE_PATH = "data/docs/docs.yield.fi.md" # Placeholder, user to provide actual file

    def __init__(self, file_path: Optional[str] = None):
        self._file_path = file_path or self.DEFAULT_FILE_PATH
        self._paragraphs: List[str] = []
        self.load_data()

    @property
    def name(self) -> str:
        return f"YieldFiDocsKnowledgeSource ({os.path.basename(self._file_path)})"

    def load_data(self):
        """Loads and preprocesses the Markdown document."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Simple paragraph splitting, can be improved (e.g., by section, headers)
            self._paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            if not self._paragraphs:
                 logger.warning(f"No paragraphs found in {self._file_path}. The file might be empty or structured differently.")
            logger.info(f"Successfully loaded and processed {len(self._paragraphs)} paragraphs from {self._file_path}")
        except FileNotFoundError:
            logger.warning(f"Markdown documentation file not found: {self._file_path}. {self.name} will operate with empty data. Please ensure 'data/docs/docs.yield.fi.md' exists or provide the correct path.")
            self._paragraphs = []
        except Exception as e:
            logger.error(f"An unexpected error occurred while loading {self._file_path}: {e}. {self.name} will operate with empty data.")
            self._paragraphs = []

    def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]:
        if not self._paragraphs:
            return []

        query_lower = query.lower()
        tokens = [t for t in query_lower.split() if t]
        relevant_chunks: List[RelevantChunk] = []
        for i, paragraph in enumerate(self._paragraphs):
            paragraph_lower = paragraph.lower()
            # Match full phrase or all individual tokens
            if query_lower in paragraph_lower or all(token in paragraph_lower for token in tokens):
                score = 1.0  # Basic scoring
                metadata = {'paragraph_index': i}
                relevant_chunks.append(
                    RelevantChunk(content=paragraph, source_name=self.name, score=score, metadata=metadata)
                )
        
        # Sort by score (descending)
        relevant_chunks.sort(key=lambda x: x.score, reverse=True)
        return relevant_chunks[:top_k]

# Placeholder for future live data source
# class LiveYieldFiDataSource(KnowledgeSource):
#     @property
#     def name(self) -> str:
#         return "LiveYieldFiDataSource"
# 
#     def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]:
#         # Implementation to fetch live data from YieldFi APIs/subgraphs
#         logger.warning("LiveYieldFiDataSource.search() is not yet implemented.")
#         return []


if __name__ == '__main__':
    # Basic test for StaticJSONKnowledgeSource
    print("--- Testing StaticJSONKnowledgeSource ---")
    json_source = StaticJSONKnowledgeSource()
    if not json_source._data: # Manually create a dummy file if default doesn't exist for testing
        print(f"Default JSON file {StaticJSONKnowledgeSource.DEFAULT_FILE_PATH} not found or empty. Creating a dummy one for testing.")
        dummy_data_path = "data/docs/dummy_knowledge.json"
        try:
            os.makedirs("data/docs", exist_ok=True)
            with open(dummy_data_path, 'w') as df:
                json.dump({"test_key": "This is a test value for searching query", "faq": [{"question": "Dummy Q?", "answer": "Dummy A for query"}]}, df)
            json_source = StaticJSONKnowledgeSource(dummy_data_path) # re-init with dummy
        except Exception as e:
            print(f"Could not create dummy json: {e}")

    queries = ["Optimizer Vault", "risks involved", "YLD token", "nonexistent query", "query"]
    for q in queries:
        print(f"\nSearching for: '{q}'")
        results = json_source.search(q, top_k=3)
        if results:
            for chunk in results:
                print(chunk)
        else:
            print("No results found.")

    # Basic test for YieldFiDocsKnowledgeSource
    print("\n--- Testing YieldFiDocsKnowledgeSource ---")
    # Create a dummy markdown file for testing if docs.yield.fi.md doesn't exist
    dummy_md_path = "data/docs/dummy_docs.yield.fi.md"
    md_source = YieldFiDocsKnowledgeSource(dummy_md_path) # Try with dummy path first
    
    if not md_source._paragraphs: # If dummy is empty or not found, try to create one.
        print(f"Dummy markdown file {dummy_md_path} not found or empty. Creating a dummy one for testing.")
        try:
            os.makedirs("data/docs", exist_ok=True)
            with open(dummy_md_path, 'w', encoding='utf-8') as dmf:
                dmf.write("## Section 1\n\nThis is the first paragraph about YieldFi features.\n\nAnother paragraph in section 1, discussing yield strategies.\n\n## Section 2\n\nThis paragraph talks about security and audits. The query for security should find this.")
            md_source.load_data() # Reload data
        except Exception as e:
            print(f"Could not create dummy markdown: {e}")

    if not md_source._paragraphs and os.path.exists(YieldFiDocsKnowledgeSource.DEFAULT_FILE_PATH):
        print(f"Falling back to default markdown: {YieldFiDocsKnowledgeSource.DEFAULT_FILE_PATH}")
        md_source = YieldFiDocsKnowledgeSource() # Use default if it exists and dummy failed
    
    doc_queries = ["YieldFi features", "security", "nonexistent topic"]
    for q in doc_queries:
        print(f"\nSearching in docs for: '{q}'")
        results = md_source.search(q, top_k=2)
        if results:
            for chunk in results:
                print(chunk)
        else:
            print("No results found.")
    
    # Cleanup dummy files if created
    if os.path.exists("data/docs/dummy_knowledge.json"):
        os.remove("data/docs/dummy_knowledge.json")
    if os.path.exists(dummy_md_path):
        os.remove(dummy_md_path) 
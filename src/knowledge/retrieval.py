# Changelog:
# 2025-05-07 20:35 - Step 11.1 - Created KnowledgeRetriever class.

import logging
from typing import List, Optional, Type

from .base import KnowledgeSource, RelevantChunk
from .yieldfi import StaticJSONKnowledgeSource, YieldFiDocsKnowledgeSource

logger = logging.getLogger(__name__)

class KnowledgeRetriever:
    """Retrieves and ranks knowledge from multiple KnowledgeSource instances."""

    def __init__(self, knowledge_sources: Optional[List[KnowledgeSource]] = None):
        """
        Initializes the KnowledgeRetriever.

        Args:
            knowledge_sources: A list of KnowledgeSource instances. 
                               If None, default sources (StaticJSONKnowledgeSource, 
                               YieldFiDocsKnowledgeSource) will be initialized.
        """
        self.knowledge_sources: List[KnowledgeSource] = []
        if knowledge_sources is not None:
            self.knowledge_sources = knowledge_sources
        else:
            # Initialize default sources if none are provided
            try:
                self.knowledge_sources.append(StaticJSONKnowledgeSource())
                # Ensure data/docs/docs.yield.fi.md exists or YieldFiDocsKnowledgeSource will be empty
                self.knowledge_sources.append(YieldFiDocsKnowledgeSource())
                logger.info(f"Initialized KnowledgeRetriever with default sources: {[s.name for s in self.knowledge_sources]}")
            except Exception as e:
                logger.error(f"Error initializing default knowledge sources: {e}", exc_info=True)
                # Continue with an empty list of sources if defaults fail

    def add_source(self, source: KnowledgeSource):
        """Adds a new knowledge source to the retriever."""
        if not isinstance(source, KnowledgeSource):
            raise TypeError("Source must be an instance of KnowledgeSource.")
        if source not in self.knowledge_sources:
            self.knowledge_sources.append(source)
            logger.info(f"Added knowledge source: {source.name}")
        else:
            logger.warning(f"Knowledge source {source.name} already exists.")

    def retrieve_knowledge(
        self, 
        query: str, 
        top_k_per_source: int = 3, 
        global_top_k: int = 5
    ) -> List[RelevantChunk]:
        """
        Retrieves relevant knowledge chunks from all registered sources.

        Args:
            query: The search query.
            top_k_per_source: Max number of chunks to retrieve from each source.
            global_top_k: Max number of chunks to return globally after ranking.

        Returns:
            A list of RelevantChunk objects, sorted by relevance score (descending).
        """
        if not self.knowledge_sources:
            logger.warning("No knowledge sources registered with the retriever.")
            return []

        all_chunks: List[RelevantChunk] = []
        for source in self.knowledge_sources:
            try:
                chunks = source.search(query, top_k=top_k_per_source)
                all_chunks.extend(chunks)
                logger.debug(f"Retrieved {len(chunks)} chunks from {source.name} for query '{query}'")
            except Exception as e:
                logger.error(f"Error searching in source {source.name}: {e}", exc_info=True)
        
        # Sort all collected chunks by score (descending)
        # Additional tie-breaking can be added if necessary (e.g., source priority)
        all_chunks.sort(key=lambda chunk: chunk.score, reverse=True)
        
        logger.info(f"Retrieved a total of {len(all_chunks)} chunks from {len(self.knowledge_sources)} sources for query '{query}'. Returning top {global_top_k}.")
        return all_chunks[:global_top_k]

    def format_retrieved_knowledge(
        self, 
        chunks: List[RelevantChunk],
        max_length: int = 1500, # Increased default based on common context window needs
        max_chunks_to_format: int = 3 
    ) -> str:
        """
        Formats a list of RelevantChunk objects into a single string for prompt injection.

        Args:
            chunks: A list of RelevantChunk objects, typically sorted by relevance.
            max_length: The maximum character length of the formatted string.
            max_chunks_to_format: The maximum number of chunks to include in the formatted string.

        Returns:
            A formatted string containing concatenated knowledge, or a message if no chunks.
        """
        if not chunks:
            return "No relevant information found in knowledge base for this query."

        formatted_knowledge = """
Relevant Information from Knowledge Base:
"""
        num_formatted = 0
        for chunk in chunks[:max_chunks_to_format]:
            chunk_header = f"\n--- Source: {chunk.source_name} (Score: {chunk.score:.2f}) ---\n"
            chunk_content = chunk.content
            
            # Estimate length before adding
            if len(formatted_knowledge) + len(chunk_header) + len(chunk_content) > max_length:
                remaining_space = max_length - len(formatted_knowledge) - len(chunk_header) - 5 # 5 for ellipsis and newline
                if remaining_space > 20: # Only add if there's meaningful space left
                    chunk_content = chunk_content[:remaining_space] + "..."
                else:
                    logger.warning(f"Skipping chunk from {chunk.source_name} due to max_length. Remaining space too small.")
                    break # Stop if we can't even fit a truncated chunk header + content
            
            formatted_knowledge += chunk_header
            formatted_knowledge += chunk_content
            num_formatted += 1
            if len(formatted_knowledge) >= max_length:
                logger.info(f"Formatted knowledge reached max_length ({max_length}) after {num_formatted} chunks.")
                break
        
        if not formatted_knowledge.strip() or formatted_knowledge.strip() == "Relevant Information from Knowledge Base:":
             return "No relevant information found or able to be formatted within length constraints."

        return formatted_knowledge.strip()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.info("--- Testing KnowledgeRetriever ---")

    # Assuming yieldfi_knowledge.json and potentially docs.yield.fi.md exist as per Step 10
    # If not, the default sources might be empty, which is a valid test case.
    retriever = KnowledgeRetriever() # Uses default sources

    print(f"Retriever initialized with sources: {[s.name for s in retriever.knowledge_sources]}")

    queries_to_test = [
        "YieldMax Optimizer Vault", 
        "risks involved with YieldFi products", 
        "YLD tokenomics", 
        "nonexistent query for testing empty results",
        "security audits"
    ]

    for query in queries_to_test:
        print(f"\n--- Querying for: '{query}' ---")
        retrieved_chunks = retriever.retrieve_knowledge(query, top_k_per_source=2, global_top_k=3)
        
        if retrieved_chunks:
            print(f"Retrieved {len(retrieved_chunks)} chunks globally:")
            for i, r_chunk in enumerate(retrieved_chunks):
                print(f"  {i+1}. Source: {r_chunk.source_name}, Score: {r_chunk.score:.2f}, Path: {r_chunk.metadata.get('path', 'N/A')}")
                print(f"     Content sample: {r_chunk.content[:100].replace('\n', ' ')}...")
            
            formatted_output = retriever.format_retrieved_knowledge(retrieved_chunks, max_length=500, max_chunks_to_format=2)
            print(f"\nFormatted Output (max_length=500, max_chunks=2):\n{formatted_output}")
        else:
            print("No chunks retrieved globally.")
            formatted_output = retriever.format_retrieved_knowledge(retrieved_chunks)
            print(f"Formatted Output for no chunks:\n{formatted_output}")

    # Test adding a source (mock for simplicity here)
    class MockKnowledgeSource(KnowledgeSource):
        @property
        def name(self) -> str: return "MockSource"
        def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]:
            if "mock" in query.lower():
                return [RelevantChunk("This is a mock result for 'mock' query.", self.name, 0.99)]
            return []

    print("\n--- Testing add_source ---")
    mock_source = MockKnowledgeSource()
    retriever.add_source(mock_source)
    print(f"Retriever now has sources: {[s.name for s in retriever.knowledge_sources]}")
    mock_query_chunks = retriever.retrieve_knowledge("mock query", global_top_k=1)
    if mock_query_chunks:
        print(f"Retrieved from mock source: {mock_query_chunks[0].content[:50]}...")
    else:
        print("Did not retrieve from mock source as expected for 'mock query'.")

    print("\n--- Testing with no sources initially ---")
    empty_retriever = KnowledgeRetriever(knowledge_sources=[])
    empty_results = empty_retriever.retrieve_knowledge("any query")
    print(f"Results from empty retriever: {empty_results}")
    formatted_empty = empty_retriever.format_retrieved_knowledge(empty_results)
    print(f"Formatted output from empty retriever: {formatted_empty}") 
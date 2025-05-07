# Changelog:
# 2025-05-07 20:10 - Step 10.1 - Created KnowledgeSource ABC and RelevantChunk dataclass.

import abc
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

@dataclass
class RelevantChunk:
    """Represents a chunk of relevant information retrieved from a knowledge source."""
    content: str
    source_name: str
    score: float = 0.0  # Optional: relevance score
    metadata: Dict[str, Any] = field(default_factory=dict)  # e.g., section_title, document_id

    def __str__(self) -> str:
        return f"Source: {self.source_name}, Score: {self.score:.2f}\nContent: {self.content[:100]}..."

class KnowledgeSource(abc.ABC):
    """Abstract base class for all knowledge sources."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Returns the unique name of the knowledge source."""
        pass

    @abc.abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]:
        """
        Searches the knowledge source for information relevant to the query.

        Args:
            query: The search query string.
            top_k: The maximum number of relevant chunks to return.

        Returns:
            A list of RelevantChunk objects, sorted by relevance (highest first).
        """
        pass

    def load_data(self):
        """
        Optional method to explicitly load or refresh data for the source.
        Not all sources may need this (e.g., API-based sources).
        """
        logger.info(f"Data loading not implemented for {self.name}")
        pass 
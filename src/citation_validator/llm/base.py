"""
Base LLM provider interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response for the given prompt.
        
        Args:
            prompt: The input prompt
            
        Returns:
            Generated response string
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the LLM provider is available and properly configured.
        
        Returns:
            True if available, False otherwise
        """
        pass

"""
LLM provider factory for creating appropriate LLM instances.
"""

import logging

from ..config import config
from .base import LLMProvider
from .openai_provider import OpenAIProvider
from .mock_provider import MockProvider

logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory for creating LLM providers."""

    @staticmethod
    def create_provider() -> LLMProvider:
        """
        Create appropriate LLM provider based on configuration.

        Returns:
            Configured LLM provider instance
        """
        if config.use_mock_llm:
            logger.info("Creating mock LLM provider")
            return MockProvider()

        if config.llm_provider.lower() == "openai":
            logger.info("Creating OpenAI LLM provider")
            return OpenAIProvider(
                api_key=config.openai_api_key,
                model=config.openai_model,
                max_tokens=config.openai_max_tokens,
                temperature=config.openai_temperature,
            )

        # Default to mock if unknown provider
        logger.warning(
            f"Unknown LLM provider: {config.llm_provider}. "
            "Falling back to mock provider."
        )
        return MockProvider()

    @staticmethod
    def get_available_providers() -> list:
        """Get list of available provider names."""
        return ["openai", "mock"]

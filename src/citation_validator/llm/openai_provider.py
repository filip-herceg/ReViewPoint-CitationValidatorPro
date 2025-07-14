"""
OpenAI LLM provider implementation.
"""

import logging
from typing import Optional

from .base import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500,
        temperature: float = 0.3,
    ):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            max_tokens: Maximum tokens in response
            temperature: Temperature setting for generation
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client: Optional[object] = None

        if self.api_key:
            self._initialize_client()

    def _initialize_client(self):
        """Initialize OpenAI client."""
        try:
            import openai

            self._client = openai.OpenAI(api_key=self.api_key)
            logger.info(f"OpenAI client initialized with model {self.model}")
        except ImportError:
            logger.error(
                "OpenAI package not installed. "
                "Install with: pip install openai")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise

    def generate_response(self, prompt: str) -> str:
        """
        Generate response using OpenAI API.

        Args:
            prompt: Input prompt

        Returns:
            Generated response
        """
        if not self.is_available():
            return "❌ **Configuration Error**: OpenAI API not properly " "configured."

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert academic reviewer "
                            "specializing in citation analysis. Provide "
                            "thorough, professional evaluations of "
                            "citation usage."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return f"❌ **API Error**: Could not get LLM response - {str(e)}"

    def is_available(self) -> bool:
        """Check if OpenAI provider is available."""
        return self._client is not None and self.api_key is not None

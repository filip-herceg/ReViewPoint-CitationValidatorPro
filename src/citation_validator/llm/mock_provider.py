"""
Mock LLM provider for testing and development.
"""

import logging
from typing import Dict, Any

from .base import LLMProvider

logger = logging.getLogger(__name__)


class MockProvider(LLMProvider):
    """Mock LLM provider that generates realistic responses for testing."""

    def __init__(self):
        """Initialize mock provider."""
        self.response_templates = {
            "intro_ai": (
                "✅ **Citation Evaluation**: This citation is appropriately "
                "placed in the introduction section. The source provides a "
                "comprehensive review that directly supports the opening "
                "statements about AI development.\n\n"
                "**Strengths:**\n"
                "- Relevant and current source\n"
                "- Supports the broad claims about AI development\n"
                "- Appropriate for establishing context\n\n"
                "**Suggestions for improvement:**\n"
                "- Consider adding specific statistics from the paper\n"
                "- The citation could be more specific about which aspects "
                "are referenced"
            ),
            "background_ai": (
                "⚠️ **Citation Evaluation**: The citation is topically "
                "relevant but the connection could be more explicit. While "
                "the source discusses AI applications, the specific relevance "
                "needs clarification.\n\n"
                "**Concerns:**\n"
                "- The citation may not directly support all examples "
                "mentioned\n"
                "- Consider verifying source coverage of specific applications\n\n"
                "**Recommendations:**\n"
                "- Provide more specific page references\n"
                "- Consider adding sources that directly discuss mentioned "
                "applications"
            ),
            "privacy_technical": (
                "⚠️ **Citation Evaluation**: This citation needs strengthening "
                "for the privacy and technical claims being made. The current "
                "source may not adequately support specific assertions.\n\n"
                "**Issues identified:**\n"
                "- Connection between citation and privacy claims needs "
                "clarification\n"
                "- Technical details require more specific sourcing\n\n"
                "**Improvements needed:**\n"
                "- Add citations focused on enterprise data protection\n"
                "- Include sources on privacy risks in AI tools\n"
                "- Consider academic papers on confidential computing"
            ),
            "default": (
                "❓ **Citation Evaluation**: This citation requires further "
                "review. While the source appears academically sound, the "
                "specific relevance needs clarification.\n\n"
                "**Evaluation criteria:**\n"
                "- **Relevance**: Moderate - source is topically related but "
                "connection needs strengthening\n"
                "- **Accuracy**: Cannot fully assess without specific page "
                "references\n"
                "- **Context**: Citation placement seems appropriate but "
                "could be more precise\n\n"
                "**Recommendations:**\n"
                "- Provide specific page numbers or section references\n"
                "- Consider if additional supporting sources would strengthen "
                "the argument\n"
                "- Ensure citation directly supports all claims in this section"
            ),
        }

    def generate_response(self, prompt: str) -> str:
        """
        Generate mock response based on prompt analysis.

        Args:
            prompt: Input prompt

        Returns:
            Generated mock response
        """
        logger.info("Generating mock LLM response")

        prompt_lower = prompt.lower()

        # Determine response type based on prompt content
        if self._is_intro_ai_content(prompt_lower):
            return self.response_templates["intro_ai"]
        elif self._is_background_ai_content(prompt_lower):
            return self.response_templates["background_ai"]
        elif self._is_privacy_technical_content(prompt_lower):
            return self.response_templates["privacy_technical"]
        else:
            return self.response_templates["default"]

    def is_available(self) -> bool:
        """Mock provider is always available."""
        return True

    def _is_intro_ai_content(self, prompt: str) -> bool:
        """Check if prompt is for intro AI content."""
        intro_keywords = ["einleitung", "introduction"]
        ai_keywords = ["ai", "künstliche intelligenz", "chatbot", "code completion"]

        has_intro = any(keyword in prompt for keyword in intro_keywords)
        has_ai = any(keyword in prompt for keyword in ai_keywords)

        return has_intro and has_ai

    def _is_background_ai_content(self, prompt: str) -> bool:
        """Check if prompt is for background AI content."""
        background_keywords = ["hintergrund", "background"]
        ai_keywords = ["ai", "künstliche intelligenz", "chatbot"]

        has_background = any(keyword in prompt for keyword in background_keywords)
        has_ai = any(keyword in prompt for keyword in ai_keywords)

        return has_background and has_ai

    def _is_privacy_technical_content(self, prompt: str) -> bool:
        """Check if prompt is for privacy/technical content."""
        privacy_keywords = ["datenschutz", "privacy", "sicherheit", "security"]
        technical_keywords = ["system", "modell", "implementierung", "plattform"]

        has_privacy = any(keyword in prompt for keyword in privacy_keywords)
        has_technical = any(keyword in prompt for keyword in technical_keywords)

        return has_privacy or has_technical

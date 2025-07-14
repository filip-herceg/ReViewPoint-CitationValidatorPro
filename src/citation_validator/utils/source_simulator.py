"""
Source content simulation for simplified mode.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SourceContentSimulator:
    """Simulates source content extraction for simplified mode."""

    def __init__(self):
        """Initialize the simulator with predefined content categories."""
        self.simulated_sources = {
            "ai_research": [
                ("This paper presents a comprehensive survey of artificial "
                 "intelligence applications in various domains."),
                ("The study demonstrates significant improvements in AI model "
                 "performance across multiple benchmarks."),
                ("Recent advances in neural network architectures have led to "
                 "breakthrough results in natural language processing."),
                ("The research discusses ethical implications of AI deployment "
                 "in enterprise environments."),
                ("Experimental results show promising applications of AI in "
                 "automated software development."),
            ],
            "code_completion": [
                ("Code completion systems have revolutionized the software "
                 "development workflow by providing intelligent suggestions."),
                ("The study evaluates the effectiveness of various code "
                 "completion algorithms in real-world development scenarios."),
                ("Machine learning models trained on large codebases show "
                 "significant improvement in code prediction accuracy."),
                ("Integration of code completion tools in IDEs has led to "
                 "measurable productivity gains for developers."),
                ("The research addresses challenges in code completion for "
                 "domain-specific programming languages."),
            ],
            "privacy_security": [
                ("Enterprise data protection requirements necessitate careful "
                 "consideration of AI model deployment strategies."),
                ("The paper discusses privacy-preserving techniques for "
                 "machine learning in sensitive enterprise environments."),
                ("Confidential computing approaches enable secure AI "
                 "processing without exposing sensitive data."),
                ("The study presents frameworks for evaluating privacy risks "
                 "in AI-powered development tools."),
                ("Research findings indicate the importance of on-premises AI "
                 "solutions for highly regulated industries."),
            ],
        }

    def simulate_source_content(self, citation: Dict[str, Any]) -> str:
        """
        Simulate extracted content from a source based on citation metadata.

        Args:
            citation: Citation metadata dictionary

        Returns:
            Simulated source content string
        """
        logger.debug(
            f"Simulating content for citation: " f"{
                citation.get(
                    'title',
                    'Unknown')}")

        # Classify the citation based on title and keywords
        source_category = self._classify_citation(citation)

        # Select content based on hash for consistency
        content_list = self.simulated_sources[source_category]
        content_index = hash(
            citation.get(
                "doi",
                citation.get(
                    "title",
                    ""))) % len(content_list)

        return content_list[content_index]

    def _classify_citation(self, citation: Dict[str, Any]) -> str:
        """
        Classify citation into content category.

        Args:
            citation: Citation metadata

        Returns:
            Category name
        """
        title = citation.get("title", "").lower()
        citation.get("citation", "").lower()

        # Check for AI research keywords
        ai_keywords = [
            "chatbot",
            "conversational",
            "ai",
            "artificial intelligence"]
        if any(keyword in title for keyword in ai_keywords):
            return "ai_research"

        # Check for code completion keywords
        code_keywords = ["code", "completion", "development", "programming"]
        if any(keyword in title for keyword in code_keywords):
            return "code_completion"

        # Check for privacy/security keywords
        privacy_keywords = [
            "privacy",
            "security",
            "data protection",
            "enterprise"]
        if any(keyword in title for keyword in privacy_keywords):
            return "privacy_security"

        # Default to AI research
        return "ai_research"

    def get_available_categories(self) -> list:
        """Get list of available content categories."""
        return list(self.simulated_sources.keys())

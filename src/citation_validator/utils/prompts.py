"""
Prompt templates for LLM citation evaluation.
"""

import json
from typing import Dict, Any, Optional


class PromptTemplate:
    """Handles creation of LLM prompts for citation evaluation."""
    
    @staticmethod
    def create_citation_evaluation_prompt(
        div_text: str,
        citation_metadata: Dict[str, Any],
        source_content: Optional[str] = None,
        use_simplified_mode: bool = True
    ) -> str:
        """
        Create the prompt for LLM evaluation.
        
        Args:
            div_text: Text excerpt containing the citation
            citation_metadata: Citation metadata dictionary
            source_content: Optional simulated or actual source content
            use_simplified_mode: Whether using simplified mode
            
        Returns:
            Formatted prompt string
        """
        base_prompt = f"""You are an expert academic reviewer specializing in citation analysis. Your task is to evaluate whether a citation is correctly used, relevant, and truthful based on the text excerpt and citation metadata provided.

--- Text Excerpt ---
{div_text}
--- End of Excerpt ---

--- Citation Metadata ---
{json.dumps(citation_metadata, indent=2, ensure_ascii=False)}
--- End of Citation Metadata ---"""

        if use_simplified_mode and source_content:
            base_prompt += f"""

--- Simulated Source Content ---
{source_content}
--- End of Source Content ---

Note: In simplified mode, the source content above is simulated based on the citation metadata. In full mode, this would be actual extracted content from the original paper."""

        evaluation_instructions = """

Please provide a thorough evaluation focusing on:

1. **Relevance**: How well does the citation support the claims made in the text excerpt?
2. **Accuracy**: Does the way the source is represented align with the citation metadata?
3. **Context**: Is the citation appropriately placed and used within the argument structure?
4. **Potential Issues**: Identify any misinterpretations, overgeneralizations, or misrepresentations.
5. **Improvement Suggestions**: Provide specific recommendations if the citation usage could be enhanced.

Format your response with clear sections and provide actionable feedback. Use emojis to categorize your evaluation:
- ✅ for well-used citations
- ⚠️ for citations that need improvement
- ❌ for problematic citations
- 💡 for helpful suggestions

Keep your response professional, concise but thorough (aim for 150-300 words)."""

        return base_prompt + evaluation_instructions
    
    @staticmethod
    def create_system_prompt() -> str:
        """
        Create system prompt for LLM.
        
        Returns:
            System prompt string
        """
        return ("You are an expert academic reviewer specializing in "
                "citation analysis. Provide thorough, professional "
                "evaluations of citation usage.")
    
    @staticmethod
    def create_missing_citation_response(footnote_id: int) -> str:
        """
        Create response for missing citation metadata.
        
        Args:
            footnote_id: ID of the missing footnote
            
        Returns:
            Error message string
        """
        return (f"⚠️ **Missing Citation**: No citation metadata found for "
                f"footnote {footnote_id}.")
    
    @staticmethod
    def create_empty_content_response(footnote_id: int) -> str:
        """
        Create response for empty div content.
        
        Args:
            footnote_id: ID of the empty footnote
            
        Returns:
            Warning message string
        """
        return (f"⚠️ **Empty Content**: Div {footnote_id} has no text "
                f"content to evaluate.")
    
    @staticmethod
    def create_configuration_error_response() -> str:
        """
        Create response for configuration errors.
        
        Returns:
            Error message string
        """
        return ("❌ **Configuration Error**: LLM provider not properly "
                "configured. Please check your settings.")

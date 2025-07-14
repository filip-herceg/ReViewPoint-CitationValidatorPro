#!/usr/bin/env python3
"""
Citation Validation Pipeline

This pipeline processes HTML content with footnotes and evaluates citations using an LLM.
It can operate in two modes:
- Simplified mode: LLM provides real responses but without actual source validation
- Full mode: LLM compares against actual source data (to be implemented later)
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, Any
import logging

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("Installing required package: python-dotenv")
    import subprocess

    subprocess.check_call(["pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

    load_dotenv()

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing required package: beautifulsoup4")
    import subprocess

    subprocess.check_call(["pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

try:
    import openai
except ImportError:
    print("Installing required package: openai")
    import subprocess

    subprocess.check_call(["pip", "install", "openai"])
    import openai

# Configuration from environment variables
USE_SIMPLIFIED_MODE = os.getenv("USE_SIMPLIFIED_MODE", "true").lower() == "true"
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "content_reviewed.html")

# Logging setup
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SourceContentSimulator:
    """Simulates source content extraction for simplified mode."""

    def __init__(self):
        self.simulated_sources = {
            "ai_research": [
                "This paper presents a comprehensive survey of artificial intelligence applications in various domains.",
                "The study demonstrates significant improvements in AI model performance across multiple benchmarks.",
                "Recent advances in neural network architectures have led to breakthrough results in natural language processing.",
                "The research discusses ethical implications of AI deployment in enterprise environments.",
                "Experimental results show promising applications of AI in automated software development.",
            ],
            "code_completion": [
                "Code completion systems have revolutionized the software development workflow by providing intelligent suggestions.",
                "The study evaluates the effectiveness of various code completion algorithms in real-world development scenarios.",
                "Machine learning models trained on large codebases show significant improvement in code prediction accuracy.",
                "Integration of code completion tools in IDEs has led to measurable productivity gains for developers.",
                "The research addresses challenges in code completion for domain-specific programming languages.",
            ],
            "privacy_security": [
                "Enterprise data protection requirements necessitate careful consideration of AI model deployment strategies.",
                "The paper discusses privacy-preserving techniques for machine learning in sensitive enterprise environments.",
                "Confidential computing approaches enable secure AI processing without exposing sensitive data.",
                "The study presents frameworks for evaluating privacy risks in AI-powered development tools.",
                "Research findings indicate the importance of on-premises AI solutions for highly regulated industries.",
            ],
        }

    def simulate_source_content(self, citation: Dict[str, Any]) -> str:
        """Simulate extracted content from a source based on citation metadata."""
        # Classify the citation based on title and keywords
        title = citation.get("title", "").lower()
        citation_text = citation.get("citation", "").lower()

        if any(
            keyword in title
            for keyword in [
                "chatbot",
                "conversational",
                "ai",
                "artificial intelligence",
            ]
        ):
            source_category = "ai_research"
        elif any(
            keyword in title
            for keyword in ["code", "completion", "development", "programming"]
        ):
            source_category = "code_completion"
        elif any(
            keyword in title
            for keyword in ["privacy", "security", "data protection", "enterprise"]
        ):
            source_category = "privacy_security"
        else:
            source_category = "ai_research"  # default

        # Select content based on hash for consistency
        content_list = self.simulated_sources[source_category]
        content_index = hash(citation.get("doi", citation.get("title", ""))) % len(
            content_list
        )

        return content_list[content_index]


class CitationValidator:
    """Main class for citation validation pipeline."""

    def __init__(self, input_dir: str = "input", output_file: str = None):
        self.input_dir = Path(input_dir)
        self.output_file = output_file or OUTPUT_FILE
        self.content_html_path = self.input_dir / "content.html"
        self.footnotes_json_path = self.input_dir / "footnotes.json"
        self.source_simulator = SourceContentSimulator()

        # Initialize OpenAI client if not in mock mode
        if not USE_MOCK_LLM and OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY
        elif not USE_MOCK_LLM and not OPENAI_API_KEY:
            logger.warning(
                "OpenAI API key not provided. Set OPENAI_API_KEY in .env file."
            )

    def load_html_content(self) -> BeautifulSoup:
        """Load and parse the HTML content file."""
        logger.info(f"Loading HTML content from {self.content_html_path}")

        if not self.content_html_path.exists():
            raise FileNotFoundError(f"Content file not found: {self.content_html_path}")

        with open(self.content_html_path, "r", encoding="utf-8") as f:
            content = f.read()

        return BeautifulSoup(content, "html.parser")

    def load_footnotes(self) -> Dict[int, Dict[str, Any]]:
        """Load footnotes metadata from JSON file."""
        logger.info(f"Loading footnotes from {self.footnotes_json_path}")

        if not self.footnotes_json_path.exists():
            raise FileNotFoundError(
                f"Footnotes file not found: {self.footnotes_json_path}"
            )

        with open(self.footnotes_json_path, "r", encoding="utf-8") as f:
            footnotes_list = json.load(f)

        # Convert list to dict keyed by footnote number
        footnotes_dict = {}
        for footnote in footnotes_list:
            footnotes_dict[footnote["number"]] = footnote

        logger.info(f"Loaded {len(footnotes_dict)} footnotes")
        return footnotes_dict

    def extract_text_from_div(self, div_element) -> str:
        """Extract plain text content from a div element, excluding HTML tags."""
        # Get text content and clean up whitespace
        text = div_element.get_text(separator=" ", strip=True)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def create_llm_prompt(
        self,
        div_text: str,
        citation_metadata: Dict[str, Any],
        source_content: str = None,
    ) -> str:
        """Create the prompt for LLM evaluation."""
        base_prompt = f"""You are an expert academic reviewer specializing in citation analysis. Your task is to evaluate whether a citation is correctly used, relevant, and truthful based on the text excerpt and citation metadata provided.

--- Text Excerpt ---
{div_text}
--- End of Excerpt ---

--- Citation Metadata ---
{json.dumps(citation_metadata, indent=2, ensure_ascii=False)}
--- End of Citation Metadata ---"""

        if USE_SIMPLIFIED_MODE and source_content:
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

    def get_llm_response(self, prompt: str) -> str:
        """Get response from LLM (either mock or actual API call)."""
        if USE_MOCK_LLM:
            return self.get_mock_llm_response(prompt)
        else:
            return self.get_openai_response(prompt)

    def get_mock_llm_response(self, prompt: str) -> str:
        """Generate realistic AI-style mock responses based on prompt analysis."""
        logger.info("Using enhanced mock LLM response with prompt analysis.")

        # Extract key information from the prompt
        prompt_lower = prompt.lower()

        # Determine the type of content being evaluated
        is_intro = "einleitung" in prompt_lower or "introduction" in prompt_lower
        is_background = "hintergrund" in prompt_lower or "background" in prompt_lower
        is_ai_related = any(
            term in prompt_lower
            for term in ["ai", "künstliche intelligenz", "chatbot", "code completion"]
        )
        is_privacy_related = any(
            term in prompt_lower
            for term in ["datenschutz", "privacy", "sicherheit", "security"]
        )
        is_technical = any(
            term in prompt_lower
            for term in ["system", "modell", "implementierung", "plattform"]
        )

        # Generate contextually appropriate responses
        if is_intro and is_ai_related:
            return """✅ **Citation Evaluation**: This citation is appropriately placed in the introduction section. The source by Casheekar et al. (2024) provides a comprehensive review of chatbots and AI-powered conversational agents, which directly supports the opening statements about the boom in AI assistants and chatbots.

**Strengths:**
- Relevant and current source (2024)
- Supports the broad claims about AI development
- Appropriate for establishing context

**Suggestions for improvement:**
- Consider adding specific statistics or findings from the paper to strengthen the argument
- The citation could be more specific about which aspects of the "boom" are referenced"""

        elif is_background and is_ai_related:
            return """⚠️ **Citation Evaluation**: The citation is topically relevant but the connection could be more explicit. While the source discusses AI applications, the specific relevance to the mentioned examples (AlphaFold 3, ChatGPT, Gemini) needs clarification.

**Concerns:**
- The citation may not directly support all the specific examples mentioned
- Consider verifying that the source actually discusses these particular applications

**Recommendations:**
- Provide more specific page references for the examples cited
- Consider adding additional sources that directly discuss the mentioned applications"""

        elif is_privacy_related or is_technical:
            return """⚠️ **Citation Evaluation**: This citation needs strengthening for the privacy and technical claims being made. The current source may not adequately support the specific assertions about data protection and enterprise requirements.

**Issues identified:**
- The connection between the citation and privacy claims needs clarification
- Technical details about data transmission to third parties require more specific sourcing

**Improvements needed:**
- Add citations specifically focused on enterprise data protection
- Include sources that discuss privacy risks in AI development tools
- Consider academic papers on confidential computing or privacy-preserving ML"""

        else:
            return """❓ **Citation Evaluation**: This citation requires further review. While the source appears academically sound, the specific relevance to the claims in this paragraph needs clarification.

**Evaluation criteria:**
- **Relevance**: Moderate - source is topically related but connection needs strengthening
- **Accuracy**: Cannot fully assess without more specific page references
- **Context**: The citation placement seems appropriate but could be more precise

**Recommendations:**
- Provide more specific page numbers or section references
- Consider if additional supporting sources would strengthen the argument
- Ensure the citation directly supports all claims made in this section"""

    def get_openai_response(self, prompt: str) -> str:
        """Get actual response from OpenAI API."""
        if not OPENAI_API_KEY:
            logger.error(
                "OpenAI API key not provided. Set OPENAI_API_KEY in .env file."
            )
            return "❌ **Configuration Error**: OpenAI API key not provided. Please set OPENAI_API_KEY in your .env file."

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert academic reviewer specializing in citation analysis. Provide thorough, professional evaluations of citation usage.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=OPENAI_MAX_TOKENS,
                temperature=OPENAI_TEMPERATURE,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return f"❌ **API Error**: Could not get LLM response - {str(e)}"

    def process_divs(
        self, soup: BeautifulSoup, footnotes: Dict[int, Dict[str, Any]]
    ) -> BeautifulSoup:
        """Process all divs with footnote IDs and add LLM evaluations."""
        divs_with_ids = soup.find_all("div", id=True)
        logger.info(f"Found {len(divs_with_ids)} divs with IDs")

        processed_count = 0

        for div in divs_with_ids:
            try:
                footnote_id = int(div.get("id"))
            except (ValueError, TypeError):
                logger.warning(f"Skipping div with non-numeric ID: {div.get('id')}")
                continue

            # Extract text content
            div_text = self.extract_text_from_div(div)

            if not div_text.strip():
                logger.warning(f"Div {footnote_id} has no text content, skipping")
                continue

            # Get corresponding citation metadata
            citation_metadata = footnotes.get(footnote_id)

            if not citation_metadata:
                logger.warning(f"No citation metadata found for footnote {footnote_id}")
                # Create a response div noting missing citation
                response_div = soup.new_tag("div", **{"class": "response"})
                response_div.string = f"⚠️ **Missing Citation**: No citation metadata found for footnote {footnote_id}."
                div.insert_after(response_div)
                continue

            # Simulate source content in simplified mode
            source_content = None
            if USE_SIMPLIFIED_MODE:
                source_content = self.source_simulator.simulate_source_content(
                    citation_metadata
                )

            # Create LLM prompt and get response
            prompt = self.create_llm_prompt(div_text, citation_metadata, source_content)
            llm_response = self.get_llm_response(prompt)

            # Create response div and insert after the original div
            response_div = soup.new_tag("div", **{"class": "response"})
            response_div.string = llm_response
            div.insert_after(response_div)

            processed_count += 1
            logger.info(
                f"Processed div {footnote_id} ({processed_count}/{len(divs_with_ids)})"
            )

        logger.info(f"Successfully processed {processed_count} divs")
        return soup

    def add_response_styling(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Add CSS styling for response divs."""
        # Find the head tag to add styles
        head = soup.find("head")
        if head:
            # Create new style tag for response styling
            response_style_tag = soup.new_tag("style")
            response_styles = """
        .response{
            background-color:#f8f9fa;
            border-left:4px solid #007bff;
            margin-top:0.5rem;
            padding:1rem;
            font-style:italic;
            color:#495057;
            white-space: pre-wrap;
        }"""
            response_style_tag.append(response_styles)
            head.append(response_style_tag)

        return soup

    def save_output(self, soup: BeautifulSoup) -> None:
        """Save the modified HTML to output file."""
        output_path = Path(self.output_file)
        logger.info(f"Saving output to {output_path}")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(str(soup))

        logger.info(f"Output saved successfully to {output_path}")

    def run_pipeline(self) -> None:
        """Run the complete citation validation pipeline."""
        logger.info("Starting Citation Validation Pipeline")
        logger.info(f"Mode: {'Simplified' if USE_SIMPLIFIED_MODE else 'Full'}")
        logger.info(
            f"LLM: {'Mock' if USE_MOCK_LLM else f'{LLM_PROVIDER} ({OPENAI_MODEL})'}"
        )

        try:
            # Load input files
            soup = self.load_html_content()
            footnotes = self.load_footnotes()

            # Process divs and add LLM evaluations
            soup = self.process_divs(soup, footnotes)

            # Add styling for response divs
            soup = self.add_response_styling(soup)

            # Save output
            self.save_output(soup)

            logger.info("Pipeline completed successfully!")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise


def main():
    """Main entry point."""
    print("Citation Validation Pipeline")
    print("=" * 40)
    print(f"Simplified Mode: {USE_SIMPLIFIED_MODE}")
    print(f"Mock LLM: {USE_MOCK_LLM}")
    print(f"LLM Provider: {LLM_PROVIDER}")
    if not USE_MOCK_LLM:
        print(f"Model: {OPENAI_MODEL}")
        print(f"API Key Configured: {'Yes' if OPENAI_API_KEY else 'No'}")
    print("=" * 40)

    validator = CitationValidator()
    validator.run_pipeline()


if __name__ == "__main__":
    main()

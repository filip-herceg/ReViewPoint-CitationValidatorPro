"""
Core citation validator implementation.
"""

import logging
from pathlib import Path
from typing import Dict, Any

from .config import config
from .llm.factory import LLMFactory
from .processors.html_processor import HTMLProcessor
from .processors.citation_processor import CitationDataProcessor
from .utils.source_simulator import SourceContentSimulator
from .utils.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class CitationValidator:
    """Main class for citation validation pipeline."""

    def __init__(self, input_dir: str = None, output_file: str = None):
        """
        Initialize citation validator.

        Args:
            input_dir: Directory containing input files
            output_file: Output HTML file path
        """
        self.input_dir = input_dir or config.input_dir
        self.output_file = output_file or config.output_file

        # If output_file doesn't have a directory, use the output_dir config
        output_path = Path(self.output_file)
        if not output_path.parent or output_path.parent == Path("."):
            self.output_file = str(Path(config.output_dir) / self.output_file)

        # Initialize processors
        self.html_processor = HTMLProcessor(self.input_dir)
        self.citation_processor = CitationDataProcessor(self.input_dir)
        self.source_simulator = SourceContentSimulator()
        self.prompt_template = PromptTemplate()

        # Initialize LLM provider
        self.llm_provider = LLMFactory.create_provider()

        logger.info(
            f"CitationValidator initialized with input_dir: "
            f"{self.input_dir}, output_file: {self.output_file}"
        )

    def run_pipeline(self) -> None:
        """Run the complete citation validation pipeline."""
        logger.info("Starting Citation Validation Pipeline")

        # Log configuration summary
        config_summary = config.get_summary()
        for key, value in config_summary.items():
            logger.info(f"{key}: {value}")

        try:
            # Validate configuration
            if not config.validate():
                raise ValueError("Invalid configuration")

            # Load input files
            soup = self.html_processor.load_html_content()
            footnotes = self.citation_processor.load_footnotes()

            # Process divs and add LLM evaluations
            soup = self._process_divs(soup, footnotes)

            # Add styling for response divs
            soup = self.html_processor.add_response_styling(soup)

            # Save output
            self.html_processor.save_html(soup, self.output_file)

            logger.info("Pipeline completed successfully!")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

    def _process_divs(self, soup, footnotes: Dict[int, Dict[str, Any]]):
        """
        Process all divs with footnote IDs and add LLM evaluations.

        Args:
            soup: BeautifulSoup object
            footnotes: Footnotes metadata dictionary

        Returns:
            Modified BeautifulSoup object
        """
        valid_divs = self.html_processor.find_divs_with_footnote_ids(soup)
        logger.info(f"Processing {len(valid_divs)} divs with footnote IDs")

        processed_count = 0

        for div, footnote_id in valid_divs:
            try:
                # Extract text content
                div_text = self.html_processor.extract_text_from_div(div)

                if not div_text.strip():
                    logger.warning(
                        f"Div {footnote_id} has no text content, skipping")
                    response_content = (
                        self.prompt_template.create_empty_content_response(footnote_id))
                    self.html_processor.add_response_div(
                        soup, div, response_content)
                    continue

                # Get corresponding citation metadata
                citation_metadata = footnotes.get(footnote_id)

                if not citation_metadata:
                    logger.warning(
                        f"No citation metadata found for footnote {footnote_id}")
                    response_content = (
                        self.prompt_template.create_missing_citation_response(
                            footnote_id
                        )
                    )
                    self.html_processor.add_response_div(
                        soup, div, response_content)
                    continue

                # Validate citation metadata
                if not self.citation_processor.validate_footnote(
                        citation_metadata):
                    logger.warning(
                        f"Invalid citation metadata for footnote {footnote_id}"
                    )
                    continue

                # Generate LLM response
                response_content = self._generate_citation_evaluation(
                    div_text, citation_metadata
                )

                # Add response div
                self.html_processor.add_response_div(
                    soup, div, response_content)

                processed_count += 1
                logger.info(
                    f"Processed div {footnote_id} "
                    f"({processed_count}/{len(valid_divs)})"
                )

            except Exception as e:
                logger.error(f"Error processing div {footnote_id}: {e}")
                response_content = (
                    f"❌ **Processing Error**: "
                    f"Failed to process footnote {footnote_id} "
                    f"- {str(e)}"
                )
                self.html_processor.add_response_div(
                    soup, div, response_content)

        logger.info(f"Successfully processed {processed_count} divs")
        return soup

    def _generate_citation_evaluation(
        self, div_text: str, citation_metadata: Dict[str, Any]
    ) -> str:
        """
        Generate LLM evaluation for a citation.

        Args:
            div_text: Text content of the div
            citation_metadata: Citation metadata

        Returns:
            LLM response string
        """
        # Simulate source content in simplified mode
        source_content = None
        if config.use_simplified_mode:
            source_content = self.source_simulator.simulate_source_content(
                citation_metadata
            )

        # Create LLM prompt
        prompt = self.prompt_template.create_citation_evaluation_prompt(
            div_text=div_text,
            citation_metadata=citation_metadata,
            source_content=source_content,
            use_simplified_mode=config.use_simplified_mode,
        )

        # Get LLM response
        try:
            response = self.llm_provider.generate_response(prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return f"❌ **LLM Error**: Failed to generate response - " f"{
                str(e)}"

    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of validation configuration and status.

        Returns:
            Summary dictionary
        """
        return {
            "input_dir": str(self.input_dir),
            "output_file": str(self.output_file),
            "llm_available": self.llm_provider.is_available(),
            "config": config.get_summary(),
        }

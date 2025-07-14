"""
Citation data processing utilities.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class CitationDataProcessor:
    """Handles loading and processing of citation metadata."""

    def __init__(self, input_dir: str = "input"):
        """
        Initialize citation data processor.

        Args:
            input_dir: Directory containing input files
        """
        self.input_dir = Path(input_dir)
        self.footnotes_json_path = self.input_dir / "footnotes.json"

    def load_footnotes(self) -> Dict[int, Dict[str, Any]]:
        """
        Load footnotes metadata from JSON file.

        Returns:
            Dictionary mapping footnote numbers to metadata

        Raises:
            FileNotFoundError: If footnotes file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        logger.info(f"Loading footnotes from {self.footnotes_json_path}")

        if not self.footnotes_json_path.exists():
            raise FileNotFoundError(
                f"Footnotes file not found: {self.footnotes_json_path}"
            )

        try:
            with open(self.footnotes_json_path, "r", encoding="utf-8") as f:
                footnotes_list = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in footnotes file: {e}")
            raise

        # Convert list to dict keyed by footnote number
        footnotes_dict = {}
        for footnote in footnotes_list:
            if "number" in footnote:
                footnotes_dict[footnote["number"]] = footnote
            else:
                logger.warning("Footnote missing 'number' field, skipping")

        logger.info(f"Loaded {len(footnotes_dict)} footnotes")
        return footnotes_dict

    def validate_footnote(self, footnote: Dict[str, Any]) -> bool:
        """
        Validate that a footnote has required fields.

        Args:
            footnote: Footnote metadata dictionary

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["number"]
        optional_fields = ["title", "citation", "doi", "authors", "year"]

        # Check required fields
        for field in required_fields:
            if field not in footnote:
                logger.warning(f"Footnote missing required field: {field}")
                return False

        # Log available optional fields
        available_optional = [
            field for field in optional_fields if field in footnote]
        logger.debug(
            f"Footnote {footnote['number']} has optional fields: "
            f"{available_optional}"
        )

        return True

    def get_footnote_summary(self, footnote: Dict[str, Any]) -> str:
        """
        Get a summary string for a footnote.

        Args:
            footnote: Footnote metadata

        Returns:
            Summary string
        """
        title = footnote.get("title", "Unknown Title")
        authors = footnote.get("authors", "Unknown Authors")
        year = footnote.get("year", "Unknown Year")

        return f"{authors} ({year}): {title}"

    def export_footnotes(
        self, footnotes: Dict[int, Dict[str, Any]], output_path: str
    ) -> None:
        """
        Export footnotes to JSON file.

        Args:
            footnotes: Footnotes dictionary
            output_path: Path to save the file
        """
        # Convert back to list format
        footnotes_list = list(footnotes.values())

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(footnotes_list, f, ensure_ascii=False, indent=2)

        logger.info(f"Footnotes exported to {output_path}")

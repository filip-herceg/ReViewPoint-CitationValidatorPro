"""
Tests for Citation Validator core functionality.
"""

import pytest
from unittest.mock import patch, MagicMock

from citation_validator.core import CitationValidator
from citation_validator.config import config


class TestCitationValidator:
    """Test CitationValidator class."""

    def test_initialization(self, temp_input_dir):
        """Test validator initialization."""
        validator = CitationValidator(
            input_dir=temp_input_dir, output_file="test_output.html"
        )

        assert validator.input_dir == temp_input_dir
        assert validator.output_file == "test_output.html"
        assert validator.llm_provider is not None

    @patch("citation_validator.config.config.use_mock_llm", True)
    def test_pipeline_with_mock_llm(self, temp_input_dir):
        """Test pipeline execution with mock LLM."""
        validator = CitationValidator(
            input_dir=temp_input_dir, output_file="test_output.html"
        )

        # Should not raise exception
        validator.run_pipeline()

        # Check output file exists
        from pathlib import Path

        assert Path("test_output.html").exists()

    def test_validation_summary(self, temp_input_dir):
        """Test validation summary generation."""
        validator = CitationValidator(input_dir=temp_input_dir)
        summary = validator.get_validation_summary()

        assert "input_dir" in summary
        assert "output_file" in summary
        assert "llm_available" in summary
        assert "config" in summary

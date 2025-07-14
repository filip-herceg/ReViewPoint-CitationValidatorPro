"""
Configuration module for Citation Validator.

Handles environment variables, settings validation, and configuration management.
"""

import os
from pathlib import Path
from typing import Optional
import logging

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # Optional dependency


class Config:
    """Configuration management for Citation Validator."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Optional path to configuration file
        """
        if config_file:
            self._load_config_file(config_file)

        self._setup_logging()

    # Mode settings
    @property
    def use_simplified_mode(self) -> bool:
        """Whether to use simplified mode (simulated sources)."""
        return os.getenv("USE_SIMPLIFIED_MODE", "true").lower() == "true"

    @property
    def use_mock_llm(self) -> bool:
        """Whether to use mock LLM responses for testing."""
        return os.getenv("USE_MOCK_LLM", "false").lower() == "true"

    # LLM Provider settings
    @property
    def llm_provider(self) -> str:
        """LLM provider to use."""
        return os.getenv("LLM_PROVIDER", "openai")

    @property
    def openai_api_key(self) -> Optional[str]:
        """OpenAI API key."""
        return os.getenv("OPENAI_API_KEY")

    @property
    def openai_model(self) -> str:
        """OpenAI model to use."""
        return os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    @property
    def openai_max_tokens(self) -> int:
        """Maximum tokens for OpenAI responses."""
        return int(os.getenv("OPENAI_MAX_TOKENS", "500"))

    @property
    def openai_temperature(self) -> float:
        """Temperature setting for OpenAI model."""
        return float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

    # File paths
    @property
    def input_dir(self) -> str:
        """Input directory path."""
        return os.getenv("INPUT_DIR", "input")

    @property
    def output_dir(self) -> str:
        """Output directory path."""
        return os.getenv("OUTPUT_DIR", "output")

    @property
    def output_file(self) -> str:
        """Output file path."""
        return os.getenv("OUTPUT_FILE", "content_reviewed.html")

    # Logging
    @property
    def log_level(self) -> str:
        """Logging level."""
        return os.getenv("LOG_LEVEL", "INFO")

    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def _load_config_file(self, config_file: str):
        """Load configuration from file."""
        config_path = Path(config_file)
        if config_path.exists():
            # Load dotenv from specific file
            from dotenv import load_dotenv

            load_dotenv(config_path)

    def validate(self) -> bool:
        """
        Validate configuration settings.

        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.use_mock_llm and self.llm_provider == "openai":
            if not self.openai_api_key:
                logging.warning(
                    "OpenAI API key not provided but required for non-mock mode"
                )
                return False

        # Validate input directory exists
        if not Path(self.input_dir).exists():
            logging.error(f"Input directory does not exist: {self.input_dir}")
            return False

        # Create output directory if it doesn't exist
        try:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            logging.info(f"Output directory ready: {self.output_dir}")
        except Exception as e:
            logging.error(
                f"Cannot create output directory {
                    self.output_dir}: {e}")
            return False

        return True

    def get_summary(self) -> dict:
        """Get a summary of current configuration."""
        return {
            "mode": "Simplified" if self.use_simplified_mode else "Full",
            "llm": (
                "Mock"
                if self.use_mock_llm
                else f"{self.llm_provider} ({self.openai_model})"
            ),
            "input_dir": self.input_dir,
            "output_dir": self.output_dir,
            "output_file": self.output_file,
            "log_level": self.log_level,
            "api_key_configured": (
                bool(self.openai_api_key) if not self.use_mock_llm else "N/A"
            ),
        }


# Global config instance
config = Config()

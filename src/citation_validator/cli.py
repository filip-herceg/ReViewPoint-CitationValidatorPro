"""
Command-line interface for Citation Validator.
"""

import argparse
import sys
import logging
from pathlib import Path

from .core import CitationValidator
from .config import config

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Citation Validation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input-dir input --output content_reviewed.html
  %(prog)s --mock-llm --simplified-mode
  %(prog)s --config .env.production
        """,
    )

    parser.add_argument(
        "--input-dir",
        default=config.input_dir,
        help="Input directory containing content.html and footnotes.json",
    )

    parser.add_argument(
        "--output-dir",
        default=config.output_dir,
        help="Output directory for generated files",
    )

    parser.add_argument(
        "--output",
        default=config.output_file,
        help="Output HTML file name (will be placed in output directory)",
    )

    parser.add_argument("--config", help="Configuration file path (.env file)")

    parser.add_argument(
        "--mock-llm", action="store_true", help="Use mock LLM responses for testing"
    )

    parser.add_argument(
        "--simplified-mode",
        action="store_true",
        help="Use simplified mode with simulated source content",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=config.log_level,
        help="Set logging level",
    )

    parser.add_argument(
        "--validate-config", action="store_true", help="Validate configuration and exit"
    )

    parser.add_argument(
        "--version", action="version", version="Citation Validator 1.0.0"
    )

    return parser


def validate_args(args) -> bool:
    """
    Validate command-line arguments.

    Args:
        args: Parsed arguments

    Returns:
        True if valid, False otherwise
    """
    # Check if input directory exists
    input_path = Path(args.input_dir)
    if not input_path.exists():
        logger.error(f"Input directory does not exist: {args.input_dir}")
        return False

    # Check if required input files exist
    content_file = input_path / "content.html"
    footnotes_file = input_path / "footnotes.json"

    if not content_file.exists():
        logger.error(f"Required file not found: {content_file}")
        return False

    if not footnotes_file.exists():
        logger.error(f"Required file not found: {footnotes_file}")
        return False

    return True


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Load custom config if provided
    if args.config:
        from .config import Config

        global config
        config = Config(args.config)

    # Override config with CLI args
    if args.mock_llm:
        import os

        os.environ["USE_MOCK_LLM"] = "true"

    if args.simplified_mode:
        import os

        os.environ["USE_SIMPLIFIED_MODE"] = "true"

    if args.output_dir:
        import os

        os.environ["OUTPUT_DIR"] = args.output_dir

    # Validate configuration
    if args.validate_config:
        print("Validating configuration...")
        if config.validate():
            print("✅ Configuration is valid")
            print("\nConfiguration Summary:")
            summary = config.get_summary()
            for key, value in summary.items():
                print(f"  {key}: {value}")
            sys.exit(0)
        else:
            print("❌ Configuration is invalid")
            sys.exit(1)

    # Validate arguments
    if not validate_args(args):
        sys.exit(1)

    # Print startup information
    print("Citation Validation Pipeline")
    print("=" * 40)
    summary = config.get_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("=" * 40)

    # Run validation
    try:
        validator = CitationValidator(input_dir=args.input_dir, output_file=args.output)
        validator.run_pipeline()
        print(f"\n✅ Validation completed successfully!")
        print(f"📄 Output saved to: {args.output}")

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

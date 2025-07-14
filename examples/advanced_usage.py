#!/usr/bin/env python3
"""
Example: Advanced configuration and custom usage.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from citation_validator import CitationValidator


def main():
    """Demonstrate advanced configuration."""
    print("Citation Validator - Advanced Example")
    print("=" * 40)

    # Set custom environment variables
    os.environ["USE_MOCK_LLM"] = "true"
    os.environ["USE_SIMPLIFIED_MODE"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["OUTPUT_DIR"] = "custom_output"

    # Create validator with custom settings
    validator = CitationValidator(
        input_dir="input", output_file="advanced_example_output.html"
    )

    print("Configuration:")
    print(f"  Input Dir: {validator.input_dir}")
    print(f"  Output File: {validator.output_file}")
    print(f"  LLM Available: {validator.llm_provider.is_available()}")
    print()

    try:
        # Run validation
        validator.run_pipeline()
        print("✅ Advanced validation completed!")

    except Exception as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    main()

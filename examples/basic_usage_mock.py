#!/usr/bin/env python3
"""
Example: Basic usage of the Citation Validator with mock LLM.
"""

from citation_validator import CitationValidator
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def main():
    """Demonstrate basic usage with mock LLM."""
    print("Citation Validator - Basic Example (Mock LLM)")
    print("=" * 45)

    # Set environment variable to use mock LLM
    import os

    os.environ["USE_MOCK_LLM"] = "true"

    # Create validator with default settings (will use mock LLM due to env var)
    validator = CitationValidator(
        input_dir="input", output_file="basic_example_mock_output.html"
    )

    # Show validation summary
    summary = validator.get_validation_summary()
    print("Validation Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print()

    # Run validation
    try:
        validator.run_pipeline()
        print("✅ Basic citation validation complete!")
        print(f"📄 Output saved to: {summary['output_file']}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    main()

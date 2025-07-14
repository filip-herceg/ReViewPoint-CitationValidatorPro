#!/usr/bin/env python3
"""
Example: Basic usage of the Citation Validator.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from citation_validator import CitationValidator


def main():
    """Demonstrate basic usage."""
    print("Citation Validator - Basic Example")
    print("=" * 40)
    
    # Create validator with default settings
    validator = CitationValidator(
        input_dir="input",
        output_file="basic_example_output.html"
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
    except Exception as e:
        print(f"❌ Validation failed: {e}")


if __name__ == "__main__":
    main()

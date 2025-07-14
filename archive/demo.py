#!/usr/bin/env python3
"""
Demo script for the Citation Validation Pipeline

This script demonstrates how to use the citation validator in different modes.
"""

from citation_validator import CitationValidator
import logging

def demo_simplified_mode():
    """Demonstrate the simplified mode with mock LLM responses."""
    print("\n" + "="*60)
    print("DEMO: Simplified Mode (Mock LLM)")
    print("="*60)
    
    # Configure for simplified mode
    import citation_validator
    citation_validator.USE_SIMPLIFIED_MODE = True
    citation_validator.USE_MOCK_LLM = True
    
    validator = CitationValidator(
        input_dir="input",
        output_file="content_reviewed_simplified.html"
    )
    
    try:
        validator.run_pipeline()
        print("\n✅ Simplified mode demo completed successfully!")
        print("📄 Output saved to: content_reviewed_simplified.html")
    except Exception as e:
        print(f"❌ Error in simplified mode: {e}")


def demo_configuration_options():
    """Show different configuration options."""
    print("\n" + "="*60)
    print("CONFIGURATION OPTIONS")
    print("="*60)
    
    print("1. Simplified Mode vs Full Mode:")
    print("   - Simplified: Mock responses, no actual source validation")
    print("   - Full: Uses actual LLM with source comparison (future feature)")
    print()
    
    print("2. LLM Options:")
    print("   - Mock LLM: Predefined responses for testing")
    print("   - OpenAI API: Real LLM responses (requires API key)")
    print()
    
    print("3. Configuration Variables in citation_validator.py:")
    print("   - USE_SIMPLIFIED_MODE: True/False")
    print("   - USE_MOCK_LLM: True/False")
    print("   - OPENAI_API_KEY: Your API key or None")
    print()


def demo_input_format():
    """Demonstrate the expected input format."""
    print("\n" + "="*60)
    print("INPUT FORMAT REQUIREMENTS")
    print("="*60)
    
    print("📁 Input Directory Structure:")
    print("   input/")
    print("   ├── content.html    # HTML with <div id='X'> elements")
    print("   └── footnotes.json  # Citation metadata")
    print()
    
    print("📄 content.html format:")
    print("   <div id='1'>Text content...</div>")
    print("   <div id='2'>More content...</div>")
    print()
    
    print("📄 footnotes.json format:")
    print("   [")
    print("     {")
    print('       "number": 1,')
    print('       "citation": "Author et al. 2024, p. 123",')
    print('       "title": "Paper Title",')
    print('       "authors": ["Author Name"],')
    print("       ...")
    print("     }")
    print("   ]")
    print()


def demo_output_format():
    """Demonstrate the output format."""
    print("\n" + "="*60)
    print("OUTPUT FORMAT")
    print("="*60)
    
    print("📄 The pipeline generates content_reviewed.html with:")
    print("   - Original div content")
    print("   - New <div class='response'> after each original div")
    print("   - CSS styling for response divs")
    print("   - LLM evaluation of each citation")
    print()
    
    print("🎨 Response div styling:")
    print("   - Light blue left border")
    print("   - Gray background")
    print("   - Italic text")
    print("   - Clear visual separation")
    print()


def main():
    """Run all demos."""
    # Set up logging
    logging.basicConfig(level=logging.WARNING)  # Reduce log noise for demo
    
    print("Citation Validation Pipeline - Demo")
    print("=" * 40)
    
    # Show configuration options
    demo_configuration_options()
    
    # Show input/output format
    demo_input_format()
    demo_output_format()
    
    # Run simplified mode demo
    demo_simplified_mode()
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. Open content_reviewed_simplified.html in a browser")
    print("2. Review the LLM evaluations for each citation")
    print("3. Modify configuration variables to test different modes")
    print("4. Add your OpenAI API key for real LLM responses")
    print("5. Future: Implement web crawler integration for full mode")
    print()


if __name__ == "__main__":
    main()

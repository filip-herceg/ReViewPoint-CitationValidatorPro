"""
Citation Validator Package

A comprehensive tool for validating academic citations in HTML documents
using Large Language Models (LLMs).
"""

__version__ = "1.0.0"
__author__ = "Citation Validator Team"

# Import main classes for easy access
try:
    from .core import CitationValidator
    from .config import Config
    
    __all__ = [
        "CitationValidator",
        "Config",
    ]
except ImportError:
    # Handle import errors gracefully during development
    __all__ = []

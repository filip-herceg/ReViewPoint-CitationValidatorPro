"""
Test configuration and fixtures.
"""

import pytest
import tempfile
import json
from pathlib import Path


@pytest.fixture
def temp_input_dir():
    """Create temporary input directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = Path(tmpdir)
        
        # Create test HTML content
        html_content = '''<!DOCTYPE html>
<html>
<head><title>Test Document</title></head>
<body>
    <div id="1">This is a test citation about AI research.</div>
    <div id="2">Another citation about code completion systems.</div>
</body>
</html>'''
        
        with open(input_dir / "content.html", "w") as f:
            f.write(html_content)
        
        # Create test footnotes
        footnotes = [
            {
                "number": 1,
                "title": "AI Research Survey",
                "authors": "Smith, J.",
                "year": "2024",
                "citation": "Smith, J. (2024). AI Research Survey."
            },
            {
                "number": 2,
                "title": "Code Completion Systems",
                "authors": "Doe, A.",
                "year": "2023",
                "citation": "Doe, A. (2023). Code Completion Systems."
            }
        ]
        
        with open(input_dir / "footnotes.json", "w") as f:
            json.dump(footnotes, f)
        
        yield str(input_dir)


@pytest.fixture
def sample_citation():
    """Sample citation metadata."""
    return {
        "number": 1,
        "title": "Test Citation",
        "authors": "Test Author",
        "year": "2024",
        "citation": "Test Author (2024). Test Citation."
    }

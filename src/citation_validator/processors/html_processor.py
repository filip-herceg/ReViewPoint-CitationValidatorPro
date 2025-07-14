"""
HTML processing utilities for citation validation.
"""

import re
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
except ImportError:
    logger.error("BeautifulSoup not installed. Install with: "
                "pip install beautifulsoup4")
    raise


class HTMLProcessor:
    """Handles HTML content loading, parsing, and modification."""
    
    def __init__(self, input_dir: str = "input"):
        """
        Initialize HTML processor.
        
        Args:
            input_dir: Directory containing input files
        """
        self.input_dir = Path(input_dir)
        self.content_html_path = self.input_dir / "content.html"
    
    def load_html_content(self) -> BeautifulSoup:
        """
        Load and parse the HTML content file.
        
        Returns:
            Parsed BeautifulSoup object
            
        Raises:
            FileNotFoundError: If content file doesn't exist
        """
        logger.info(f"Loading HTML content from {self.content_html_path}")
        
        if not self.content_html_path.exists():
            raise FileNotFoundError(
                f"Content file not found: {self.content_html_path}"
            )
        
        with open(self.content_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return BeautifulSoup(content, 'html.parser')
    
    def extract_text_from_div(self, div_element) -> str:
        """
        Extract plain text content from a div element, excluding HTML tags.
        
        Args:
            div_element: BeautifulSoup div element
            
        Returns:
            Clean text content
        """
        # Get text content and clean up whitespace
        text = div_element.get_text(separator=' ', strip=True)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def find_divs_with_footnote_ids(self, soup: BeautifulSoup) -> list:
        """
        Find all divs with numeric IDs (footnote references).
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of div elements with numeric IDs
        """
        divs_with_ids = soup.find_all('div', id=True)
        valid_divs = []
        
        for div in divs_with_ids:
            try:
                footnote_id = int(div.get('id'))
                valid_divs.append((div, footnote_id))
            except (ValueError, TypeError):
                logger.warning(
                    f"Skipping div with non-numeric ID: {div.get('id')}"
                )
                continue
        
        logger.info(f"Found {len(valid_divs)} divs with valid footnote IDs")
        return valid_divs
    
    def add_response_div(self, soup: BeautifulSoup, target_div,
                        response_content: str) -> None:
        """
        Add a response div after the target div.
        
        Args:
            soup: BeautifulSoup object
            target_div: Div element to add response after
            response_content: Content for the response div
        """
        response_div = soup.new_tag('div', **{'class': 'response'})
        response_div.string = response_content
        target_div.insert_after(response_div)
    
    def add_response_styling(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Add CSS styling for response divs.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Modified BeautifulSoup object
        """
        head = soup.find('head')
        if head:
            response_style_tag = soup.new_tag('style')
            response_styles = '''
        .response {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            margin-top: 0.5rem;
            padding: 1rem;
            font-style: italic;
            color: #495057;
            white-space: pre-wrap;
        }'''
            response_style_tag.append(response_styles)
            head.append(response_style_tag)
        
        return soup
    
    def save_html(self, soup: BeautifulSoup, output_path: str) -> None:
        """
        Save the modified HTML to output file.
        
        Args:
            soup: BeautifulSoup object to save
            output_path: Path to save the file
        """
        output_file = Path(output_path)
        
        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving HTML output to {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        logger.info(f"HTML output saved successfully to {output_file}")

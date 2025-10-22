"""
HTML Cleaning Module

Provides HTML preprocessing functionality using lxml to remove scripts, styles,
and other noise while preserving content structure.
"""

from enum import Enum
from typing import Optional

try:
    from lxml.html.clean import Cleaner
    import lxml.html as LH
except ImportError:
    raise ImportError(
        "lxml is required for HTML cleaning. Install with: pip install lxml"
    )


class HTMLCleaningLevel(Enum):
    """HTML cleaning aggressiveness levels."""
    LIGHT = "light"  # Remove only scripts and styles
    STANDARD = "standard"  # Recommended, matches training data
    AGGRESSIVE = "aggressive"  # Remove more elements


# Pre-configured cleaners for different levels
_CLEANERS = {
    HTMLCleaningLevel.LIGHT: Cleaner(
        scripts=True,
        javascript=True,
        style=True,
        inline_style=False,  # Keep inline styles in light mode
        safe_attrs_only=False,
        remove_tags=[],
        kill_tags=[]
    ),
    
    HTMLCleaningLevel.STANDARD: Cleaner(
        scripts=True,
        javascript=True,
        style=True,
        inline_style=True,
        safe_attrs_only=False,
        remove_tags=[],
        kill_tags=[]
    ),
    
    HTMLCleaningLevel.AGGRESSIVE: Cleaner(
        scripts=True,
        javascript=True,
        style=True,
        inline_style=True,
        safe_attrs_only=False,
        forms=True,  # Remove forms
        remove_tags=['iframe', 'noscript', 'nav', 'footer', 'header'],
        kill_tags=['script', 'style']
    )
}


def clean_html_content(
    html: str,
    level: HTMLCleaningLevel = HTMLCleaningLevel.STANDARD
) -> str:
    """Clean HTML by removing scripts, styles, and JavaScript.
    
    This function uses lxml to remove unwanted elements from HTML while preserving
    the content structure. The cleaning level matches what Schematron was trained on.
    
    Args:
        html: Raw HTML content to clean
        level: Cleaning level (LIGHT, STANDARD, or AGGRESSIVE)
        
    Returns:
        Cleaned HTML string
        
    Examples:
        >>> html = '<html><head><script>alert("hi")</script></head><body>Content</body></html>'
        >>> clean_html_content(html)
        '<html><head></head><body>Content</body></html>'
    """
    # Handle empty input
    if not html or not html.strip():
        return ""
    
    # Get appropriate cleaner
    cleaner = _CLEANERS.get(level, _CLEANERS[HTMLCleaningLevel.STANDARD])
    
    try:
        # Parse HTML
        doc = LH.fromstring(html)
        
        # Clean the document
        cleaned = cleaner.clean_html(doc)
        
        # Convert back to string
        cleaned_html = LH.tostring(cleaned, encoding="unicode")
        
        return cleaned_html
        
    except Exception as e:
        # If cleaning fails, log warning and return original
        # (MCP server will log this through ctx.log_warning)
        print(f"Warning: HTML cleaning failed: {str(e)}")
        return html


def estimate_cleaning_reduction(html: str, level: HTMLCleaningLevel = HTMLCleaningLevel.STANDARD) -> float:
    """Estimate the size reduction from cleaning HTML.
    
    Args:
        html: Raw HTML content
        level: Cleaning level
        
    Returns:
        Percentage reduction (0-100)
    """
    if not html:
        return 0.0
    
    cleaned = clean_html_content(html, level)
    
    original_size = len(html)
    cleaned_size = len(cleaned)
    
    if original_size == 0:
        return 0.0
    
    reduction = (1 - cleaned_size / original_size) * 100
    return round(reduction, 2)


def remove_specific_tags(html: str, tags_to_remove: list[str]) -> str:
    """Remove specific HTML tags while keeping content.
    
    Args:
        html: Raw HTML content
        tags_to_remove: List of tag names to remove (e.g., ['nav', 'footer'])
        
    Returns:
        HTML with specified tags removed
    """
    if not html or not tags_to_remove:
        return html
    
    try:
        doc = LH.fromstring(html)
        
        # Remove each specified tag
        for tag in tags_to_remove:
            for element in doc.xpath(f'.//{tag}'):
                element.drop_tag()
        
        return LH.tostring(doc, encoding="unicode")
    
    except Exception:
        return html


def extract_text_only(html: str) -> str:
    """Extract only text content from HTML (no tags).
    
    Args:
        html: Raw HTML content
        
    Returns:
        Plain text extracted from HTML
    """
    if not html:
        return ""
    
    try:
        doc = LH.fromstring(html)
        return doc.text_content()
    except Exception:
        return html

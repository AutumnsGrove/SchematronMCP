#!/usr/bin/env python3
"""
Test script for Schematron MCP Server

This script demonstrates how to test the extraction functionality locally
without going through the full MCP protocol.
"""

import asyncio
from schematron_mcp.inference.mlx import SchematronModel
from schematron_mcp.cleaning.html_cleaner import clean_html_content
from examples.schemas import PRODUCT_SCHEMA, ARTICLE_SCHEMA


async def test_product_extraction():
    """Test product extraction from sample HTML."""
    
    print("=" * 60)
    print("Testing Product Extraction")
    print("=" * 60)
    
    # Sample HTML
    html = """
    <div id="product">
        <h1 class="title">MacBook Pro M3</h1>
        <div class="price">
            <span class="currency">$</span>
            <span class="amount">2,499.99</span>
        </div>
        <div class="rating">
            <span class="stars">⭐⭐⭐⭐⭐</span>
            <span class="count">(127 reviews)</span>
        </div>
        <p class="description">
            The most powerful MacBook Pro ever with Apple M3 chip.
        </p>
        <ul class="specs">
            <li>RAM: 16GB</li>
            <li>Storage: 512GB SSD</li>
            <li>Display: 14-inch Liquid Retina XDR</li>
        </ul>
        <div class="stock">In Stock</div>
    </div>
    """
    
    # Clean HTML
    print("\n1. Cleaning HTML...")
    cleaned = clean_html_content(html)
    print(f"   Original: {len(html)} chars → Cleaned: {len(cleaned)} chars")
    
    # Load model
    print("\n2. Loading model...")
    model = SchematronModel(verbose=True)
    await model.load()
    print("   Model loaded!")
    
    # Extract data
    print("\n3. Extracting structured data...")
    result = await model.extract(
        html=cleaned,
        schema=PRODUCT_SCHEMA,
        temperature=0.0,
        max_tokens=4000
    )
    
    # Display result
    print("\n4. Extraction Result:")
    print("-" * 60)
    import json
    print(json.dumps(result, indent=2))
    print("-" * 60)
    
    return result


async def test_article_extraction():
    """Test article extraction from sample HTML."""
    
    print("\n\n" + "=" * 60)
    print("Testing Article Extraction")
    print("=" * 60)
    
    # Sample HTML
    html = """
    <article>
        <header>
            <h1>The Future of AI in 2025</h1>
            <div class="meta">
                <span class="author">By Jane Smith</span>
                <time datetime="2025-01-15">January 15, 2025</time>
            </div>
        </header>
        <div class="content">
            <p>Artificial intelligence continues to evolve at a rapid pace...</p>
            <p>In this article, we explore the latest trends and predictions.</p>
        </div>
        <footer>
            <div class="tags">
                <span class="tag">AI</span>
                <span class="tag">Technology</span>
                <span class="tag">Future</span>
            </div>
        </footer>
    </article>
    """
    
    # Clean HTML
    print("\n1. Cleaning HTML...")
    cleaned = clean_html_content(html)
    
    # Load model (reuse if already loaded)
    print("\n2. Using loaded model...")
    model = SchematronModel(verbose=True)
    await model.load()
    
    # Extract data
    print("\n3. Extracting structured data...")
    result = await model.extract(
        html=cleaned,
        schema=ARTICLE_SCHEMA,
        temperature=0.0,
        max_tokens=4000
    )
    
    # Display result
    print("\n4. Extraction Result:")
    print("-" * 60)
    import json
    print(json.dumps(result, indent=2))
    print("-" * 60)
    
    return result


async def test_html_cleaning():
    """Test HTML cleaning at different levels."""
    
    print("\n\n" + "=" * 60)
    print("Testing HTML Cleaning")
    print("=" * 60)
    
    html = """
    <html>
    <head>
        <script>alert('test');</script>
        <style>body { color: red; }</style>
    </head>
    <body>
        <h1>Title</h1>
        <p style="color: blue;">Content</p>
    </body>
    </html>
    """
    
    from schematron_mcp.cleaning.html_cleaner import HTMLCleaningLevel
    
    for level in [HTMLCleaningLevel.LIGHT, HTMLCleaningLevel.STANDARD, HTMLCleaningLevel.AGGRESSIVE]:
        print(f"\n{level.value.upper()} Cleaning:")
        cleaned = clean_html_content(html, level=level)
        print(f"Original: {len(html)} → Cleaned: {len(cleaned)} ({100*(1-len(cleaned)/len(html)):.1f}% reduction)")
        print(f"Sample: {cleaned[:200]}...")


async def main():
    """Run all tests."""
    try:
        # Test HTML cleaning
        await test_html_cleaning()
        
        # Test product extraction
        await test_product_extraction()
        
        # Test article extraction
        await test_article_extraction()
        
        print("\n\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

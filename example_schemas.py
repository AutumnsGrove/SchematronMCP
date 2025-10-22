"""
Example JSON Schemas for Common Extraction Tasks

This module provides pre-built schemas for common web scraping and data extraction tasks.
Use these as starting points and customize for your specific needs.
"""

from typing import Dict, Any


# E-commerce Product Extraction
PRODUCT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Product name or title"
        },
        "price": {
            "type": "number",
            "description": "Product price in USD"
        },
        "currency": {
            "type": "string",
            "description": "Currency code (e.g., USD, EUR)"
        },
        "rating": {
            "type": "number",
            "description": "Product rating (e.g., 4.5 out of 5)"
        },
        "review_count": {
            "type": "integer",
            "description": "Number of customer reviews"
        },
        "in_stock": {
            "type": "boolean",
            "description": "Whether product is currently in stock"
        },
        "description": {
            "type": "string",
            "description": "Product description"
        },
        "specifications": {
            "type": "object",
            "description": "Technical specifications as key-value pairs"
        },
        "images": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of product image URLs"
        },
        "category": {
            "type": "string",
            "description": "Product category"
        }
    },
    "required": ["name", "price"]
}


# Blog Article/News Extraction
ARTICLE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "Article title or headline"
        },
        "author": {
            "type": "string",
            "description": "Author name"
        },
        "published_date": {
            "type": "string",
            "description": "Publication date in ISO format or human-readable"
        },
        "content": {
            "type": "string",
            "description": "Main article content/body text"
        },
        "summary": {
            "type": "string",
            "description": "Article summary or excerpt"
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Article tags or categories"
        },
        "word_count": {
            "type": "integer",
            "description": "Estimated word count"
        },
        "image_url": {
            "type": "string",
            "description": "Main article image URL"
        }
    },
    "required": ["title", "content"]
}


# Job Posting Extraction
JOB_POSTING_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "Job title"
        },
        "company": {
            "type": "string",
            "description": "Company name"
        },
        "location": {
            "type": "string",
            "description": "Job location (city, state, or remote)"
        },
        "salary_range": {
            "type": "string",
            "description": "Salary range (e.g., $80k-$120k)"
        },
        "employment_type": {
            "type": "string",
            "description": "Employment type (full-time, part-time, contract)"
        },
        "description": {
            "type": "string",
            "description": "Job description"
        },
        "requirements": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of job requirements"
        },
        "benefits": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of benefits offered"
        },
        "posted_date": {
            "type": "string",
            "description": "Date job was posted"
        },
        "application_url": {
            "type": "string",
            "description": "URL to apply for the job"
        }
    },
    "required": ["title", "company", "location"]
}


# Real Estate Listing Extraction
REAL_ESTATE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "address": {
            "type": "string",
            "description": "Property address"
        },
        "price": {
            "type": "number",
            "description": "Listing price"
        },
        "bedrooms": {
            "type": "integer",
            "description": "Number of bedrooms"
        },
        "bathrooms": {
            "type": "number",
            "description": "Number of bathrooms"
        },
        "square_feet": {
            "type": "integer",
            "description": "Property size in square feet"
        },
        "property_type": {
            "type": "string",
            "description": "Type of property (house, condo, apartment, etc.)"
        },
        "description": {
            "type": "string",
            "description": "Property description"
        },
        "features": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of property features"
        },
        "images": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of property image URLs"
        },
        "year_built": {
            "type": "integer",
            "description": "Year the property was built"
        },
        "listing_agent": {
            "type": "string",
            "description": "Name of listing agent"
        }
    },
    "required": ["address", "price"]
}


# Restaurant/Business Listing
RESTAURANT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Restaurant name"
        },
        "cuisine": {
            "type": "string",
            "description": "Type of cuisine"
        },
        "address": {
            "type": "string",
            "description": "Restaurant address"
        },
        "phone": {
            "type": "string",
            "description": "Phone number"
        },
        "rating": {
            "type": "number",
            "description": "Average rating (e.g., 4.5)"
        },
        "review_count": {
            "type": "integer",
            "description": "Number of reviews"
        },
        "price_range": {
            "type": "string",
            "description": "Price range (e.g., $$, $$$)"
        },
        "hours": {
            "type": "object",
            "description": "Operating hours by day"
        },
        "features": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Features (outdoor seating, delivery, etc.)"
        },
        "menu_url": {
            "type": "string",
            "description": "URL to menu"
        }
    },
    "required": ["name", "address"]
}


# Event Listing
EVENT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "Event title"
        },
        "date": {
            "type": "string",
            "description": "Event date"
        },
        "time": {
            "type": "string",
            "description": "Event time"
        },
        "location": {
            "type": "string",
            "description": "Event location/venue"
        },
        "description": {
            "type": "string",
            "description": "Event description"
        },
        "organizer": {
            "type": "string",
            "description": "Event organizer"
        },
        "ticket_price": {
            "type": "number",
            "description": "Ticket price"
        },
        "registration_url": {
            "type": "string",
            "description": "URL to register/buy tickets"
        },
        "category": {
            "type": "string",
            "description": "Event category (conference, concert, etc.)"
        }
    },
    "required": ["title", "date", "location"]
}


# Contact Information
CONTACT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Person or organization name"
        },
        "email": {
            "type": "string",
            "description": "Email address"
        },
        "phone": {
            "type": "string",
            "description": "Phone number"
        },
        "address": {
            "type": "string",
            "description": "Physical address"
        },
        "website": {
            "type": "string",
            "description": "Website URL"
        },
        "social_media": {
            "type": "object",
            "properties": {
                "twitter": {"type": "string"},
                "linkedin": {"type": "string"},
                "facebook": {"type": "string"}
            },
            "description": "Social media profiles"
        }
    },
    "required": ["name"]
}


# Research Paper/Publication
PUBLICATION_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "Publication title"
        },
        "authors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of authors"
        },
        "abstract": {
            "type": "string",
            "description": "Abstract or summary"
        },
        "publication_date": {
            "type": "string",
            "description": "Date of publication"
        },
        "journal": {
            "type": "string",
            "description": "Journal or conference name"
        },
        "doi": {
            "type": "string",
            "description": "DOI identifier"
        },
        "keywords": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Keywords or topics"
        },
        "pdf_url": {
            "type": "string",
            "description": "URL to PDF"
        }
    },
    "required": ["title", "authors"]
}


# Generic Table Data
TABLE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "headers": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Column headers"
        },
        "rows": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}
            },
            "description": "Table rows as arrays"
        }
    },
    "required": ["headers", "rows"]
}


# All schemas for easy access
ALL_SCHEMAS = {
    "product": PRODUCT_SCHEMA,
    "article": ARTICLE_SCHEMA,
    "job": JOB_POSTING_SCHEMA,
    "real_estate": REAL_ESTATE_SCHEMA,
    "restaurant": RESTAURANT_SCHEMA,
    "event": EVENT_SCHEMA,
    "contact": CONTACT_SCHEMA,
    "publication": PUBLICATION_SCHEMA,
    "table": TABLE_SCHEMA,
}


def get_schema(name: str) -> Dict[str, Any]:
    """Get a schema by name.
    
    Args:
        name: Schema name (product, article, job, etc.)
        
    Returns:
        JSON Schema dictionary
        
    Raises:
        KeyError: If schema name not found
    """
    return ALL_SCHEMAS[name]


def list_schemas() -> list[str]:
    """List all available schema names."""
    return list(ALL_SCHEMAS.keys())

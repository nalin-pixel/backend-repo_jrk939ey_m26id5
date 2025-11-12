"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (you can keep using these if needed):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Tourism app schemas

class Destination(BaseModel):
    """
    Travel destinations (e.g., Dubai, Thailand)
    Collection name: "destination"
    """
    name: str = Field(..., description="Destination name")
    slug: str = Field(..., description="URL-friendly identifier")
    country: Optional[str] = Field(None, description="Country")
    description: Optional[str] = Field(None, description="Short description")
    image: Optional[str] = Field(None, description="Hero image URL")
    highlights: Optional[List[str]] = Field(default_factory=list, description="Key highlights")

class Package(BaseModel):
    """
    Travel packages for destinations
    Collection name: "package"
    """
    title: str = Field(..., description="Package title")
    destination_slug: str = Field(..., description="Slug of the destination")
    days: int = Field(..., gt=0, description="Number of days")
    price: float = Field(..., ge=0, description="Price in USD")
    includes: Optional[List[str]] = Field(default_factory=list, description="What is included")
    image: Optional[str] = Field(None, description="Image URL")

class Inquiry(BaseModel):
    """
    Customer inquiries / leads
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Customer full name")
    email: EmailStr = Field(..., description="Customer email")
    phone: Optional[str] = Field(None, description="Phone number")
    message: Optional[str] = Field(None, description="Customer message")
    package_title: Optional[str] = Field(None, description="Interested package title")
    destination_slug: Optional[str] = Field(None, description="Related destination slug")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!

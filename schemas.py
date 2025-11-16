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

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
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

# Real Estate Property schema
class GeoLocation(BaseModel):
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")

class Property(BaseModel):
    """
    Real estate property schema
    Collection name: "property"
    """
    title: str = Field(..., description="Listing title")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")
    price: float = Field(..., ge=0, description="Price in USD")
    bedrooms: int = Field(..., ge=0)
    bathrooms: int = Field(..., ge=0)
    area: float = Field(..., ge=0, description="Area in sqft")
    type: str = Field(..., description="Property type e.g., Apartment, Villa")
    status: str = Field("For Sale", description="For Sale, For Rent, Sold")
    badges: List[str] = Field(default_factory=list, description="Badges like Hot, Furnished")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    description: Optional[str] = Field(None, description="Detailed description")
    amenities: List[str] = Field(default_factory=list)
    location: Optional[GeoLocation] = None
    floor_plans: List[str] = Field(default_factory=list, description="Floor plan image URLs")
    featured: bool = Field(False)

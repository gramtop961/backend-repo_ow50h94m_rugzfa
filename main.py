import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Property

app = FastAPI(title="Luxury Real Estate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PropertyCreate(Property):
    pass

class PropertyOut(Property):
    id: str


def serialize_property(doc) -> PropertyOut:
    return PropertyOut(
        id=str(doc.get("_id")),
        title=doc.get("title"),
        address=doc.get("address"),
        city=doc.get("city"),
        country=doc.get("country"),
        price=doc.get("price"),
        bedrooms=doc.get("bedrooms"),
        bathrooms=doc.get("bathrooms"),
        area=doc.get("area"),
        type=doc.get("type"),
        status=doc.get("status"),
        badges=doc.get("badges", []),
        images=doc.get("images", []),
        description=doc.get("description"),
        amenities=doc.get("amenities", []),
        location=doc.get("location"),
        floor_plans=doc.get("floor_plans", []),
        featured=doc.get("featured", False),
    )


@app.get("/", tags=["health"])
async def root():
    return {"message": "Luxury Real Estate API running"}


@app.get("/properties", response_model=List[PropertyOut], tags=["properties"])
async def list_properties(
    city: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    bedrooms: Optional[int] = Query(None, ge=0),
    type: Optional[str] = None,
    featured: Optional[bool] = None,
    limit: int = Query(24, ge=1, le=100)
):
    filter_q = {}
    if city:
        filter_q["city"] = {"$regex": f"^{city}$", "$options": "i"}
    if type:
        filter_q["type"] = {"$regex": f"^{type}$", "$options": "i"}
    if bedrooms is not None:
        filter_q["bedrooms"] = {"$gte": bedrooms}
    if featured is not None:
        filter_q["featured"] = featured
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        filter_q["price"] = price_filter

    docs = get_documents("property", filter_q, limit)
    return [serialize_property(d) for d in docs]


@app.get("/properties/{prop_id}", response_model=PropertyOut, tags=["properties"])
async def get_property(prop_id: str):
    try:
        oid = ObjectId(prop_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid property id")

    doc = db["property"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Property not found")
    return serialize_property(doc)


@app.post("/properties", response_model=str, tags=["properties"])
async def create_property(payload: PropertyCreate):
    new_id = create_document("property", payload)
    return new_id


@app.get("/test", tags=["health"])  # database connectivity test
async def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

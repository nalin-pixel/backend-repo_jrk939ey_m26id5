import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Destination, Package, Inquiry

app = FastAPI(title="Tours & Travels API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Tours & Travels Backend Running"}

@app.get("/test")
def test_database():
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
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Seed default data endpoint (idempotent)
@app.post("/seed")
async def seed_data():
    try:
        existing = get_documents("destination", {}) if db else []
        if not existing:
            # Seed a couple of destinations
            dubai = Destination(
                name="Dubai",
                slug="dubai",
                country="United Arab Emirates",
                description="Futuristic city with luxury shopping, ultramodern architecture and vibrant nightlife.",
                image="https://images.unsplash.com/photo-1504270997636-07ddfbd48945?q=80&w=1600&auto=format&fit=crop",
                highlights=["Burj Khalifa", "Desert Safari", "Dubai Mall", "Dubai Marina"],
            )
            thailand = Destination(
                name="Thailand",
                slug="thailand",
                country="Thailand",
                description="Tropical beaches, opulent royal palaces, ancient ruins and ornate temples.",
                image="https://images.unsplash.com/photo-1540503831458-3237544b2d37?q=80&w=1600&auto=format&fit=crop",
                highlights=["Phuket Beaches", "Bangkok Temples", "Chiang Mai"],
            )
            create_document("destination", dubai)
            create_document("destination", thailand)

            create_document("package", Package(
                title="Dubai Highlights 5D/4N",
                destination_slug="dubai",
                days=5,
                price=899.0,
                includes=["Hotel", "Breakfast", "City Tour", "Desert Safari"],
                image="https://images.unsplash.com/photo-1546412414-8035e1776c9a?q=80&w=1600&auto=format&fit=crop"
            ))
            create_document("package", Package(
                title="Thailand Explorer 7D/6N",
                destination_slug="thailand",
                days=7,
                price=1099.0,
                includes=["Hotel", "Breakfast", "Phi Phi Tour", "Temple Visits"],
                image="https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=1600&auto=format&fit=crop"
            ))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public API
@app.get("/destinations")
async def list_destinations():
    try:
        docs = get_documents("destination", {}) if db else []
        for d in docs:
            d['_id'] = str(d.get('_id'))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/packages")
async def list_packages(destination: Optional[str] = None):
    try:
        query = {"destination_slug": destination} if destination else {}
        docs = get_documents("package", query) if db else []
        for d in docs:
            d['_id'] = str(d.get('_id'))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class InquiryIn(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: Optional[str] = None
    package_title: Optional[str] = None
    destination_slug: Optional[str] = None

@app.post("/inquire")
async def create_inquiry(payload: InquiryIn):
    try:
        inquiry = Inquiry(**payload.model_dump())
        inserted_id = create_document("inquiry", inquiry)
        return {"status": "received", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

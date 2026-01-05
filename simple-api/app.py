import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:password@localhost:27017/")
try:
    client = MongoClient(MONGODB_URL)
    db = client.simple_api_db
    visits_collection = db.visits
    # Test connection
    client.admin.command('ping')
    print(f"✅ Connected to MongoDB at {MONGODB_URL}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    client = None

@app.get("/")
def read_root():
    # Track visits in MongoDB
    if client:
        try:
            visits_collection.insert_one({
                "endpoint": "/",
                "timestamp": datetime.utcnow()
            })
            visit_count = visits_collection.count_documents({"endpoint": "/"})
            return {
                "message": "Welcome to Simple API",
                "visit_count": visit_count,
                "database": "connected"
            }
        except Exception as e:
            return {
                "message": "Welcome to Simple API",
                "database": "error",
                "error": str(e)
            }
    return {"message": "Welcome to Simple API", "database": "not connected"}

@app.get("/health")
def health_check():
    # Check MongoDB connection
    db_status = "disconnected"
    if client:
        try:
            client.admin.command('ping')
            db_status = "connected"
        except:
            db_status = "error"
    
    return {
        "status": "healthy",
        "database": db_status
    }

@app.get("/stats")
def get_stats():
    """Get visit statistics from MongoDB"""
    if not client:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        total_visits = visits_collection.count_documents({})
        root_visits = visits_collection.count_documents({"endpoint": "/"})
        
        return {
            "total_visits": total_visits,
            "root_endpoint_visits": root_visits,
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

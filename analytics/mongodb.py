from datetime import datetime,timezone
from django.conf import settings

def log_event(collection,payload):
    """Write historical data to MongoDB. App functions still work if MongoDB is offline."""
    try:
        from pymongo import MongoClient
        client=MongoClient(settings.MONGODB_URI,serverSelectionTimeoutMS=1200)
        payload["logged_at"]=datetime.now(timezone.utc)
        client[settings.MONGODB_DATABASE][collection].insert_one(payload)
        client.close()
    except Exception:
        pass

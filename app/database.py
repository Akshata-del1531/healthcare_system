import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "healthcare")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]

patient_collection = db.get_collection("patients")

async def get_patient_by_id(patient_id: str):
    return await patient_collection.find_one({"_id": patient_id})

async def list_patients():
    patients = []
    cursor = patient_collection.find({}).sort("created_at", -1)
    async for patient in cursor:
        patients.append(patient)
    return patients

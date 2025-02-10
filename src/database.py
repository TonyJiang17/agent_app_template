from pymongo import MongoClient
from typing import Optional, List
import os
from dotenv import load_dotenv
from schema.models_new import Roadmap
from bson import ObjectId
from pymongo.operations import SearchIndexModel

load_dotenv()

# MongoDB connection string
PWD = os.getenv("MONGO_PWD")
USER = os.getenv("MONGO_USER")
#MONGO_URI = f"mongodb+srv://{USER}:{PWD}@database.0o8ty.mongodb.net/?retryWrites=true&w=majority&appName=database"
MONGO_URI = f"mongodb+srv://{USER}:{PWD}@cluster0.5ixgx.mongodb.net/"

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.XXXX # change to db name 
        
    # Example Calls, replace with new schemas 
    def create_roadmap(self, roadmap: Roadmap) -> str:
        """Create a new roadmap"""
        data = roadmap.model_dump(exclude={"mongo_id"})
        result = self.db.roadmaps.insert_one(data)
        return str(result.inserted_id)
    
    def update_roadmap(self, roadmap_id: str, roadmap: Roadmap) -> bool:
        """Update an existing roadmap"""
        data = roadmap.model_dump(exclude={"mongo_id"})
        result = self.db.roadmaps.update_one(
            {'_id': ObjectId(roadmap_id)},
            {'$set': data}
        )
        return result.modified_count > 0
    
    def get_roadmap(self, roadmap_id: str) -> Optional[Roadmap]:
        """Get a roadmap by ID"""
        data = self.db.roadmaps.find_one({'_id': ObjectId(roadmap_id)})
        if data:
            data['mongo_id'] = data.pop('_id')
            return Roadmap.model_validate(data)
        return None
    
    def get_roadmap_by_title(self, title: str) -> Optional[Roadmap]:
        """Get a roadmap by title"""
        data = self.db.roadmaps.find_one({'title': title})
        if data:
            data['mongo_id'] = data.pop('_id')
            return Roadmap.model_validate(data)
        return None
    
    def get_all_roadmaps(self) -> List[Roadmap]:
        """Get all roadmaps"""
        data = list(self.db.roadmaps.find())
        roadmaps = []
        for item in data:
            item['mongo_id'] = item.pop('_id')
            roadmaps.append(Roadmap.model_validate(item))
        return roadmaps
    

if __name__ == "__main__":
    db = Database()
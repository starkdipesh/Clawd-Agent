from typing import List, Dict, Optional
import importlib
import os
import json

class SkillService:
    def __init__(self, db):
        self.db = db
        self.skills = db.skills
        self.loaded_skills = {}
        self.skill_directory = "/app/backend/skills"
    
    async def get_all_skills(self) -> List[Dict]:
        """Get all available skills"""
        cursor = self.skills.find({})
        skills = await cursor.to_list(length=100)
        return skills
    
    async def get_enabled_skills(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get enabled skills for a user"""
        query = {"enabled": True}
        cursor = self.skills.find(query)
        skills = await cursor.to_list(length=100)
        return skills
    
    async def enable_skill(self, skill_id: str) -> bool:
        """Enable a skill"""
        result = await self.skills.update_one(
            {"skill_id": skill_id},
            {"$set": {"enabled": True}}
        )
        return result.modified_count > 0
    
    async def disable_skill(self, skill_id: str) -> bool:
        """Disable a skill"""
        result = await self.skills.update_one(
            {"skill_id": skill_id},
            {"$set": {"enabled": False}}
        )
        return result.modified_count > 0
    
    async def execute_skill(self, skill_name: str, parameters: Dict) -> Dict:
        """Execute a skill with given parameters"""
        try:
            # Import skill module dynamically
            skill_module = importlib.import_module(f"skills.{skill_name}")
            result = await skill_module.execute(parameters)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def install_default_skills(self):
        """Install default built-in skills"""
        default_skills = [
            {
                "skill_id": "weather",
                "name": "Weather",
                "description": "Get weather information for any location",
                "category": "Information",
                "enabled": True,
                "config": {},
                "version": "1.0.0"
            },
            {
                "skill_id": "web_search",
                "name": "Web Search",
                "description": "Search the web for information",
                "category": "Information",
                "enabled": True,
                "config": {},
                "version": "1.0.0"
            },
            {
                "skill_id": "calendar",
                "name": "Calendar",
                "description": "Manage calendar events and reminders",
                "category": "Productivity",
                "enabled": True,
                "config": {},
                "version": "1.0.0"
            },
            {
                "skill_id": "email",
                "name": "Email",
                "description": "Read and send emails",
                "category": "Communication",
                "enabled": True,
                "config": {},
                "version": "1.0.0"
            },
            {
                "skill_id": "notes",
                "name": "Notes",
                "description": "Create and manage notes",
                "category": "Productivity",
                "enabled": True,
                "config": {},
                "version": "1.0.0"
            }
        ]
        
        for skill in default_skills:
            await self.skills.update_one(
                {"skill_id": skill["skill_id"]},
                {"$set": skill},
                upsert=True
            )
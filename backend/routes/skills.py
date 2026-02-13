from fastapi import APIRouter, HTTPException
from typing import List

from services.skill_service import SkillService

router = APIRouter(prefix="/api/skills", tags=["skills"])

def get_db():
    from server import db
    return db

@router.get("/list")
async def get_all_skills():
    """Get all available skills"""
    try:
        db = get_db()
        skill_service = SkillService(db)
        
        skills = await skill_service.get_all_skills()
        
        for skill in skills:
            skill.pop("_id", None)
        
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enabled")
async def get_enabled_skills(user_id: str = None):
    """Get enabled skills"""
    try:
        db = get_db()
        skill_service = SkillService(db)
        
        skills = await skill_service.get_enabled_skills(user_id)
        
        for skill in skills:
            skill.pop("_id", None)
        
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/enable/{skill_id}")
async def enable_skill(skill_id: str):
    """Enable a skill"""
    try:
        db = get_db()
        skill_service = SkillService(db)
        
        success = await skill_service.enable_skill(skill_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/disable/{skill_id}")
async def disable_skill(skill_id: str):
    """Disable a skill"""
    try:
        db = get_db()
        skill_service = SkillService(db)
        
        success = await skill_service.disable_skill(skill_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/install-defaults")
async def install_default_skills():
    """Install default built-in skills"""
    try:
        db = get_db()
        skill_service = SkillService(db)
        
        await skill_service.install_default_skills()
        return {"success": True, "message": "Default skills installed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
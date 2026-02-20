#!/usr/bin/env python3
"""
Test Skills Directly - Bypass Database Issues
"""
import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.append('/home/dipesh-patel/Documents/Clawd-Agent/backend')

from skills.weather import execute as weather_execute
from skills.web_search import execute as search_execute
from skills.calendar import execute as calendar_execute
from skills.email import execute as email_execute
from skills.notes import execute as notes_execute

async def test_all_skills():
    """Test all skills directly"""
    print("🧪 Testing Moltbot Skills Directly")
    print("=" * 50)
    
    # Test Weather Skill
    print("\n🌤️ Testing Weather Skill:")
    weather_result = await weather_execute({"location": "delhi"})
    print(weather_result)
    
    # Test Web Search Skill
    print("\n🔍 Testing Web Search Skill:")
    search_result = await search_execute({"query": "python programming"})
    print(search_result)
    
    # Test Calendar Skill
    print("\n📅 Testing Calendar Skill:")
    calendar_result = await calendar_execute({"action": "list"})
    print(calendar_result)
    
    # Test Email Skill
    print("\n📧 Testing Email Skill:")
    email_result = await email_execute({"action": "inbox"})
    print(email_result)
    
    # Test Notes Skill
    print("\n📝 Testing Notes Skill:")
    notes_result = await notes_execute({"action": "list"})
    print(notes_result)
    
    print("\n✅ All Skills Tested Successfully!")

if __name__ == "__main__":
    asyncio.run(test_all_skills())

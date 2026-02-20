# Weather Skill
import requests
import json

async def execute(parameters: dict) -> str:
    """Execute weather skill"""
    try:
        location = parameters.get('location', 'current location')
        
        # Mock weather data (in real implementation, use weather API)
        weather_data = {
            'delhi': {
                'temp': '32°C',
                'condition': 'Partly Cloudy',
                'humidity': '45%',
                'wind': '10 km/h'
            },
            'mumbai': {
                'temp': '30°C', 
                'condition': 'Humid',
                'humidity': '70%',
                'wind': '15 km/h'
            },
            'default': {
                'temp': '25°C',
                'condition': 'Pleasant',
                'humidity': '50%',
                'wind': '5 km/h'
            }
        }
        
        # Normalize location name
        location_lower = location.lower()
        if 'delhi' in location_lower:
            weather = weather_data['delhi']
        elif 'mumbai' in location_lower:
            weather = weather_data['mumbai']
        else:
            weather = weather_data['default']
        
        return f"""🌤️ Weather Update for {location.title()}:
        
🌡️ Temperature: {weather['temp']}
☁️ Condition: {weather['condition']}
💧 Humidity: {weather['humidity']}
💨 Wind: {weather['wind']}

Have a great day! ☀️"""
        
    except Exception as e:
        return f"❌ Sorry, I couldn't get weather information for {location}. Error: {str(e)}"

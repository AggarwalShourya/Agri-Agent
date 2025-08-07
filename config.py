import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Hard-coded farmer context (KHC data)
FARMER_CONTEXT = {
    "name": "Rajesh Kumar",
    "location": {
        "village": "Sikandarpur",
        "district": "Muzaffarpur", 
        "state": "Bihar",
        "coordinates": {"lat": 26.1209, "lng": 85.3647}
    },
    "crops": [
        {
            "name": "Wheat",
            "area": "2 acres",
            "planting_date": "2024-11-15",
            "expected_harvest": "2024-03-15",
            "current_stage": "flowering",
            "health_status": "good"
        },
        {
            "name": "Mustard",
            "area": "1.5 acres", 
            "planting_date": "2024-11-10",
            "expected_harvest": "2024-03-10",
            "current_stage": "pod_formation",
            "health_status": "good"
        }
    ],
    "financial_status": {
        "income_level": "medium",
        "savings": "limited",
        "credit_available": True,
        "risk_tolerance": "moderate"
    },
    "equipment": [
        "tractor",
        "irrigation_pump", 
        "sprayer",
        "harvester"
    ],
    "soil_type": "clay_loam",
    "irrigation_type": "drip_irrigation",
    "experience_years": 15
}

# Weather API configuration (placeholder)
WEATHER_API_CONFIG = {
    "base_url": "https://api.openweathermap.org/data/2.5/",
    "api_key": os.getenv("WEATHER_API_KEY", "")
}

# Market API configuration (placeholder)
MARKET_API_CONFIG = {
    "base_url": "https://api.example.com/market/",
    "api_key": os.getenv("MARKET_API_KEY", "")
}

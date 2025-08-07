import requests
import json
from typing import Dict, List, Optional
from langchain.tools import Tool
from config import WEATHER_API_CONFIG, MARKET_API_CONFIG, FARMER_CONTEXT

class WeatherTool:
    """Tool for fetching weather data and providing weather-based agricultural advice"""
    
    def __init__(self):
        self.api_key = WEATHER_API_CONFIG["api_key"]
        self.base_url = WEATHER_API_CONFIG["base_url"]
    
    def get_current_weather(self, location: Dict) -> Dict:
        """Get current weather conditions for a location"""
        if not self.api_key:
            # Mock data for demo purposes
            return {
                "temperature": 28,
                "humidity": 65, 
                "wind_speed": 12,
                "description": "partly cloudy",
                "rainfall_probability": 30
            }
        
        # Real API call would go here
        # lat, lng = location["coordinates"]["lat"], location["coordinates"]["lng"]
        # url = f"{self.base_url}weather?lat={lat}&lon={lng}&appid={self.api_key}&units=metric"
        # response = requests.get(url)
        # return response.json()
        
        return {
            "temperature": 28,
            "humidity": 65,
            "wind_speed": 12,
            "description": "partly cloudy",
            "rainfall_probability": 30
        }
    
    def get_weather_forecast(self, location: Dict, days: int = 7) -> List[Dict]:
        """Get weather forecast for upcoming days"""
        if not self.api_key:
            # Mock forecast data
            return [
                {"date": "2024-03-01", "temp_max": 32, "temp_min": 18, "rainfall": 0, "description": "sunny"},
                {"date": "2024-03-02", "temp_max": 35, "temp_min": 20, "rainfall": 0, "description": "hot"},
                {"date": "2024-03-03", "temp_max": 38, "temp_min": 22, "rainfall": 0, "description": "very hot"},
                {"date": "2024-03-04", "temp_max": 40, "temp_min": 25, "rainfall": 0, "description": "extremely hot"},
                {"date": "2024-03-05", "temp_max": 42, "temp_min": 27, "rainfall": 0, "description": "extremely hot"}
            ]
        
        # Real API call would go here
        return [
            {"date": "2024-03-01", "temp_max": 32, "temp_min": 18, "rainfall": 0, "description": "sunny"},
            {"date": "2024-03-02", "temp_max": 35, "temp_min": 20, "rainfall": 0, "description": "hot"},
            {"date": "2024-03-03", "temp_max": 38, "temp_min": 22, "rainfall": 0, "description": "very hot"},
            {"date": "2024-03-04", "temp_max": 40, "temp_min": 25, "rainfall": 0, "description": "extremely hot"},
            {"date": "2024-03-05", "temp_max": 42, "temp_min": 27, "rainfall": 0, "description": "extremely hot"}
        ]
    
    def analyze_weather_impact(self, weather_data: Dict, crop_info: Dict) -> Dict:
        """Analyze how weather conditions affect specific crops"""
        temp = weather_data.get("temperature", 25)
        humidity = weather_data.get("humidity", 60)
        rainfall = weather_data.get("rainfall_probability", 0)
        
        crop_name = crop_info.get("name", "").lower()
        stage = crop_info.get("current_stage", "")
        
        impact_analysis = {
            "risk_level": "low",
            "recommendations": [],
            "warnings": []
        }
        
        # Wheat-specific analysis
        if "wheat" in crop_name:
            if stage == "flowering":
                if temp > 35:
                    impact_analysis["risk_level"] = "high"
                    impact_analysis["warnings"].append("High temperature during flowering can reduce grain yield")
                    impact_analysis["recommendations"].append("Consider irrigation to reduce temperature stress")
                if rainfall > 80:
                    impact_analysis["risk_level"] = "medium"
                    impact_analysis["warnings"].append("Heavy rainfall can cause lodging and disease")
                    impact_analysis["recommendations"].append("Ensure proper drainage and monitor for fungal diseases")
        
        # Mustard-specific analysis
        elif "mustard" in crop_name:
            if stage == "pod_formation":
                if temp > 38:
                    impact_analysis["risk_level"] = "high"
                    impact_analysis["warnings"].append("Extreme heat can cause pod abortion in mustard")
                    impact_analysis["recommendations"].append("Apply light irrigation to reduce heat stress")
                if humidity > 80:
                    impact_analysis["risk_level"] = "medium"
                    impact_analysis["warnings"].append("High humidity can increase disease risk")
                    impact_analysis["recommendations"].append("Monitor for white rust and apply preventive fungicide if needed")
        
        return impact_analysis

class MarketTool:
    """Tool for fetching market data and providing market-based advice"""
    
    def __init__(self):
        self.api_key = MARKET_API_CONFIG["api_key"]
        self.base_url = MARKET_API_CONFIG["base_url"]
    
    def get_crop_prices(self, crop_name: str, location: Dict) -> Dict:
        """Get current market prices for crops"""
        # Mock market data
        market_data = {
            "wheat": {
                "current_price": 2200,  # Rs per quintal
                "trend": "stable",
                "demand": "high",
                "supply": "adequate"
            },
            "mustard": {
                "current_price": 5200,  # Rs per quintal
                "trend": "rising",
                "demand": "very_high",
                "supply": "limited"
            }
        }
        
        return market_data.get(crop_name.lower(), {
            "current_price": 0,
            "trend": "unknown",
            "demand": "unknown",
            "supply": "unknown"
        })
    
    def get_market_advice(self, crop_name: str, quantity: float, location: Dict) -> Dict:
        """Provide market-based recommendations"""
        price_data = self.get_crop_prices(crop_name, location)
        
        advice = {
            "sell_now": False,
            "hold": False,
            "price_expectation": "stable",
            "reasoning": ""
        }
        
        if crop_name.lower() == "wheat":
            if price_data["trend"] == "stable" and price_data["demand"] == "high":
                advice["sell_now"] = True
                advice["reasoning"] = "Good demand and stable prices - favorable selling conditions"
            else:
                advice["hold"] = True
                advice["reasoning"] = "Consider holding for better prices"
        
        elif crop_name.lower() == "mustard":
            if price_data["trend"] == "rising" and price_data["demand"] == "very_high":
                advice["sell_now"] = True
                advice["reasoning"] = "Excellent market conditions - high demand and rising prices"
            else:
                advice["hold"] = True
                advice["reasoning"] = "Market conditions suggest holding for better prices"
        
        return advice

class AgriculturalKnowledgeTool:
    """Tool providing agricultural knowledge and best practices"""
    
    def get_crop_management_advice(self, crop_name: str, stage: str, weather_condition: str) -> Dict:
        """Get crop-specific management advice based on stage and weather"""
        
        knowledge_base = {
            "wheat": {
                "flowering": {
                    "normal_weather": [
                        "Ensure adequate irrigation",
                        "Monitor for pests like aphids",
                        "Apply balanced fertilizer if needed"
                    ],
                    "extreme_heat": [
                        "Increase irrigation frequency",
                        "Apply light irrigation during peak heat",
                        "Monitor for heat stress symptoms",
                        "Consider foliar application of nutrients"
                    ],
                    "heavy_rainfall": [
                        "Ensure proper drainage",
                        "Monitor for fungal diseases",
                        "Apply preventive fungicide",
                        "Avoid heavy irrigation"
                    ]
                }
            },
            "mustard": {
                "pod_formation": {
                    "normal_weather": [
                        "Maintain moderate irrigation",
                        "Monitor for white rust",
                        "Apply micronutrients if needed"
                    ],
                    "extreme_heat": [
                        "Apply light irrigation to reduce heat stress",
                        "Monitor for pod abortion",
                        "Consider shade netting if available"
                    ],
                    "heavy_rainfall": [
                        "Ensure drainage to prevent waterlogging",
                        "Monitor for fungal diseases",
                        "Apply preventive fungicide"
                    ]
                }
            }
        }
        
        crop_data = knowledge_base.get(crop_name.lower(), {})
        stage_data = crop_data.get(stage, {})
        weather_advice = stage_data.get(weather_condition, ["Monitor crop health regularly"])
        
        return {
            "recommendations": weather_advice,
            "crop": crop_name,
            "stage": stage,
            "weather_condition": weather_condition
        }

# Create LangChain tools
weather_tool_instance = WeatherTool()
market_tool_instance = MarketTool()
agri_knowledge_tool_instance = AgriculturalKnowledgeTool()

def get_weather_tool():
    return Tool(
        name="weather_analyzer",
        description="Analyze weather conditions and their impact on crops",
        func=lambda location: weather_tool_instance.get_current_weather(location)
    )

def get_market_tool():
    return Tool(
        name="market_analyzer", 
        description="Get market prices and trends for agricultural products",
        func=lambda crop, location: market_tool_instance.get_crop_prices(crop, location)
    )

def get_agri_knowledge_tool():
    return Tool(
        name="agricultural_knowledge",
        description="Get crop-specific management advice based on growth stage and weather",
        func=lambda crop, stage, weather: agri_knowledge_tool_instance.get_crop_management_advice(crop, stage, weather)
    )

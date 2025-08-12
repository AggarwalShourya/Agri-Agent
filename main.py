<<<<<<< HEAD
#!/usr/bin/env python
import json
import warnings
import tempfile
from datetime import datetime
from agri_project.crew import AgriProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the Pest Management Crew with a hardcoded example scenario from the paper.
    """
    # Example from Table 1 in the paper
    scenario_data = {
        "Pest": "Beet Cyst Nematode",
        "Infestation Severity": "1 egg and larvae per gram of soil",
        "Crop Name": "Sugar Beet",
        "Crop Growth Stage": "Seedling",
        "Temperature": "15°C",
        "Weather": "Overcast",
        "Humidity": "75%",
        "Precipitation": "20mm",
        "Time": "April",
        "Location": "Lincolnshire"
    }

    # Save to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w")
    json.dump(scenario_data, temp_file, indent=2)
    temp_file.close()

    # Hardcoded paths for example scenario & PMA template
    example_path = "data/example_scenario.json"
    example_pma_path = "data/example_pma.md"

    inputs = {
        "query_path": temp_file.name,
        "example_path": example_path,
        "example_pma_path": example_pma_path,
        "current_year": str(datetime.now().year)
    }

    try:
        AgriProject().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
=======
#!/usr/bin/env python3
"""
Agricultural AI Advisor - Main Application
Handles user queries and provides comprehensive agricultural advice
"""

import os
import sys
from agents import AgriculturalAgentSystem
from config import FARMER_CONTEXT

def print_farmer_context():
    """Display the current farmer context"""
    print("\n" + "="*60)
    print("FARMER CONTEXT (KHC Data)")
    print("="*60)
    print(f"Name: {FARMER_CONTEXT['name']}")
    print(f"Location: {FARMER_CONTEXT['location']['village']}, {FARMER_CONTEXT['location']['district']}, {FARMER_CONTEXT['location']['state']}")
    print(f"Experience: {FARMER_CONTEXT['experience_years']} years")
    print(f"Soil Type: {FARMER_CONTEXT['soil_type']}")
    print(f"Irrigation: {FARMER_CONTEXT['irrigation_type']}")
    print(f"Financial Status: {FARMER_CONTEXT['financial_status']['income_level']} income, {FARMER_CONTEXT['financial_status']['savings']} savings")
    print("\nCROPS:")
    for crop in FARMER_CONTEXT['crops']:
        print(f"  - {crop['name']}: {crop['area']}, Stage: {crop['current_stage']}, Health: {crop['health_status']}")
    print("\nEQUIPMENT:")
    for equipment in FARMER_CONTEXT['equipment']:
        print(f"  - {equipment}")
    print("="*60)

def test_queries():
    """Test the system with predefined queries"""
    
    # Initialize the agricultural agent system
    print("Initializing Agricultural AI Advisor...")
    agri_system = AgriculturalAgentSystem()
    
    # Test Query 1: Sudden weather change
    print("\n" + "="*80)
    print("TEST QUERY 1: Sudden Weather Change")
    print("="*80)
    query1 = "The weather has suddenly changed from sunny to extremely rainy and my crops may not withstand the potential damage. What should I do?"
    print(f"Query: {query1}")
    
    print("\nProcessing query with multi-agent system...")
    print("(This may take a few moments as agents analyze the situation)")
    
    try:
        result1 = agri_system.get_advice(query1)
        print("\n" + "="*60)
        print("COMPREHENSIVE ADVICE")
        print("="*60)
        print(result1)
    except Exception as e:
        print(f"Error processing query: {e}")
    
    # Test Query 2: Crop damage scenario
    print("\n" + "="*80)
    print("TEST QUERY 2: Crop Damage Scenario")
    print("="*80)
    query2 = "I have crops Wheat and Mustard. Unfortunately, due to sudden hot and dry weather for the last 5 days, 30% of Wheat could not withstand and are dead while Mustard is standing strong. Both crops' harvest cycles are 2 weeks to go. What should I do?"
    print(f"Query: {query2}")
    
    print("\nProcessing query with multi-agent system...")
    print("(This may take a few moments as agents analyze the situation)")
    
    try:
        result2 = agri_system.get_advice(query2)
        print("\n" + "="*60)
        print("COMPREHENSIVE ADVICE")
        print("="*60)
        print(result2)
    except Exception as e:
        print(f"Error processing query: {e}")

def interactive_mode():
    """Run the system in interactive mode for user queries"""
    
    print("\n" + "="*60)
    print("AGRICULTURAL AI ADVISOR - INTERACTIVE MODE")
    print("="*60)
    print("Type your agricultural query and press Enter.")
    print("Type 'quit' to exit.")
    print("Type 'context' to see farmer information.")
    print("="*60)
    
    # Initialize the agricultural agent system
    agri_system = AgriculturalAgentSystem()
    
    while True:
        try:
            user_input = input("\nEnter your query: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'context':
                print_farmer_context()
                continue
            elif not user_input:
                continue
            
            print(f"\nProcessing: {user_input}")
            print("Analyzing with multi-agent system...")
            
            result = agri_system.get_advice(user_input)
            
            print("\n" + "="*60)
            print("AI ADVISOR RESPONSE")
            print("="*60)
            print(result)
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

def main():
    """Main function to run the agricultural AI advisor"""
    
    print("🌾 AGRICULTURAL AI ADVISOR 🌾")
    print("Multi-Agent System for Agricultural Decision Support")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  WARNING: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key:")
        print("   Windows: set OPENAI_API_KEY=your_api_key_here")
        print("   Linux/Mac: export OPENAI_API_KEY=your_api_key_here")
        print("\nThe system will use mock data for demonstration purposes.")
    
    # Display farmer context
    print_farmer_context()
    
    # Ask user for mode
    print("\nChoose mode:")
    print("1. Run test queries (predefined scenarios)")
    print("2. Interactive mode (enter your own queries)")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            test_queries()
            break
        elif choice == "2":
            interactive_mode()
            break
        else:
            print("Please enter 1 or 2.")

if __name__ == "__main__":
    main()
>>>>>>> 888773fcdc5c0da7fea85b92f2c0cce86fe9e38b

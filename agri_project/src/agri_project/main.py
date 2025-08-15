#!/usr/bin/env python
import warnings
from datetime import datetime
from agri_project.crew import AgriProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the Pest Management Crew with a hardcoded problem statement."""
    inputs = {
    "problem_statement": {
        "pest": "Brown Planthopper (Nilaparvata lugens)",
        "infestation_severity": "1 hoppers per hill",
        "crop_name": "Rice",
        "crop_growth_stage": "Panicle initiation to booting",
        "temperature": "28°C",
        "weather": "Overcast with intermittent showers",
        "humidity": "85%",
        "precipitation": "50 mm",
        "time": "August (Kharif season)",
        "location": "Tamil Nadu (e.g., Cauvery Delta)"
      },
    "current_year": str(datetime.now().year)
}

    AgriProject().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

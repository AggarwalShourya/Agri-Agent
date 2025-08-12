#!/usr/bin/env python
import warnings
from datetime import datetime
from agri_project.crew import AgriProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the Pest Management Crew with a hardcoded problem statement."""
    inputs = {
    "problem_statement": {
        "Pest": "Free-Living Nematodes",
        "InfestationSeverity": "800 Trichodorus nematodes per litre of soil",
        "CropName": "Sugar Beet",
        "CropGrowthStage": "Early root development",
        "Temperature": "12°C",
        "Weather": "Partly cloudy",
        "Humidity": "75%",
        "Precipitation": "30 mm",
        "Time": "May",
        "Location": "Norfolk"
    },
    "current_year": str(datetime.now().year)
}

    AgriProject().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

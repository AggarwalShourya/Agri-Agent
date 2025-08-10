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

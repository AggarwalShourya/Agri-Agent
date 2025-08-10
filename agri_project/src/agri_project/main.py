#!/usr/bin/env python
import warnings
from datetime import datetime
from agri_project.crew import AgriProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the Pest Management Crew with a hardcoded problem statement."""
    inputs = {
        "problem_statement": (
            "Beet Cyst Nematode infestation in Sugar Beet seedlings in Lincolnshire, "
            "April, 15°C, overcast, 75% humidity, 20mm precipitation, severity: "
            "1 egg and larvae per gram of soil. Provide a detailed pest management "
            "advice document for this situation."
        ),
        "current_year": str(datetime.now().year)
    }

    AgriProject().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

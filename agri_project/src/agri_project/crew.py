from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

@CrewBase
class AgriProject():
    """PestMA-inspired Multi-Agent Crew for Pest Management"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # --- Agents ---
    @agent
    def editor(self) -> Agent:
        """Agronomist: Generates and customises PMA"""
        return Agent(
            config=self.agents_config['editor'],  # matches agents.yaml key
            verbose=True
        )

    @agent
    def retriever(self) -> Agent:
        """Research Specialist: Finds external data to fill gaps"""
        return Agent(
            config=self.agents_config['retriever'],  # matches agents.yaml key
            verbose=True,
            tools=[Webse]
        )

    @agent
    def validator(self) -> Agent:
        """Managing Editor: Validates PMA correctness and thresholds"""
        return Agent(
            config=self.agents_config['validator'],  # matches agents.yaml key
            verbose=True
        )

    # --- Tasks ---
    @task
    def generate_initial_pma(self) -> Task:
        return Task(
            config=self.tasks_config['generate_initial_pma']
        )

    @task
    def make_customisation_plan(self) -> Task:
        return Task(
            config=self.tasks_config['make_customisation_plan']
        )

    @task
    def knowledge_retrieval(self) -> Task:
        return Task(
            config=self.tasks_config['knowledge_retrieval']
        )

    @task
    def generate_customised_pma(self) -> Task:
        return Task(
            config=self.tasks_config['generate_customised_pma']
        )

    @task
    def validate_threshold(self) -> Task:
        return Task(
            config=self.tasks_config['validate_threshold'],
            output_file='validated_pma.md'
        )

    # --- Crew ---
    @crew
    def crew(self) -> Crew:
        """Creates the AgriProject crew for pest management workflow"""
        return Crew(
            agents=self.agents,  # built from @agent decorators
            tasks=self.tasks,    # built from @task decorators
            process=Process.sequential,  # Editor → Retriever → Validator
            verbose=True
        )

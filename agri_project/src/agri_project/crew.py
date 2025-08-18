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
from crewai_tools import RagTool
from embedchain import App  
from embedchain.config import AppConfig  
import os
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage
from crewai.knowledge.knowledge import Knowledge
from crewai_tools import RagTool


from crewai import LLM

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
llm = LLM(
    model="gemini/gemini-2.0-flash-lite",
    temperature=0.2,

)

# custom_storage = KnowledgeStorage(
#     embedder={
#         "provider": "google",
#         "config": {"model": "models/embedding-001",
#                    "api_key":""
#                    }
#     },
#     collection_name="my_custom_knowledge"
# )

pdf_source = PDFKnowledgeSource(
    file_paths=["cd4890en.pdf"]
)
# pdf_source.storage=custom_storage

# my_knowledge = Knowledge(
#     sources=[pdf_source],
#     storage=custom_storage,
#     collection_name="my_custom_knowledge"
# )



# Create a RAG tool with custom configuration
config = {
    "llm": {
        "provider": "google",
        "config": {
            "model": "gemini/gemini-2.0-flash-lite",
            "temperature":0.5,
            "top_p":0.5,

        }
    },
    "embedding_model": {
        "provider": "google",
        "config": {
            "model": "models/embedding-001"
        }
    },
    "vectordb": {
        "provider": "chroma",
        "config": {
            "collection_name": "my-collection",
            "dir":"db"
        }
    },
    "chunker": {
        "chunk_size": 600,
        "chunk_overlap": 100,
        "length_function": "len",
        "min_chunk_size": 120
    }
}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
pdf_path = os.path.join(BASE_DIR, "knowledge", "cd4890en.pdf")

@CrewBase
class AgriProject():
    """PestMA-inspired Multi-Agent Crew for Pest Management"""

    agents: List[BaseAgent]
    tasks: List[Task]


    serper_tool = SerperDevTool(api_key=os.getenv('SERPER_API_KEY'))
    rag_tool = RagTool(config=config, summarize=False)
    rag_tool.add(source=pdf_path, data_type="pdf_file")

    # embedchain_config = {
    #     'embedder': {
    #         'provider': 'google',
    #         'config': {
    #             'model': 'models/text-embedding-004',  # Gemini embedding model
    #             'api_key': ""
    #         }
    #     }
    # }
    # embedchain_app = App.from_config(config=embedchain_config)
    # website_search_tool = WebsiteSearchTool(app=embedchain_app)
    # --- Agents ---
    @agent
    def editor(self) -> Agent:
        """Agronomist: Generates and customises PMA"""
        return Agent(
            config=self.agents_config['editor'],  # matches agents.yaml key
            verbose=True,
            knowledge_sources=[pdf_source],
            embedder={
                   "provider": "google",
                    "config": {
                    "model": "models/embedding-001",
                    "api_key":os.getenv("GEMINI_API_KEY")
                   }
            },
            llm=llm
        )

    @agent
    def retriever(self) -> Agent:
        """Retrieval Specialist: Finds external data to fill gaps. With the help of two agents provided the following agent specialises in
        minimising the knowledge gap between a generic answer and a """
        return Agent(
            config=self.agents_config['retriever'],  # matches agents.yaml key
            verbose=True,
            tools=[self.serper_tool],
            llm=llm
        )

    @agent
    def validator(self) -> Agent:
        """Managing Editor: Validates PMA correctness and thresholds"""
        return Agent(
            config=self.agents_config['validator'],  # matches agents.yaml key
            verbose=True,
            tools=[self.serper_tool],
            llm=llm
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


# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from crewai.agents.agent_builder.base_agent import BaseAgent
# from typing import List
# from crewai_tools import (
#     # DirectoryReadTool,
#     # FileReadTool,
#     SerperDevTool,
#     WebsiteSearchTool, 
#     ScrapeWebsiteTool
# )
# from .tools.custom_tool import PdfExtractorTool
# from embedchain import App  
# from embedchain.config import AppConfig  
# # import google.generativeai as genai
# # from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from crewai import LLM

# api_key="AIzaSyAdeQr4U7g0gLjcSZGi0zbcWDhhYvGz42Q"
# @CrewBase
# class AgriProject():
#     """PestMA-inspired Multi-Agent Crew for Pest Management"""

#     agents: List[BaseAgent]
#     tasks: List[Task]

#     # Configure embedchain for Gemini
#     # if not os.getenv('GEMINI_API_KEY'):
#     #     raise ValueError("GEMINI_API_KEY not found in environment")  # ADD: Validate key
        
#     # Configure embedchain for Gemini
#     # embedchain_config = AppConfig(embedder=GeminiEmbedder(api_key=os.getenv('GEMINI_API_KEY')))
#     # embedchain_app = App(config=embedchain_config)
#     # Configure embedchain for Gemini/Google
#     # embedchain_config = {
#     #     'embedder': {
#     #         'provider': 'google',
#     #         'config': {
#     #             'model': 'models/text-embedding-004',  # Gemini embedding model
#     #             'api_key': "AIzaSyAdeQr4U7g0gLjcSZGi0zbcWDhhYvGz42Q"
#     #         }
#     #     }
#     # }
#     # embedchain_config=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
#     # embedchain_app = App.from_config(config=embedchain_config,api_key=api_key)

#     # alternately one could instantiate the tools in agent constructor itself
#     serper_tool = SerperDevTool(api_key="907fcae3c8a3fb8c61ee6e5833476d0e9138761e")
#     # website_search_tool = WebsiteSearchTool(app=embedchain_app)
#     scrape_website_tool = ScrapeWebsiteTool()
#     pdf_extractor_tool = PdfExtractorTool()

#     # --- Agents ---
#     @agent
#     def editor(self) -> Agent:
#         """Agronomist: Generates and customises PMA"""
#         return Agent(
#             config=self.agents_config['editor'],  # matches agents.yaml key
#             verbose=True, 
#             tools=[]
#         )

#     @agent
#     def retriever(self) -> Agent:
#         """Research Specialist: Finds external data to fill gaps"""
#         return Agent(
#             config=self.agents_config['retriever'],  # matches agents.yaml key
#             verbose=True, 
#             tools=[self.serper_tool,  self.pdf_extractor_tool]
#         )

#     @agent
#     def validator(self) -> Agent:
#         """Managing Editor: Validates PMA correctness and thresholds"""
#         return Agent(
#             config=self.agents_config['validator'],  # matches agents.yaml key
#             verbose=True, 
#             tools=[self.serper_tool, self.scrape_website_tool, self.pdf_extractor_tool]
#         )

#     # --- Tasks ---
#     @task
#     def generate_initial_pma(self) -> Task:
#         return Task(
#             config=self.tasks_config['generate_initial_pma']
#         )

#     @task
#     def make_customisation_plan(self) -> Task:
#         return Task(
#             config=self.tasks_config['make_customisation_plan']
#         )

#     @task
#     def knowledge_retrieval(self) -> Task:
#         return Task(
#             config=self.tasks_config['knowledge_retrieval']
#         )

#     @task
#     def generate_customised_pma(self) -> Task:
#         return Task(
#             config=self.tasks_config['generate_customised_pma']
#         )

#     @task
#     def validate_threshold(self) -> Task:
#         return Task(
#             config=self.tasks_config['validate_threshold'],
#             output_file='validated_pma.md'
#         )

#     # --- Crew ---
#     @crew
#     def crew(self) -> Crew:
#         """Creates the AgriProject crew for pest management workflow"""
#         return Crew(
#             agents=self.agents,  # built from @agent decorators
#             tasks=self.tasks,    # built from @task decorators
#             process=Process.sequential,  # Editor → Retriever → Validator
#             verbose=True, 
#             memory=True,
#             llm=gemini_llm 
#         )


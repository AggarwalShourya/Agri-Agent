from crewai import Agent, Task, Crew, Process, LLM
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from tools import WeatherTool, MarketTool, AgriculturalKnowledgeTool
from config import FARMER_CONTEXT
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize tools
weather_tool = WeatherTool()
market_tool = MarketTool()
agri_knowledge_tool = AgriculturalKnowledgeTool()

# Initialize LLM
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.1,
    google_api_key=os.getenv("GEMINI_API_KEY")
)
# llm = LLM(model="gemini/gemini-2.0-flash", provider="vertex_ai")

# llm = Ollama(model="llama3.2")

class AgriculturalAgentSystem:
    def __init__(self):
        self.farmer_context = FARMER_CONTEXT
        self.setup_agents()
    
    def setup_agents(self):
        """Initialize all specialized agents"""
        
        # Weather Analysis Agent
        self.weather_agent = Agent(
            role='Weather and Climate Specialist',
            goal='Analyze weather conditions and their impact on agricultural operations',
            backstory="""You are an expert meteorologist specializing in agricultural weather. 
            You understand how weather patterns affect crop growth, disease risk, and farming operations. 
            You provide actionable weather-based recommendations for farmers.""",
            llm=llm,
            verbose=False
        )
        
        # Crop Management Agent
        self.crop_agent = Agent(
            role='Crop Management Specialist',
            goal='Provide crop-specific advice based on growth stage and environmental conditions',
            backstory="""You are an agricultural expert with deep knowledge of crop physiology, 
            growth stages, and management practices. You understand how different weather conditions 
            affect crops at various growth stages and provide practical management recommendations.""",
            llm=llm,
            verbose=False
        )
        
        # Market Analysis Agent
        self.market_agent = Agent(
            role='Agricultural Market Analyst',
            goal='Analyze market conditions and provide selling/holding recommendations',
            backstory="""You are an agricultural economist who understands market dynamics, 
            price trends, and supply-demand factors. You help farmers make informed decisions 
            about when to sell their produce and how to maximize their returns.""",
            llm=llm,
            verbose=False
        )
        
        # Risk Assessment Agent
        self.risk_agent = Agent(
            role='Agricultural Risk Assessment Specialist',
            goal='Evaluate risks and provide mitigation strategies for agricultural operations',
            backstory="""You are a risk management expert specializing in agriculture. 
            You assess various risks including weather, market, and crop health risks. 
            You provide strategies to minimize losses and maximize farmer resilience.""",
            llm=llm,
            verbose=False
        )
        
        # Orchestrator Agent
        self.orchestrator = Agent(
            role='Agricultural Advisor Coordinator',
            goal='Coordinate multiple specialists to provide comprehensive agricultural advice',
            backstory="""You are a senior agricultural advisor who coordinates multiple specialists 
            to provide comprehensive advice to farmers. You synthesize information from weather, 
            crop, market, and risk specialists to provide actionable recommendations.""",
            llm=llm,
            verbose=False
        )
    
    def create_tasks(self, user_query):
        """Create tasks for the crew based on user query"""
        
        # Task 1: Analyze weather conditions
        weather_task = Task(
            description=f"""
            Analyze the weather conditions mentioned in the user query: "{user_query}"
            
            Farmer Context:
            - Location: {self.farmer_context['location']}
            - Crops: {[crop['name'] for crop in self.farmer_context['crops']]}
            
            Provide detailed weather analysis including:
            1. Current weather impact on crops
            2. Weather forecast implications
            3. Weather-related risks and recommendations
            """,
            agent=self.weather_agent,
            expected_output="Detailed weather analysis with specific recommendations"
        )
        
        # Task 2: Assess crop management needs
        crop_task = Task(
            description=f"""
            Based on the user query: "{user_query}"
            
            Farmer's Crops:
            {json.dumps(self.farmer_context['crops'], indent=2)}
            
            Provide crop-specific management advice including:
            1. Current crop health assessment
            2. Growth stage-specific recommendations
            3. Management practices for current conditions
            4. Recovery strategies if damage is mentioned
            """,
            agent=self.crop_agent,
            expected_output="Comprehensive crop management recommendations"
        )
        
        # Task 3: Analyze market implications
        market_task = Task(
            description=f"""
            Analyze market implications for the situation described: "{user_query}"
            
            Farmer's Crops: {[crop['name'] for crop in self.farmer_context['crops']]}
            Financial Status: {self.farmer_context['financial_status']}
            
            Provide market analysis including:
            1. Current market conditions for affected crops
            2. Price trends and demand analysis
            3. Selling/holding recommendations
            4. Financial impact assessment
            """,
            agent=self.market_agent,
            expected_output="Market analysis with selling/holding recommendations"
        )
        
        # Task 4: Risk assessment
        risk_task = Task(
            description=f"""
            Assess overall risks for the situation: "{user_query}"
            
            Consider:
            1. Crop damage risks
            2. Financial risks
            3. Weather-related risks
            4. Market risks
            
            Provide comprehensive risk assessment and mitigation strategies.
            """,
            agent=self.risk_agent,
            expected_output="Risk assessment with mitigation strategies"
        )
        
        # Task 5: Synthesize final recommendations
        synthesis_task = Task(
            description=f"""
            Synthesize all specialist analyses into a comprehensive recommendation for the farmer.
            
            User Query: "{user_query}"
            
            Consider all inputs from weather, crop, market, and risk specialists.
            Provide:
            1. Immediate action items (next 24-48 hours)
            2. Short-term strategies (next week)
            3. Long-term considerations
            4. Financial implications
            5. Risk mitigation steps
            
            Make recommendations practical and actionable for the farmer's specific situation.
            """,
            agent=self.orchestrator,
            expected_output="Comprehensive, actionable agricultural advice"
        )
        
        return [weather_task, crop_task, market_task, risk_task, synthesis_task]
    
    def get_advice(self, user_query):
        """Get comprehensive agricultural advice for a user query"""
        
        # Create tasks
        tasks = self.create_tasks(user_query)
        
        # Create crew
        crew = Crew(
            agents=[self.weather_agent, self.crop_agent, self.market_agent, self.risk_agent, self.orchestrator],
            tasks=tasks,
            process=Process.sequential,
            verbose=False
        )
        
        # Execute crew
        result = crew.kickoff()
        
        return result
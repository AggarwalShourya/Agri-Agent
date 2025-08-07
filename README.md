# 🌾 Agricultural AI Advisor

A multi-agent AI system designed to provide comprehensive agricultural advice to farmers in India. The system addresses complex agricultural queries by coordinating specialized agents for weather analysis, crop management, market analysis, and risk assessment.

## 🎯 Problem Statement

Agriculture is a high-impact area of Indian society that requires continuous innovation and experimentation with data, analytics, and AI/ML. This system addresses key challenges:

- **Multilingual Support**: Handles queries in local languages
- **Multi-modal Input**: Text, audio, and image inputs
- **Real-time Data**: Weather, market, and policy information
- **Contextual Advice**: Personalized recommendations based on farmer profile
- **Offline Capability**: Works with limited internet access
- **Explainable AI**: Provides reasoning for recommendations

## 🏗️ Architecture

### Multi-Agent System

The system uses CrewAI to coordinate specialized agents:

1. **Weather Agent**: Analyzes weather conditions and their impact on crops
2. **Crop Management Agent**: Provides crop-specific advice based on growth stages
3. **Market Agent**: Analyzes market conditions and pricing trends
4. **Risk Assessment Agent**: Evaluates risks and provides mitigation strategies
5. **Orchestrator Agent**: Coordinates all specialists for comprehensive advice

### Data Flow

```
User Query → Translation Layer → Multi-Agent System → Response Generation → User Output
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (optional for demo)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agricultural-ai-advisor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 📋 Usage

### Test Queries

The system comes with two predefined test scenarios:

1. **Sudden Weather Change**: "The weather has suddenly changed from sunny to extremely rainy and my crops may not withstand the potential damage. What should I do?"

2. **Crop Damage Scenario**: "I have crops Wheat and Mustard. Unfortunately, due to sudden hot and dry weather for the last 5 days, 30% of Wheat could not withstand and are dead while Mustard is standing strong. Both crops' harvest cycles are 2 weeks to go. What should I do?"

### Interactive Mode

Run the system in interactive mode to test your own queries:

```bash
python main.py
# Choose option 2 for interactive mode
```

## 🧪 Demo Farmer Profile

The system uses a hardcoded farmer profile for demonstration:

- **Name**: Rajesh Kumar
- **Location**: Sikandarpur, Muzaffarpur, Bihar
- **Crops**: Wheat (2 acres), Mustard (1.5 acres)
- **Experience**: 15 years
- **Financial Status**: Medium income, limited savings
- **Equipment**: Tractor, irrigation pump, sprayer, harvester

## 🔧 Configuration

### Farmer Context (KHC Data)

Edit `config.py` to modify the farmer profile:

```python
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
            "current_stage": "flowering",
            "health_status": "good"
        }
    ],
    # ... more configuration
}
```

### API Integration

The system supports real API integration for:

- **Weather Data**: OpenWeatherMap API
- **Market Data**: Agricultural market APIs
- **Policy Data**: Government scheme APIs

Configure APIs in `config.py`:

```python
WEATHER_API_CONFIG = {
    "base_url": "https://api.openweathermap.org/data/2.5/",
    "api_key": os.getenv("WEATHER_API_KEY", "")
}
```

## 🛠️ Technical Details

### Tools and Libraries

- **CrewAI**: Multi-agent orchestration
- **LangChain**: LLM integration and tool management
- **OpenAI GPT-3.5**: Language model for reasoning
- **Python-dotenv**: Environment variable management

### Agent Specializations

#### Weather Agent
- Analyzes current weather conditions
- Provides weather forecasts
- Assesses weather impact on crops
- Recommends weather-based actions

#### Crop Management Agent
- Provides crop-specific advice
- Considers growth stages
- Recommends management practices
- Suggests recovery strategies

#### Market Agent
- Analyzes market prices and trends
- Provides selling/holding recommendations
- Assesses demand-supply dynamics
- Considers financial implications

#### Risk Assessment Agent
- Evaluates crop damage risks
- Assesses financial risks
- Provides mitigation strategies
- Considers farmer's risk tolerance

## 🎯 Key Features

### 1. Contextual Understanding
- Uses farmer profile (KHC data) for personalized advice
- Considers location, crops, equipment, and financial status

### 2. Multi-Domain Analysis
- Weather impact assessment
- Crop health monitoring
- Market condition analysis
- Risk evaluation

### 3. Actionable Recommendations
- Immediate action items (24-48 hours)
- Short-term strategies (next week)
- Long-term considerations
- Financial implications

### 4. Explainable AI
- Provides reasoning for recommendations
- Shows data sources
- Explains risk factors
- Offers alternatives

## 🔮 Future Enhancements

### Planned Features

1. **Multilingual Support**
   - Hindi, English, and regional language support
   - Voice input/output capabilities

2. **Real-time Data Integration**
   - Live weather API integration
   - Real-time market data
   - Government policy updates

3. **Mobile Application**
   - Android/iOS app development
   - Offline capability
   - Image recognition for crop health

4. **Advanced Analytics**
   - Predictive modeling for crop yields
   - Machine learning for personalized recommendations
   - Historical data analysis

5. **Community Features**
   - Farmer-to-farmer knowledge sharing
   - Expert consultation integration
   - Local market information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- CrewAI team for the multi-agent framework
- OpenAI for language model capabilities
- Agricultural experts for domain knowledge
- Indian farming community for insights and feedback

---

**Note**: This is a hackathon project demonstrating the potential of AI in agriculture. For production use, additional testing, validation, and real data integration would be required.

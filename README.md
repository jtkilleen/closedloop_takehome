# Medical Diagnostic Agent - Take Home Assignment

A sophisticated multi-agent medical diagnostic system built with Google's Agent Development Kit (ADK). This system conducts empathetic medical interviews, systematically collects symptoms, and provides appropriate care recommendations while prioritizing patient safety.

## 🏥 Overview

This take-home assignment demonstrates the implementation of a **hierarchical multi-agent system** using Google ADK's advanced features. The system showcases:

- **Multi-Agent Architecture**: Specialized agents working together for medical assessment
- **Intelligent Tool Integration**: Custom medical knowledge and risk assessment tools
- **Safety-First Design**: Built-in safeguards and emergency detection
- **Professional Medical Interview Flow**: Systematic symptom collection and analysis

## 🏗️ Architecture

### Multi-Agent System Design

```bash
Medical Interview Coordinator (Root Agent)
├── Symptom Collector Agent
│   ├── Medical Knowledge Lookup Tool
│   └── Symptom Clarification Tool
└── Risk Assessment Agent
    ├── Patient Risk Assessment Tool
    ├── Care Recommendations Tool
    └── Symptom Pattern Analysis Tool
```

### Key ADK Features Demonstrated

1. **LLMAgent with Dynamic Reasoning**: Intelligent decision-making using Gemini 2.0
2. **Hierarchical Agent Structure**: Parent-child relationships with specialized sub-agents  
3. **Tool Integration**: Custom medical tools seamlessly integrated with agents
4. **State Management**: Patient information persistence across agent interactions
5. **Session Handling**: Consistent conversation context throughout the interview

## 🚀 Quick Start

### Option 1: Docker (Recommended)

#### Prerequisites

- Docker and Docker Compose installed
- Google API Key for Gemini models

#### Quick Start with Docker

1. **Set up environment:**

   ```bash
   # Create .env file with your API key
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

2. **Build and run:**

   ```bash
   docker-compose up --build
   ```

### Option 2: Local Development

#### Prerequisites

- Python 3.10 or higher
- Google API Key for Gemini models
- `uv` package manager (recommended) or `pip`

#### Installation

1. **Clone and navigate to the project:**

   ```bash
   cd closedloop_takehome
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Set up Google API authentication:**

   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

#### Running the Application

##### Using ADK Command

```bash
# Run the medical diagnostic agent
adk web
```

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
pytest
```

### Test Coverage

The test suite includes:

- **Unit Tests**: Individual component testing (tools, agents)
- **Integration Tests**: Multi-component interaction testing
- **System Tests**: End-to-end workflow validation
- **Error Handling Tests**: Edge cases and error scenarios

## 📁 Project Structure

```bash
closedloop_takehome/
├── medical_diagnostic_agent/         # Main package
│   ├── agent.py                      # Agent implementations
│   ├── tools/                        # Custom medical tools
│   │   ├── medical_knowledge.py      # Medical lookup and analysis
│   │   ├── patient_lookup.py         # Patient data retrieval
│   │   └── risk_assessment.py        # Risk evaluation and recommendations
│   └── data/                         # Medical data and knowledge base
│       ├── mock_medical_data.py      # Simplified medical knowledge
│       ├── patient_records.py        # Patient record management
│       └── patients.json             # Patient data storage
├── tests/                            # Comprehensive test suite
│   ├── test_medical_knowledge.py     # Medical tools tests
│   ├── test_risk_assessment.py       # Risk assessment tests
│   ├── test_agents.py                # Agent configuration tests
│   ├── test_patient_lookup.py        # Patient lookup tests
│   └── conftest.py                   # Test fixtures and configuration
├── pyproject.toml                    # Project configuration
├── uv.lock                           # Dependency lock file
├── Dockerfile                        # Docker container definition
├── docker-compose.yml                # Docker Compose configuration
├── .dockerignore                     # Docker build exclusions
├── .flake8                           # Code formatting configuration
├── .python-version                   # Python version specification
└── README.md                         # This file
```

## 🔧 Key Components

### 1. Medical Interview Coordinator (Root Agent)

- **Purpose**: Main orchestrator and patient interface
- **Responsibilities**:
  - Warm, professional greeting with disclaimers
  - Patient identification and record lookup
  - Delegating to specialized sub-agents
  - Synthesizing findings into clear summaries
  - Ensuring patient safety throughout the process
- **Tools**: `list_available_patients` for patient directory access

### 2. Enhanced Symptom Collector Agent

- **Purpose**: Systematic symptom gathering with patient history integration
- **Tools Used**:
  - `lookup_medical_conditions`: Identifies possible conditions from symptoms
  - `lookup_patient_record`: Retrieves existing patient information
  - `get_patient_medical_history`: Accesses detailed medical background
  - `onboard_new_patient`: Adds new patients to the system
- **Approach**: Uses medical interview best practices with personalized context

### 3. Enhanced Risk Assessment Agent  

- **Purpose**: Safety evaluation with patient history integration
- **Tools Used**:
  - `assess_patient_risk`: Evaluates urgency based on symptoms and demographics
  - `generate_care_recommendations`: Provides specific next steps and timelines
  - `check_patient_risk_factors`: Incorporates existing patient risk factors
  - `save_visit_summary`: Records consultation for future reference
  - `update_patient_lifestyle`: Updates patient lifestyle information

### 4. Enhanced Patient Records System

- **JSON-based Storage**: Patient data stored in `medical_diagnostic_agent/data/patients.json`
- **Patient Database**: Stores comprehensive patient profiles including:
  - Demographics (age, occupation)
  - Lifestyle factors (work environment, exercise, sleep, stress)
  - Medical history and risk factors
  - Clinical notes and previous visits
- **Pre-loaded Personas**: Sarah (Software Engineer), Robert (Construction Foreman), Emma (Teacher), Margaret (Retired)
- **Dynamic Onboarding**: New patients can be added to the system automatically
- **Persistent Records**: All patient data persists between sessions

### 5. Medical Knowledge Tools

- **Condition Lookup**: Maps symptoms to possible medical conditions
- **Risk Stratification**: Implements triage logic for care level determination
- **Red Flag Detection**: Identifies symptoms requiring immediate attention
- **Patient Lookup**: Provides personalized medical context

## 🎯 Enhanced Demonstration Scenarios

### Scenario 1: Sarah's Computer-Related Headache

- **Patient**: Sarah, 28, Software Engineer
- **Input**: "Hi, I'm Sarah and I have a persistent headache"
- **Agent Response**:
  - Looks up Sarah's record
  - References her long computer hours and high caffeine intake
  - Provides ergonomic recommendations
  - Suggests caffeine reduction strategies

### Scenario 2: Robert's Post-Smoking Cough

- **Patient**: Robert, 55, Construction Foreman  
- **Input**: "I'm Robert and I have a lingering cough"
- **Agent Response**:
  - Accesses smoking cessation history (quit 6 months ago)
  - Factors in 20-year smoking background
  - Recommends closer monitoring due to risk factors
  - Suggests chest imaging consideration

### Scenario 3: Emma's Chronic Fatigue

- **Patient**: Emma, 34, Elementary School Teacher
- **Input**: "I'm Emma and I'm exhausted all the time"
- **Agent Response**:
  - References chronic sleep deprivation (5-6 hours nightly)
  - Considers high stress from work and parenting
  - Provides sleep hygiene counseling
  - Addresses stress management strategies

### Scenario 4: Margaret's Joint Pain

- **Patient**: Margaret, 72, Retired
- **Input**: "I'm Margaret and my joints hurt from gardening"
- **Agent Response**:
  - Notes her active lifestyle through gardening
  - Considers age-related factors
  - Provides activity modification suggestions
  - Addresses fall prevention concerns

### Scenario 5: New Patient Onboarding

- **Input**: "Hi, I'm Alex and I'm new here"
- **Agent Response**:
  - Offers to onboard as new patient
  - Collects age, occupation, and lifestyle information
  - Creates permanent patient record
  - Proceeds with personalized consultation

## 💡 ADK Features Highlighted

### 1. Multi-Agent Coordination

```python
root_agent = LlmAgent(
    name="medical_interviewer",
    model="gemini-2.0-flash", 
    sub_agents=[symptom_agent, risk_agent],
    instruction="Coordinate medical interview workflow..."
)
```

### 2. Dynamic Tool Selection

```python
symptom_agent = LlmAgent(
    tools=[lookup_medical_conditions, get_symptom_clarification_questions],
    instruction="Use tools based on conversation context..."
)
```

### 3. State Management

- Patient information persists across agent interactions
- Context-aware responses based on previously gathered data
- Session continuity throughout the medical interview

### 4. Safety-First Design

- Built-in medical disclaimers
- Emergency condition detection
- Escalation protocols for high-risk symptoms

## 🔍 Technical Implementation Details

### Agent Communication Pattern

1. **Root Agent** receives patient query
2. **Delegates** to Symptom Collector for detailed symptom gathering
3. **Delegates** to Risk Assessor for safety evaluation  
4. **Synthesizes** findings into comprehensive assessment
5. **Provides** clear next steps and recommendations

### Tool Integration Strategy

- Tools are **stateless functions** that can be called by any agent
- **Structured responses** with consistent status/error handling
- **Medical knowledge** separated from agent logic for maintainability

### Error Handling Approach

- Graceful degradation for missing or invalid data
- **Conservative bias** toward higher care levels when uncertain
- Comprehensive input validation and sanitization

## 🔮 Potential Extensions

For a production system, consider adding:

- **Real medical database** integration (ICD-10, SNOMED CT)
- **EHR system** connectivity
- **Advanced NLP** for symptom extraction
- **Multi-language** support
- **Accessibility** features
- **Audit logging** and compliance features
- **Provider handoff** workflows

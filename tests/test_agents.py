"""
Unit tests for agent creation and configuration.
"""

import pytest
from medical_diagnostic_agent.agent import symptom_collector, risk_assessor, root_agent


class TestSymptomCollectorAgent:
    """Test the symptom collector agent creation and configuration."""

    def test_agent_creation(self):
        """Test that symptom collector agent is created successfully."""
        agent = symptom_collector

        assert agent is not None
        assert agent.name == "symptom_collector"
        assert agent.model == "gemini-2.0-flash"
        assert (
            agent.description
            == "Collects and analyzes patient symptoms with access to patient records"
        )

    def test_agent_has_tools(self):
        """Test that symptom collector agent has the required tools."""
        agent = symptom_collector

        assert len(agent.tools) > 0
        tool_names = [
            tool.__name__ for tool in agent.tools if hasattr(tool, "__name__")
        ]
        assert "lookup_medical_conditions" in tool_names
        assert "lookup_patient_record" in tool_names

    def test_agent_instruction_content(self):
        """Test that symptom collector agent has appropriate instructions."""
        agent = symptom_collector

        instruction = agent.instruction.lower()
        assert "symptom" in instruction
        assert "collect" in instruction
        assert "empathetic" in instruction
        assert "professional" in instruction


class TestRiskAssessmentAgent:
    """Test the risk assessment agent creation and configuration."""

    def test_agent_creation(self):
        """Test that risk assessment agent is created successfully."""
        agent = risk_assessor

        assert agent is not None
        assert agent.name == "risk_assessor"
        assert agent.model == "gemini-2.0-flash"
        assert agent.description == (
            "Assesses patient risk with access to patient records and saves "
            "visit summaries"
        )

    def test_agent_has_tools(self):
        """Test that risk assessment agent has the required tools."""
        agent = risk_assessor

        assert len(agent.tools) > 0
        tool_names = [
            tool.__name__ for tool in agent.tools if hasattr(tool, "__name__")
        ]
        assert "assess_patient_risk" in tool_names
        assert "generate_care_recommendations" in tool_names
        assert "check_patient_risk_factors" in tool_names

    def test_agent_instruction_content(self):
        """Test that risk assessment agent has appropriate instructions."""
        agent = risk_assessor

        instruction = agent.instruction.lower()
        assert "risk" in instruction
        assert "assessment" in instruction
        assert "emergency" in instruction
        assert "safety" in instruction


class TestMedicalInterviewAgent:
    """Test the medical interview (root) agent creation and configuration."""

    def test_agent_creation(self):
        """Test that medical interview agent is created successfully."""
        agent = root_agent

        assert agent is not None
        assert agent.name == "medical_interviewer"
        assert agent.model == "gemini-2.0-flash"
        assert (
            agent.description
            == "Main coordinator for medical interviews with patient record access"
        )

    def test_agent_has_sub_agents(self):
        """Test that medical interview agent has the required sub-agents."""
        agent = root_agent

        assert len(agent.sub_agents) == 2
        sub_agent_names = [sub_agent.name for sub_agent in agent.sub_agents]
        assert "symptom_collector" in sub_agent_names
        assert "risk_assessor" in sub_agent_names

    def test_agent_instruction_content(self):
        """Test that medical interview agent has appropriate instructions."""
        agent = root_agent

        instruction = agent.instruction.lower()
        assert "medical interview" in instruction
        assert "coordinator" in instruction
        assert "empathetic" in instruction
        assert "professional" in instruction
        assert "disclaimer" in instruction
        assert "emergency" in instruction

    def test_agent_instruction_includes_disclaimers(self):
        """Test that medical interview agent includes important disclaimers."""
        agent = root_agent

        instruction = agent.instruction
        assert "NOT a substitute for professional medical advice" in instruction
        assert "call 911" in instruction
        assert "qualified healthcare professionals" in instruction

    def test_agent_instruction_includes_workflow(self):
        """Test that medical interview agent includes workflow instructions."""
        agent = root_agent

        instruction = agent.instruction.lower()
        assert "symptom_collector" in instruction
        assert "risk_assessor" in instruction
        assert "delegate" in instruction
        assert "synthesize" in instruction


class TestAgentIntegration:
    """Test that agents work together properly."""

    def test_all_agents_have_consistent_models(self):
        """Test that all agents use the same model for consistency."""
        symptom_agent = symptom_collector
        risk_agent = risk_assessor
        root_agent_obj = root_agent

        assert symptom_agent.model == "gemini-2.0-flash"
        assert risk_agent.model == "gemini-2.0-flash"
        assert root_agent_obj.model == "gemini-2.0-flash"

    def test_sub_agents_are_properly_configured(self):
        """Test that sub-agents in root agent are properly configured."""
        root_agent_obj = root_agent

        # Check that sub-agents are the same type as individually created agents
        symptom_agent = symptom_collector
        risk_agent = risk_assessor

        sub_agent_names = [agent.name for agent in root_agent_obj.sub_agents]
        assert symptom_agent.name in sub_agent_names
        assert risk_agent.name in sub_agent_names

    def test_agents_have_unique_names(self):
        """Test that all agents have unique names."""
        symptom_agent = symptom_collector
        risk_agent = risk_assessor
        root_agent_obj = root_agent

        names = [symptom_agent.name, risk_agent.name, root_agent_obj.name]
        assert len(names) == len(set(names))  # All names should be unique

    def test_agents_have_appropriate_descriptions(self):
        """Test that all agents have meaningful descriptions."""
        symptom_agent = symptom_collector
        risk_agent = risk_assessor
        root_agent_obj = root_agent

        agents = [symptom_agent, risk_agent, root_agent_obj]

        for agent in agents:
            assert agent.description is not None
            assert len(agent.description) > 10  # Should have meaningful description
            assert agent.description != ""

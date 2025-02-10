from dataclasses import dataclass

from langgraph.graph.state import CompiledStateGraph

from agents.bg_task_agent.bg_task_agent import bg_task_agent
from agents.chatbot import chatbot
from agents.research_assistant import research_assistant
from agents.default_agent import default_agent
# from agents.tutor_agent import tutor_agent
# from agents.roadmap_agent import roadmap_agent
# from agents.resource_agent import resource_agent
# from agents.quiz_agent import quiz_agent
from schema import AgentInfo

DEFAULT_AGENT = "research-assistant"


@dataclass
class Agent:
    description: str
    graph: CompiledStateGraph


agents: dict[str, Agent] = {
    "chatbot": Agent(description="A simple chatbot.", graph=chatbot),
    "research-assistant": Agent(
        description="A research assistant with web search and calculator.", graph=research_assistant
    ),
    "default-agent": Agent(description="A default agent.", graph=default_agent),
    # "tutor-agent": Agent(description="A tutor agent.", graph=tutor_agent),
    # "roadmap-agent": Agent(description="A roadmap agent.", graph=roadmap_agent),
    # "resource-agent": Agent(description="A resource agent.", graph=resource_agent),
    # "quiz-agent": Agent(description="A quiz agent.", graph=quiz_agent),
    "bg-task-agent": Agent(description="A background task agent.", graph=bg_task_agent),
}


def get_agent(agent_id: str) -> CompiledStateGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]

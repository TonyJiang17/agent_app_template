import math
import re

import numexpr
from langchain_core.tools import BaseTool, tool

from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg, tool, InjectedToolCallId
from langgraph.types import Command, interrupt
from typing_extensions import Annotated

#from react_agent.configuration import ConfigurationDefault

from database import Database
from schema.models_new import (
    Roadmap, Topic, SubTopic
)
from datetime import datetime
import json

db = Database()


def calculator_func(expression: str) -> str:
    """Calculates a math expression using numexpr.

    Useful for when you need to answer questions about math using numexpr.
    This tool is only for math questions and nothing else. Only input
    math expressions.

    Args:
        expression (str): A valid numexpr formatted math expression.

    Returns:
        str: The result of the math expression.
    """

    try:
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
        return re.sub(r"^\[|\]$", "", output)
    except Exception as e:
        raise ValueError(
            f'calculator("{expression}") raised error: {e}.'
            " Please try again with a valid numerical expression"
        )


calculator: BaseTool = tool(calculator_func)
calculator.name = "Calculator"

# def search(
#     query: str, *, config: RunnableConfig
# ) -> Optional[list[dict[str, Any]]]:
#     """Search for general web results.

#     This function performs a search using the Tavily search engine, which is designed
#     to provide comprehensive, accurate, and trusted results. It's particularly useful
#     for answering questions about current events.
#     """
#     configuration = config.get("configurable", {})
#     wrapped = TavilySearchResults(max_results=configuration.max_search_results)
#     result = wrapped.invoke({"query": query})
#     return cast(list[dict[str, Any]], result)

# search_tool: BaseTool = tool(search)
# search_tool.name = "Search_Tool"

def create_roadmap(
    title: str,
    description: str,
    topics_json: str,  # JSON string containing list of topics 
    #tool_call_id: Annotated[str, InjectedToolCallId]
) -> str: 
    """Create a new roadmap
    
    The topics_json argument should be a JSON string representing a list of dictionaries with this structure:
    [
        {
            "name": "Python Basics",
            "subtopics": [
                {"name": "Variables and Data Types"},
                {"name": "Basic Operators"},
                {"name": "Control Flow (if/else)"}
            ]
        },
        {
            "name": "Data Structures",
            "subtopics": [
                {"name": "Lists and Arrays"},
                {"name": "Dictionaries"},
                {"name": "Sets and Tuples"}
            ]
        }
    ]
    """
    # Parse JSON string to list of dicts
    topics_data = json.loads(topics_json)
    
    # Convert dictionaries to Topic models
    topic_models = [
        Topic(
            name=topic["name"],
            subtopics=[SubTopic(name=subtopic["name"], completed=False) for subtopic in topic["subtopics"]],
            completed=False
        )
        for topic in topics_data
    ]
    
    roadmap = Roadmap(
        title=title,
        description=description,
        topics=topic_models,
        created_at=datetime.now()
    )
    roadmap_id = db.create_roadmap(roadmap)
    # state_udpate = {
    #     "messages": [ToolMessage(f'roadmap {roadmap_id} has been created', tool_call_id=tool_call_id)]
    # }
    #return Command(update=state_udpate)
    return f'roadmap {roadmap_id} has been created'

create_roadmap_tool: BaseTool = tool(create_roadmap)
create_roadmap_tool.name = "Create_Roadmap_Tool"

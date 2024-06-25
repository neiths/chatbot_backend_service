from langchain_core.agents import AgentAction, AgentFinish

from langgraph.prebuilt.tool_executor import ToolExecutor
from api.langgraph.agent_runnable import tools_for_literature, tools_for_math, tools_for_supervisor 
from api.langgraph.agent_runnable import literature_agent_runnable, math_agent_runnable, supervisor_agent_runnable


def supervisor_agent_node(node_data):
    print("supervisor_agent_node")
    agent_outcome = supervisor_agent_runnable.invoke(node_data)
    node_data["agent_outcome"] = agent_outcome
    node_data["last_node_name"] = "supervisor_agent_node"
    return node_data

def supervisor_select_tool_node(node_data):
    print("supervisor_select_tool_node")
    tool_input = node_data['agent_outcome']
    tool_outcome = ToolExecutor(tools_for_supervisor).invoke(tool_input)
    node_data["intermediate_steps"] = [(tool_input, str(tool_outcome))]
    print("------tool_outcome:-------------", tool_outcome)
    node_data['next_role'] = tool_outcome
    return node_data

def supervisor_role_navigator(node_data):
    if node_data['next_role'] == 'math':
        return "math_agent_role"
    elif node_data['next_role'] == 'literature':
        return "literature_agent_role"
    else:
        return "end"

def math_agent_node(node_data):
    print("math_agent_node")
    agent_outcome = math_agent_runnable.invoke(node_data)
    node_data["agent_outcome"] = agent_outcome
    node_data["last_node_name"] = "math_agent_node"
    return node_data

def calculator_tool_node(node_data):
    print("calculator_tool_node")
    tool_input = node_data["agent_outcome"]
    tool_outcome = ToolExecutor(tools_for_math).invoke(tool_input)
    node_data["intermediate_steps"] = [(tool_input, str(tool_outcome))]
    return node_data
    
def literature_agent_node(node_data):
    print("literature_agent_node")
    agent_outcome = literature_agent_runnable.invoke(node_data)
    node_data["agent_outcome"] = agent_outcome
    node_data["last_node_name"] = "literature_agent_node"
    return node_data

def wiki_tool_node(node_data):
    print("wiki_tool_node")
    tool_input = node_data["agent_outcome"]
    tool_outcome = ToolExecutor(tools_for_literature).invoke(tool_input)
    node_data["intermediate_steps"] = [(tool_input, str(tool_outcome))]
    return node_data

def decision_node(node_data):
    if isinstance(node_data['agent_outcome'], AgentFinish):
        print("decision_node end")
        return "end"
    else:
        print("decision_node continue")
        return "continue"
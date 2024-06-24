from langchain_core.agents import AgentAction, AgentFinish

from langgraph.prebuilt.tool_executor import ToolExecutor
from api.langgraph.agent_runnable import agent_runnbale, tools_for_graph

tool_executor = ToolExecutor(tools_for_graph)

def agent_node(node_data):
    print("agent_node: \n")
    print(node_data)
    print(node_data["decision_retry_count"])
    node_data["decision_retry_count"] += 1
    agent_outcome = agent_runnbale.invoke(node_data)
    node_data['agent_outcome'] = agent_outcome
    return node_data

def tool_node(node_data):
    print("tool_node \n")
    print(node_data)
    tool_input = node_data['agent_outcome']
    tool_outcome = tool_executor.invoke(tool_input)
    #node_data["intermediate_steps"] = [(tool_input, str(tool_outcome))]
    return node_data

def decision_node(node_data):
    print("decision_node \n")
    if node_data["decision_retry_count"] <= 2:
        print("stop the loop")
        return "end"
    print(node_data)
    if isinstance(node_data['agent_outcome'], AgentFinish):
        print("decision_node end")
        return "end"
    
    else:
        print("decision_node continue")
        return "continue"
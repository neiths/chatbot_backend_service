from langgraph.graph import END, StateGraph
from api.langgraph.graph_state import AgentState
from api.langgraph.agent_node import *

def define_workflow(entry_point:str = None):

    # declare Stategraph
    workflow = StateGraph(AgentState)

    # add nodes
    workflow.add_node("math_agent_node", math_agent_node)
    workflow.add_node("calculator_tool_node", calculator_tool_node)
    
    workflow.add_node("literature_agent_node", literature_agent_node)
    workflow.add_node("wiki_tool_node", wiki_tool_node)
    
    #workflow.add_node("decision_node", decision_node)
    
    workflow.add_node("supervisor_agent_node", supervisor_agent_node)
    workflow.add_node("supervisor_select_tool_node", supervisor_select_tool_node)
    #workflow.add_node("supervisor_role_navigator", supervisor_role_navigator)

    # add egdes
    workflow.add_conditional_edges("supervisor_agent_node", decision_node,
                                {
                                            "continue": "supervisor_select_tool_node",
                                            "end": END,
                                })

    workflow.add_conditional_edges("supervisor_select_tool_node", supervisor_role_navigator,
                                {
                                            "math_agent_role": "math_agent_node",
                                            "literature_agent_role": "literature_agent_node",
                                            "end": END,
                                })

    workflow.add_conditional_edges("math_agent_node", decision_node,
                                {
                                            "continue": "calculator_tool_node",
                                            "end": END,  
                                })
    workflow.add_edge("calculator_tool_node", "math_agent_node")

    workflow.add_conditional_edges("literature_agent_node", decision_node,
                                {
                                            "continue": "wiki_tool_node",
                                            "end": END,
                                })
    workflow.add_edge("wiki_tool_node", "literature_agent_node")

    if entry_point:
        workflow.set_entry_point(entry_point)
    else:
        workflow.set_entry_point("supervisor_agent_node")

    app = workflow.compile()
    return app

app_workflow = define_workflow()

output = app_workflow.invoke({"input": "hãy tính cho tui 2 cộng 2 bằng bao nhiêu", "chat_history": []})
print(output['agent_outcome'])
print(output['last_node_name'])
#print(output)

from langgraph.graph import END, StateGraph
from api.langgraph.graph_state import AgentState
from api.langgraph.agent_node import agent_node, tool_node, decision_node

workflow = StateGraph(AgentState)

workflow.add_node("agent_node", agent_node)

workflow.add_node("tool_node", tool_node)

workflow.add_conditional_edges("agent_node", decision_node,
                               {
                                        "continue": "tool_node",
                                        "end": END,
                               })


workflow.add_edge("tool_node", "agent_node")

workflow.set_entry_point("agent_node")

app = workflow.compile()

output = app.invoke({"input": "who is the author of Manga Naruto", "chat_history": [], "decision_retry_count": 0})

print(output)

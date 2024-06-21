# create llm -L> prompt -> tool
from api.chat_service.chatbot import load_llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from api.chat_service.tool_basic import tools

llm = load_llm(llm_provider="google")

system_prompt_content=("You are a helpful assistant. I can help you with information from wikipedia."
                       "You can call tool function 'get_info_from_wikipedia' to get information from wikipedia with input: 'get_info_from_wikipedia('search term')")

system_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt_content
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# create agent construct = func(llm, tools, prompt)
#agent = create_tool_calling_agent(llm, tools, system_prompt)

# agent executor
def load_agent_executor(llm, tools, system_prompt):
    agent = create_tool_calling_agent(llm, tools, system_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

#agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#output = agent_executor.invoke({"input": "search for me manga Hunter x Hunter", "chat_history": []})

#print(output)
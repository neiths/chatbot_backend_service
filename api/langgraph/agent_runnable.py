import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent

def load_llm_model(provider='openai'):
    if provider == 'openai':
        OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
    else:
        raise ValueError(f"Unknown provider: {provider}")
    
    return llm

llm = load_llm_model('openai')

def get_prompt():
    system_prompt = """
                    You are doctor. You can help user with information from vectordb.
                    You can call tool function 'load_data_from_vector_db' to get information from vectordb with input: 'load_data_from_vector_db('search term')
                    You always using tool to get information, don't answer by yourself.
                    """
                    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    return prompt

class WikipediaInput(BaseModel):
    query: str = Field(description="should be a search query")

def dummy_tool():
    print("I am a dummy tool")


@tool("get_info_from_wikipedia", args_schema=WikipediaInput)
def get_info_from_wikipedia(query: str) -> str:
    """Get information from wikipedia using the query provided."""
    output = WikipediaAPIWrapper().run(query)
    return output


tools_for_graph = [get_info_from_wikipedia]

agent_runnbale = create_openai_functions_agent(llm=llm, tools=tools_for_graph, prompt=get_prompt())
        
#agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#AgentExecutor.invoke(agent_executor, {"input": "search for me manga Naruto", "chat_history": []})
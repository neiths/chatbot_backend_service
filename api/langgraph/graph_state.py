import operator
from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # the input string
    input : str
    
    # the list of previous messages in the conversation
    chat_history : list[BaseMessage]
    
    # the outcome of a given call to the aget
    # Needs None as a valid type, since this is what this will start as
    agent_outcome : Union[AgentAction, AgentFinish, None] # agent_outcome: str
    # list of actions and corresponding observations
    # here we annotate this with operator.add to indicate that operations to
    # this state should be ADDED to the existing values (not overwrite it)
    
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    decision_retry_count: int
    
    
    
    

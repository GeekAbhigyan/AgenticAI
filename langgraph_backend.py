from langgraph.graph import StateGraph , START , END
from typing import TypedDict , Annotated 
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage , HumanMessage , SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.environ.get("PERPLEXITY_API_KEY")

llm = ChatOpenAI(
    api_key=api_key,
    base_url="https://api.perplexity.ai",
    model="sonar" 
      # or another supported Perplexity model
)

from langgraph.graph.message import add_messages
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage] , add_messages]

def chat_node(state: ChatState):
    #take user query 
    messages = state['messages']
    #send to llm 
    response = llm.invoke(messages)

    # response store state 
    return {"messages": [response]}

checkpointer = MemorySaver()

#create the graph 
graph = StateGraph(ChatState)

# add nodes 
graph.add_node('chat_node',chat_node)

# add edges 
graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

# execute the graph 

chatbot = graph.compile(checkpointer=checkpointer)

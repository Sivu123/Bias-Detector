from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState
from typing import  Annotated
import operator
from openai import OpenAI
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
import base64
import streamlit as st
import os

import prompts as pt

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

MAX_RESULTS = 5

# set the openai model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# create client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# tavily search
tavily_search = TavilySearchResults(max_results = MAX_RESULTS)
class BotState(MessagesState):
    context: list[str]
    answers: str


def search_web(state:BotState):
  hot_topic = state["messages"]
  search_docs = tavily_search.invoke(pt.SEARCH_QUERY.format(topic = hot_topic))
  formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
  return {"context": [formatted_search_docs]}  

def bias_indentifier(state:BotState,config:RunnableConfig):
    topic_docs = state["context"]
    system_message = [SystemMessage(pt.BIAS_QUERY.format(documents = topic_docs))]

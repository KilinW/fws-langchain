from typing import List
from dotenv import load_dotenv
import os

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
from langserve import add_routes

load_dotenv()

# 1. Load Retriever (PDF)
loader = PyPDFLoader('./sample/The Design Philosophy of the DARPA Internet Protocols.pdf')
pages = loader.load_and_split()
faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
retriever = faiss_index.as_retriever()
# docs = faiss_index.similarity_search("What is the design philosophy of DARPA Internet Protocols?", k=2)
# for doc in docs:
#   print(str(doc.metadata["page"]) + ":", doc.page_content[:100])

# Web Base Load Example
# loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
# docs = loader.load()
# text_splitter = RecursiveCharacterTextSplitter()
# documents = text_splitter.split_documents(docs)
# embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
# vector = FAISS.from_documents(documents, embeddings)
# retriever = vector.as_retriever()

# 2. Create Tools
retriever_tool = create_retriever_tool(
  retriever,
  "internet_protocols_search",
  "Search for information about Internet Protocols. For any questions about Internet Protocols, you must use this tool!",
)
search = TavilySearchResults()
tools = [retriever_tool, search]


# 3. Create Agent
prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.

class Input(BaseModel):
  input: str
  chat_history: List[BaseMessage] = Field(
    ...,
    extra={"widget": {"type": "chat", "input": "location"}},
  )


class Output(BaseModel):
  output: str

add_routes(
  app,
  agent_executor.with_types(input_type=Input, output_type=Output),
  path="/agent",
)

if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="localhost", port=8000)
from typing import List
from dotenv import load_dotenv
import os

from fastapi import FastAPI, Body
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub, HuggingFaceHub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
from langchain.chains.question_answering import load_qa_chain
from langserve import add_routes

from utils.io import Input, Output, ChatRequest

load_dotenv()

# 1. Load Retriever (PDF)
loader = PyPDFLoader('./sample/Construction Safety Standards.pdf')
text_spilter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
pages = loader.load_and_split(text_splitter=text_spilter)
# embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
embeddings = HuggingFaceEmbeddings()
faiss_index = FAISS.from_documents(pages, embeddings)
retriever = faiss_index.as_retriever()

# 2. Create Tools (Retriever, Memory, Search)
retriever_tool = create_retriever_tool(
  retriever,
  "internet_protocols_search",
  "Search for information about Internet Protocols. For any questions about Internet Protocols, you must use this tool!",
)
search = TavilySearchResults()
tools = [retriever_tool, search]


# 3. Create Agent
# prompt = hub.pull("hwchase17/openai-functions-agent")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm = HuggingFaceHub(
  repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
  model_kwargs={"temperature":0.2, "max_length":1000},
)
chain = load_qa_chain(llm, chain_type="stuff")

# query = "工人是否可以喝酒?"
# query = "工作場所的高度高於多少需要定義墜落災害防止計畫?"


# docs = faiss_index.similarity_search(query, k=2)
# for doc in docs:
#   print(doc)

# ans = chain.run(input_documents=docs, question=query)
# print("Ans", ans)

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

@app.post("/agent/")
async def agent(request: ChatRequest) -> str:
  """Handle a request."""
  print(request.input)
  docs = faiss_index.similarity_search(request.input, k=2)
  res = chain.run(input_documents=docs, question=request.input)
  print(res)
  return res


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="localhost", port=8000)
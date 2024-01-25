from typing import List
from dotenv import load_dotenv
import os

from fastapi import FastAPI, Body
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain

from src.utils.io import ChatRequest

load_dotenv()

# 1. Load PDF
loader = PyPDFLoader('./sample/機台型號_ x-100.pdf')
text_spilter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
splits = loader.load_and_split(text_splitter=text_spilter)
# embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(splits, embeddings)
# retriever = vectorstore.as_retriever()

# 2. Design prompting
prompt = PromptTemplate(
   input_variables = ["input", "chat_history", "retrieved_document"],
   template="\
    你是一個場務知識的聊天機器人，你擅長根據Context和Chat History回答問題，\
    以下是Context、Chat History和問題，請你只針對該問題回答。\n\n\
    Context: {retrieved_document} \n\n\
    Chat History:\n{chat_history}\n\n\
    Question:{input} \n\
    Answer:",
)

def concatenate_retrived_docs(docs):
    return "\n\n".join(doc.page_content.replace("\n", "") for doc in docs)

def generate_chat_history(chat_history: List[str]) -> str:
    chat_history = ""
    for i in range(len(chat_history)):
        if i % 2 == 0:
            chat_history += "Human: " + chat_history[i] + "\n"
        else:
            chat_history += "AI: " + chat_history[i] + "\n"
    return chat_history

def create_chain(model: str, model_params: dict) -> LLMChain:
    print(f"//--------Loading model {model}...--------//")
    try:
      llm = HuggingFaceHub(
         repo_id=model,
         model_kwargs=model_params,
      )
      print(f"//--------Model {model} loaded.--------//")
    except:
      print(f"//--------Error: Model {model} not found.--------//")
      print("//--------Use default model: mistralai/Mixtral-8x7B-Instruct-v0.1--------//")
      llm = HuggingFaceHub(
         repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
         model_kwargs={"temperature":0.8, "max_length":1000},
      )
    
    chain = LLMChain(
      llm=llm,
      prompt=prompt,
    )
    return chain


app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

@app.post("/query/")
async def agent(request: ChatRequest) -> str:
  """Handle a request."""
  # Define LLM and chain
  chain = create_chain(request.model, request.model_params)

  # Retrieve document from retriever
  retrieved_document = concatenate_retrived_docs(vectorstore.similarity_search(request.input, k=2))

  # Convert chat history to string
  chat_history = generate_chat_history(request.chat_history)

  # Run the chain
  res = chain.run({
      "input": request.input,
      "chat_history": chat_history,
      "retrieved_document": retrieved_document
  })
  final_res = \
      f"""The model you are using: {chain.llm.repo_id}.\n\n\
      The model parameters: \n{chain.llm.model_kwargs}.\n\n\
      The input: \n{request.input}.\n\n\
      The AI's answer: \n{res}."""
  print(res)
  return final_res


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="localhost", port=8000)
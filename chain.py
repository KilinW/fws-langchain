import os
from langchain import hub
from langchain_community.llms import HuggingFaceHub
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from utils.io import prompt

def get_openai_llm(model: str="gpt-3.5-turbo"):
  return ChatOpenAI(model=model, temperature=0)

def get_huggingface_hub_llm(repo_id: str="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs: dict={"temperature":0.2, "max_length":1000}):
  return HuggingFaceHub(repo_id=repo_id, model_kwargs=model_kwargs)

def get_google_llm(model: str="gemini-pro"):
  pass

def get_chain(model: str, chain_type: str="stuff") -> LLMChain:
  try:
    if model == "gpt-3.5-turbo":
      llm = get_openai_llm(model)
    elif model == "gemini-pro":
      llm = ChatVertexAI(model_name="gemini-pro", project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"))
    else:
      llm = get_huggingface_hub_llm(model)
  except:
    raise Exception(f"Model {model} loading failed. Please check if the model is available.")
  
  chain = LLMChain(
    llm=llm,
    prompt=prompt
  )

  return chain
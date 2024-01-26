import os
from langchain import hub
from langchain_community.llms import HuggingFaceHub
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from utils.io import prompt

def get_openai_llm(model: str="gpt-3.5-turbo", model_params: dict={}):
  return ChatOpenAI(
    model_name=model,
    **model_params
  )

def get_huggingface_hub_llm(repo_id: str="mistralai/Mixtral-8x7B-Instruct-v0.1", model_params: dict={}):
  return HuggingFaceHub(
    repo_id=repo_id, 
    model_kwargs=model_params
  )

def get_google_llm(model: str="gemini-pro", model_params: dict={}):
  return ChatVertexAI(
    model_name=model, 
    project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
    **model_params
  )

def get_chain(model: str, model_params: dict={}) -> LLMChain:
  
  if model == "gpt-3.5-turbo":
    llm = get_openai_llm(model, model_params)
  elif model == "gemini-pro":
    llm = get_google_llm(model, model_params)
  else:
    llm = get_huggingface_hub_llm(model, model_params)
  
  chain = LLMChain(
    llm=llm,
    prompt=prompt
  )

  return chain
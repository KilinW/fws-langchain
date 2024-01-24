from langchain import hub, HuggingFaceHub
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

def get_openai_llm(model: str="gpt-3.5-turbo"):
  return ChatOpenAI(model=model, temperature=0)

def get_huggingface_hub_llm(repo_id: str="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs: dict={"temperature":0.2, "max_length":1000}):
  return HuggingFaceHub(repo_id=repo_id, model_kwargs=model_kwargs)

def get_google_llm(model: str="gemini-pro"):
  pass

def get_chain(model: str, chain_type: str="stuff"):
  if model == "gpt-3.5-turbo":
    llm = get_openai_llm()
  elif model == "mistralai/Mixtral-8x7B-Instruct-v0.1":
    llm = get_huggingface_hub_llm()
  elif model == "gemini-pro":
    llm = get_google_llm()
  return load_qa_chain(llm, chain_type=chain_type)

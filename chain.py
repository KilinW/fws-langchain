from langchain import hub, HuggingFaceHub
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain


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

def get_openai_llm(model: str="gpt-3.5-turbo"):
  return ChatOpenAI(model=model, temperature=0)

def get_huggingface_hub_llm(repo_id: str="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs: dict={"temperature":0.2, "max_length":1000}):
  return HuggingFaceHub(repo_id=repo_id, model_kwargs=model_kwargs)

def get_google_llm(model: str="gemini-pro"):
  pass

def get_chain(model: str, chain_type: str="stuff") -> LLMChain:
  if model == "gpt-3.5-turbo":
    llm = get_openai_llm(model)
  elif model == "mistralai/Mixtral-8x7B-Instruct-v0.1":
    llm = get_huggingface_hub_llm(model)
  elif model == "gemini-pro":
    llm = get_google_llm()

  
  chain = LLMChain(
    llm=llm,
    prompt=prompt
  )

  return chain

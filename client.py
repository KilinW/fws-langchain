from langserve import RemoteRunnable
from langchain_core.messages import AIMessage, HumanMessage
import requests


# remote_chain = RemoteRunnable("http://localhost:8000/agent/")
# response = remote_chain.invoke({
#   "input": "你好嗎？",
#   "chat_history": []
# })

response = requests.post("http://localhost:8000/query/", json={
  "input": "我叫什麼名字？",
  "chat_history": ["你好，我叫何宏發", "你好"],
  "model": "just testing",
  "model_params": {"temperature":0.8, "max_length":1000},
})
print(response)
print(response.content.decode("utf-8"))

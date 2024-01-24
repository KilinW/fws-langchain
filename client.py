from langserve import RemoteRunnable
from langchain_core.messages import AIMessage, HumanMessage
import requests

# remote_chain = RemoteRunnable("http://localhost:8000/agent/")
# response = remote_chain.invoke({
#   "input": "你好嗎？",
#   "chat_history": []
# })

response = requests.post("http://localhost:8000/agent/", json={
  "input": "hello",
  "chat_history": ""
})

print(response.content.decode("utf-8"))

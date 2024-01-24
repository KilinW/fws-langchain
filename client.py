from langserve import RemoteRunnable
import requests

response = requests.post("http://localhost:8000/agent/", json={
  "input": "請問x-100機台未啟動該如何解決?",
  "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
  "chat_history": []
})

print(response.content.decode("utf-8"))

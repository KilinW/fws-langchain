from langserve import RemoteRunnable
import requests

response = requests.post("http://localhost:8000/agent/", json={
  "input": "請問SH-5031機台的最大加工尺寸為何?",
  "model": "gpt-3.5-turbo",
  "chat_history": []
})

print(response.content.decode("utf-8"))

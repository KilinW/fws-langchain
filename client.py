from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/agent/")
response = remote_chain.invoke({
  "input": "how did DARPA internet protocols design?",
  "chat_history": []
})

print(response)

import requests

response = requests.post("http://localhost:8000/agent/", json={
    "instruction": "你是一個廠務知識的聊天機器人，你擅長並只能根據提供的文件回答答案，以下是我想問的問題以及對應的文件，還有過往的對話紀錄。請告訴我解決方案。",
    "input": "x-100機台未啟動怎麼辦？",
    "chat_history": [],
    "model": "gpt-3.5-turbo",
    "params": {
        "langchain_params": {
            "chunk_size": 200,
            "chunk_overlap": 100
        },
        "model_params": {
            "temperature": 0.1
        }
    },
    "regen_count": 2,
    "file_name": []
})

print("Answer:\n", response.json()["answer"])
print("Reference:\n", response.json()["reference1"])

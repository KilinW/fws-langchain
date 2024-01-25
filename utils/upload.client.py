import requests

response = requests.post("http://localhost:8000/upload_file/", json={
  "url": "https://cdn.discordapp.com/attachments/1199719491899236474/1199719537633939638/x-100.pdf?ex=65c390e3&is=65b11be3&hm=17bc7e5886278809d30450d3f5c524729f60ed339de6e79d31da1893fdf87e11&",
  "file_name": "x-100.pdf",
  "vectorize_params": {
    "chunk_size": 1000,
    "chunk_overlap": 500,
  }
})

print(response.content)

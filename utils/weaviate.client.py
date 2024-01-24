import weaviate
import weaviate.classes as wvc

# As of November 2023, WCS sandbox instances are not yet compatible with the new API introduced in the v4 Python client.
# This example connects to a local instance of Weaviate. You do not need to provide the Weaviate API key when local,
# anonymous, authentication is enabled.
client = weaviate.connect_to_local(
  port=8765,
  grpc_port=50051
)

sop = client.collections.create(
  "Sop",
  vectorizer_config=wvc.Configure.Vectorizer.text2vec_huggingface(),

  vector_index_config=wvc.Configure.vector_index(
    distance_metric=wvc.VectorDistance.COSINE
  ),
)

print(sop)

print(client)
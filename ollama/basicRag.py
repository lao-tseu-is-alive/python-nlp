from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

info =  """
This example demonstrates how to use a local Ollama model for question answering.
This is a bare minimum "Retrieval Augmented Generation" or RAG example build using LlamaIndex.
With the data inside the data folder, we use the Ollama model to answer questions about the text files.
https://docs.llamaindex.ai/en/stable/getting_started/starter_example_local/ 
"""

print(info)

documents = SimpleDirectoryReader("data").load_data()
print(f"## found {len(documents)} documents in the data folder")

print("## using BAAI/bge-base-en-v1.5 for embeddings")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
print("## using mistral-nemo for the LLM")
Settings.llm = Ollama(model="mistral-nemo", request_timeout=120.0, temperature=0.2)
print("## creating the index")
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
question = "What did the author do growing up?"
print(f"## asking the question: {question}")
print("You should get back a response similar to the following:\n The author wrote short stories and tried to program on an IBM 1401.\n...Waiting for the response....")
response = query_engine.query(question)
print(response)

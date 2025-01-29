#%%
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from config import CONFIG

#%% Deos
#!pip install unstructured
#!pip install -qU langchain_chroma
#!pip install python-magic python-magic-bin
#!pip install -qU langchain_ollama

#%% load docs
loader = DirectoryLoader(CONFIG.TUTO_PATH, glob="**/*.md")
documents = loader.load()

print("Loaded", len(documents), "documents")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

print(f"Loaded {len(docs)} document chunks")

# %%
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

local_embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_documents(documents=all_splits, embedding=local_embeddings)
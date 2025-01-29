#%%
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from config import CONFIG

#%% load docs
loader = DirectoryLoader(CONFIG.TUTO_PATH, glob="**/*.md")
documents = loader.load()

print("Loaded", len(documents), "documents")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

print(f"Loaded {len(docs)} document chunks")

# %%

# %%
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re
import numpy as np
from docProcessing import *
import torch
doc_embedded_path="embeddings\\doc_embedded.pt"
ref_embedded_path="embeddings\\ref_embedded.pt"
doc_text_path="embeddings\\doc_text.json"
ref_text_path="embeddings\\ref_text.json"

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
# %%
def penalize(x):
    return 100/(1+np.exp(0.003*(x-700)))
def query_related_titles(question,embedded_path,pure_texts,count=5):
    """Retrieve titles related to the input question based on embeddings similarity."""
    query_embedding = model.encode([question], convert_to_tensor=True).to("cpu")
    # Load embedded texts
    embedded_texts = torch.load(embedded_path)
    
    # embedded_texts = model.encode(pure_texts, convert_to_tensor=True).to("cpu")
    
    similarities = cosine_similarity(query_embedding,   embedded_texts)
    similarities = similarities * np.array([penalize(len(pure_texts[q])) for q in range(len(embedded_texts))])  # Penalize longer texts
    ranked_indices = similarities[0].argsort()[::-1]  # Sort in descending order

     # Adjust the number as needed
    return ranked_indices[:count]

def text_to_feed(doc_embedded_path,ref_embedded_path,pure_doc,pure_ref,question,countDocu=5,countRef=3):
    related_texts_doc_idx = query_related_titles(question,doc_embedded_path,pure_doc,countDocu)  
    related_texts_ref_idx = query_related_titles(question,ref_embedded_path,pure_ref,countRef)
    
    toFeed=""
    for idx in related_texts_doc_idx:
        text=pure_doc[idx]
        toFeed+="[[A piece of relevant grammar documentation:]]\n\n "+text+"\n\n"
    for idx in related_texts_ref_idx:
        text=pure_ref[idx]
        toFeed+="[[A piece of relevant function documentation:]]\n\n "+text+"\n\n"
    return toFeed
# Example usage
import warnings
def feed_to_RAG(question):
    warnings.filterwarnings("ignore")
    with open(doc_text_path, "r") as file:
        pure_doc = json.load(file)
    with open(ref_text_path, "r") as file:
        pure_ref = json.load(file)
    return text_to_feed(doc_embedded_path,ref_embedded_path,pure_doc,pure_ref,question)
import json
# %%
if __name__ == "__main__":
    question="How to use argmax in Envision?"
    information=feed_to_RAG(question)
    print(information,len(information))
# %%

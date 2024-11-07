# %%
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re
import numpy as np
from docProcessing import *

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
# %%
def penalize(x):
    return 100/(1+np.exp(0.003*(x-700)))
def query_related_titles(question,pure_texts,count=5):
    """Retrieve titles related to the input question based on embeddings similarity."""
    query_embedding = model.encode([question], convert_to_tensor=True).to("cpu")
    
    embedded_texts = model.encode(pure_texts, convert_to_tensor=True).to("cpu")
    
    similarities = cosine_similarity(query_embedding,   embedded_texts)
    similarities = similarities * (np.array([penalize(len(text)) for text in pure_texts]))  # Penalize longer texts
    ranked_indices = similarities[0].argsort()[::-1]  # Sort in descending order

    # Return top related titles based on similarity score
    top_texts = [pure_texts[idx] for idx in ranked_indices[:count]]  # Adjust the number as needed
    return top_texts

def text_to_feed(DocuFolder,RefFolder,question,countDocu=5,countRef=3):
    DOCU=process_markdown_folder(DocuFolder)
    pure_texts_doc=flatten_Dict(DOCU)
    related_texts = query_related_titles(question, pure_texts_doc,countDocu)

    REFE,pure_texts_ref=process_reference_folder(RefFolder)
    related_texts_ref = query_related_titles(question, pure_texts_ref,countRef)
    
    toFeed=""
    for text in related_texts:
        toFeed+="[[A piece of relevant grammar documentation:]]\n\n "+text+"\n\n"
    for text in related_texts_ref:
        toFeed+="[[A piece of relevant function documentation:]]\n\n "+text+"\n\n"
    return toFeed
# Example usage


# %%
if __name__ == "__main__":
    DocuFolder="docs"
    RefFolder="reference\\reference"
    question="How to use argmax in Envision?"
    toFeed=text_to_feed(DocuFolder,RefFolder,question)
    print(toFeed,len(toFeed))
# %%

# %%
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re
import numpy as np
from docProcessing import *

# Load your embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
# %%
def query_related_titles(question,pure_texts,count=5):
    """Retrieve titles related to the input question based on embeddings similarity."""
    query_embedding = model.encode([question], convert_to_tensor=True).to("cpu")
    
    embedded_texts = model.encode(pure_texts, convert_to_tensor=True).to("cpu")
  
    similarities = cosine_similarity(query_embedding,   embedded_texts)
    ranked_indices = similarities[0].argsort()[::-1]  # Sort in descending order

    # Return top related titles based on similarity score
    top_texts = [pure_texts[idx] for idx in ranked_indices[:count]]  # Adjust the number as needed
    return top_texts




# Example usage


# %%
if __name__ == "__main__":
    DOCU=process_markdown_folder('docs')
    pure_texts_doc=flatten_Dict(DOCU)
    question = "argmax of a coloumn in a table"
    related_texts = query_related_titles(question, pure_texts_doc,5)

    REFE,pure_texts_ref=process_reference_folder('reference')
    related_texts_ref = query_related_titles(question, pure_texts_ref,3)


    print("Related Titles:", related_texts,related_texts_ref)
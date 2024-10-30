# %%
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re
import numpy as np

# Load your embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# %%
def extract_titles_and_text(filepath):
    """Extract titles and associated paragraph text from a markdown file."""
    titles, paragraphs = [], []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.finditer(r'(^## .+)', content, re.MULTILINE)
        for match in matches:
            title = match.group(0).strip()
            start = match.end()
            end = next((m.start() for m in matches if m.start() > start), None)
            paragraph = content[start:end].strip() if end else content[start:].strip()
            titles.append(title)
            paragraphs.append(paragraph)
    return titles, paragraphs

def create_embeddings(folder_path):
    """Create embeddings for all titles and paragraphs in markdown files in a folder and its subfolders."""
    all_titles, all_paragraphs, embeddings = [], [], []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                titles, paragraphs = extract_titles_and_text(filepath)
                all_titles.extend(titles)
                all_paragraphs.extend(paragraphs)
                embeddings.extend(model.encode(titles, convert_to_tensor=True).to("cpu"))
    return all_titles, all_paragraphs, embeddings

def query_related_titles(question, all_titles, embeddings):
    """Retrieve titles related to the input question based on embeddings similarity."""
    query_embedding = model.encode([question], convert_to_tensor=True)
  
    similarities = cosine_similarity(query_embedding.to("cpu"), embeddings)
    ranked_indices = similarities[0].argsort()[::-1]  # Sort in descending order

    # Return top related titles based on similarity score
    top_titles = [all_titles[idx] for idx in ranked_indices[:5]]  # Adjust the number as needed
    return top_titles

# Example usage
folder_path = 'docs'
all_titles, all_paragraphs, embeddings = create_embeddings(folder_path)
question = "argmax of a list"
related_titles = query_related_titles(question, all_titles, embeddings)

print("Related Titles:", related_titles)


# %%
if __name__ == "__main__":
    pass
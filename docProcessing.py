from sentence_transformers import SentenceTransformer
import torch
import json
import os
import re

model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')

# Function to parse a single .md file


def parse_md_file(file_path):
    results = []
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Remove the front matter
    content = re.sub(r"\+\+\+.*?\+\+\+", "", content, flags=re.DOTALL).strip()

    # Find all subtitles (##) and subsubtitles (###) and their content
    sections = re.split(r"(## |### )", content)

    # If there is text before the first subtitle or subsubtitle, treat it as a paragraph
    if sections[0].strip():
        results.append(
            f"&Title: {os.path.basename(file_path)[:-3]} &Subtitle: Start &Content: {sections[0].strip()}")

    # Process each section
    for i in range(1, len(sections), 2):
        subtitle = sections[i] + sections[i + 1].splitlines()[0]
        content = "\n".join(sections[i + 1].splitlines()[1:]).strip()
        results.append(
            f"&Title: {os.path.basename(file_path)[:-3]} &Subtitle: {subtitle.strip()} &Content: {content if content else 'No content'}")

    return results


def parse_folder(folder_path):
    texts = []
    # Iterate through all .md files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".md"):
            results = parse_md_file(os.path.join(folder_path, file_name))
            texts.extend(results)
    return texts


def save_embedding(pure_texts, path_emb, path_text):
    clean_texts = [re.sub(r"```.*?```", "", text, flags=re.DOTALL)
                   for text in pure_texts]
    embedded_texts = model.encode(
        clean_texts, convert_to_tensor=True).to("cpu")  # embedded text is clean of code
    torch.save(embedded_texts, path_emb)
    with open(path_text, 'w') as f:
        json.dump(pure_texts, f)  # text is complete text, with code


def parse_refs(forder_path, path_emb, path_text):
    texts = []
    titles = []
    for file_name in os.listdir(forder_path):
        if file_name.endswith(".md"):
            with open(os.path.join(forder_path, file_name), "r", encoding="utf-8") as file:
                content = file.read()
            titles.append(file_name)
            texts.append(content)
    embedded_titltes = model.encode(
        titles, convert_to_tensor=True).to("cpu")
    torch.save(embedded_titltes, path_emb)
    with open(path_text, 'w') as f:
        json.dump(texts, f)
    return texts


# %%
if __name__ == "__main__":

    doc_texts = parse_folder("docs")
    save_embedding(doc_texts, "embeddings\\doc_embedded.pt",
                   "embeddings\\doc_text.json")
    ref_texts = parse_refs("reference\\reference", "embeddings\\ref_embedded.pt",
                           "embeddings\\ref_text.json")

    print("refs:", len(ref_texts), "docs", len(doc_texts))
    print(ref_texts[5])
# %%

# %%
import json
from sentence_transformers import SentenceTransformer
import os
import re
from collections import defaultdict
import torch


def parse_markdown(file_content):
    """
    Parses a markdown file content, extracting sections and subsections.
    Returns a dictionary structured as:
    {subtitle: {0: text_before_first_subsubtitle, subsubtitle: text, "ALL": full_text_of_subtitle_section}}.
    """
    doc_structure = defaultdict(lambda: {0: "", "ALL": ""})
    current_subtitle = None
    current_subsubtitle = None
    current_content = []
    subtitle_content = []

    for line in file_content.splitlines():
        if line.startswith("## "):  # New subtitle section
            # Save previous subtitle section
            if current_subtitle:
                # doc_structure[current_subtitle]["ALL"] = "\n".join(current_content).strip()
                doc_structure[current_subtitle][0] = "\n".join(
                    subtitle_content).strip()
            current_subtitle = line[3:].strip()  # Subtitle text
            current_subsubtitle = None
            current_content = []
            subtitle_content = []
            doc_structure[current_subtitle] = {
                0: "", "ALL": ""}  # Initialize new subtitle

        elif line.startswith("### "):  # New subsubtitle within a subtitle section
            # Save current subsubtitle's content if there was one
            if current_subsubtitle:
                doc_structure[current_subtitle][current_subsubtitle] = "\n".join(
                    current_content).strip()
            current_subsubtitle = line[4:].strip()  # Subsubtitle text
            current_content = []

        else:
            # Add line to both subtitle_content and current_content
            if current_subtitle is not None:
                subtitle_content.append(line)
            current_content.append(line)

    # Final save for the last section parsed
    if current_subtitle:
        doc_structure[current_subtitle]["ALL"] = "\n".join(
            current_content).strip()
        doc_structure[current_subtitle][0] = "\n".join(
            subtitle_content).strip()
        if current_subsubtitle:
            doc_structure[current_subtitle][current_subsubtitle] = "\n".join(
                current_content).strip()

    return dict(doc_structure)


def process_markdown_folder(folder_path):
    """
    Walks through folder and subfolders, processing each .md file into DOCU dictionary format.
    Returns dictionary DOCU structured as:
    {filename: {subtitle: {0: text_before_first_subsubtitle, subsubtitle: text, "ALL": full_text_of_subtitle_section}}}.
    """
    DOCU = {}

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    DOCU[file[:-3]] = parse_markdown(content)

    return DOCU


def process_reference_folder(folder_path):

    REFE = {}
    pure_texts_ref = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md") and not (file == "_index.md" and folder_path == "reference"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    REFE[file[:-3]] = content
                    pure_texts_ref.append(content)

    return REFE, pure_texts_ref


def flatten_Dict(nested_dict):
    values = []

    def recurse(d):
        for value in d.values():
            if isinstance(value, dict):
                recurse(value)
            else:

                values.append(value)

    recurse(nested_dict)
    return values


def save_embedding(pure_texts, path_emb, path_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedded_texts = model.encode(pure_texts, convert_to_tensor=True).to("cpu")
    torch.save(embedded_texts, path_emb)
    with open(path_text, 'w') as f:
        json.dump(pure_texts, f)


# %%
if __name__ == "__main__":

    DOCU = process_markdown_folder("docs")
    pure_texts = flatten_Dict(DOCU)
    save_embedding(pure_texts, "embeddings\\doc_embedded.pt",
                   "embeddings\\doc_text.json")

    REFE, pure_text_ref = process_reference_folder('reference\\reference')
    save_embedding(pure_text_ref, "embeddings\\ref_embedded.pt",
                   "embeddings\\ref_text.json")

    # print(pure_text_ref[0])
# %%

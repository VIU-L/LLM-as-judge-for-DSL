from sentence_transformers import SentenceTransformer
import torch
import json
import os
import re


# Function to parse a single .md file
def parse_md_file(file_path):
    results = []
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Find all subtitles (##) and their content
    subtitles = re.findall(r"(## .+?)(?=\n## |\Z)", content, re.DOTALL)

    for subtitle_section in subtitles:
        # Extract the subtitle title
        subtitle_lines = subtitle_section.splitlines()
        subtitle_title = subtitle_lines[0]

        # Check for subsubtitles (###) within the subtitle section
        subsubtitles = re.findall(
            r"(### .+?)(?=\n### |\Z)", subtitle_section, re.DOTALL)

        if subsubtitles:
            # Extract content before the first subsubtitle (if any)
            pre_subsubtitle_content = subtitle_section.split("###")[
                0].split("\n", 1)
            if len(pre_subsubtitle_content) > 1 and pre_subsubtitle_content[1].strip():
                results.append(
                    f"{subtitle_title} &Content: {pre_subsubtitle_content[1].strip()}")

            # Process each subsubtitle
            for subsubtitle_section in subsubtitles:
                subsubtitle_lines = subsubtitle_section.splitlines()
                subsubtitle_title = subsubtitle_lines[0]
                subsubtitle_content = " ".join(subsubtitle_lines[1:]).strip() if len(
                    subsubtitle_lines) > 1 else "No content"
                results.append(
                    f"{subtitle_title} {subsubtitle_title} & Content: {subsubtitle_content}")
        else:
            # If no subsubtitles, include all content in the subtitle
            subtitle_content = " ".join(subtitle_lines[1:]).strip() if len(
                subtitle_lines) > 1 else "No content"
            results.append(f"{subtitle_title} &Content: {subtitle_content}")
    return results


def parse_folder(folder_path):
    texts = []
    # Iterate through all .md files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".md"):
            results = parse_md_file(os.path.join(folder_path, file_name))
            for result in results:
                texts.append(
                    "&Title: " + file_name[:-3]+" &Subtitle: " + result)
    return texts


def save_embedding(pure_texts, path_emb, path_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedded_texts = model.encode(pure_texts, convert_to_tensor=True).to("cpu")
    torch.save(embedded_texts, path_emb)
    with open(path_text, 'w') as f:
        json.dump(pure_texts, f)


# %%
if __name__ == "__main__":

    doc_texts = parse_folder("docs")
    save_embedding(doc_texts, "embeddings\\doc_embedded.pt",
                   "embeddings\\doc_text.json")

    ref_texts = parse_folder('reference\\reference')
    save_embedding(ref_texts, "embeddings\\ref_embedded.pt",
                   "embeddings\\ref_text.json")

    print("refs:", len(ref_texts), "docs", len(doc_texts))
# %%

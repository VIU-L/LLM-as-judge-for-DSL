# %%
import os
import re
from collections import defaultdict

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
                doc_structure[current_subtitle]["ALL"] = "\n".join(current_content).strip()
                doc_structure[current_subtitle][0] = "\n".join(subtitle_content).strip()
            current_subtitle = line[3:].strip()  # Subtitle text
            current_subsubtitle = None
            current_content = []
            subtitle_content = []
            doc_structure[current_subtitle] = {0: "", "ALL": ""}  # Initialize new subtitle

        elif line.startswith("### "):  # New subsubtitle within a subtitle section
            # Save current subsubtitle's content if there was one
            if current_subsubtitle:
                doc_structure[current_subtitle][current_subsubtitle] = "\n".join(current_content).strip()
            current_subsubtitle = line[4:].strip()  # Subsubtitle text
            current_content = []

        else:
            # Add line to both subtitle_content and current_content
            if current_subtitle is not None:
                subtitle_content.append(line)
            current_content.append(line)

    # Final save for the last section parsed
    if current_subtitle:
        doc_structure[current_subtitle]["ALL"] = "\n".join(current_content).strip()
        doc_structure[current_subtitle][0] = "\n".join(subtitle_content).strip()
        if current_subsubtitle:
            doc_structure[current_subtitle][current_subsubtitle] = "\n".join(current_content).strip()

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
                print(file,type(file))
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    DOCU[file[:-3]] = parse_markdown(content)
                    DOCU[file[:-3]][0] = content.split("## ", 1)[-1].split("## ", 1)[0].strip()  # Content before first ##

    return DOCU
# %%
DOCU = process_markdown_folder("docs")
print (DOCU.keys())
print (DOCU["bigpicture"][0])

# %%

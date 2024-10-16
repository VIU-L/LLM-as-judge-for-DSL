def read_file(path):
    with open(path, 'r') as file:
        return file.read()
def extract_section(file_path, section_title):
    """
    Extracts the content of a specific section marked by a heading in a markdown file.

    :param file_path: The path to the markdown file.
    :param section_title: The title of the section to extract (e.g., "## Title").
    :return: The content of the section as a string, or None if the section is not found.
    """
    section_heading = f"## {section_title}"
    section_content = []
    inside_section = False

    with open(file_path, 'r', encoding='utf-8') as file:
        if section_title=="*ALL*":
            return file.read()
        for line in file:
            # Check if we reached the section we want
            if section_heading in line.strip():
                inside_section = True
                continue

            # If we're inside the section, capture the content
            if inside_section:
                # If we hit another section heading (starting with ##), stop
                if line.startswith("## "):
                    break
                section_content.append(line)

    return ''.join(section_content).strip() if section_content else None
def decompose_challenge(challenge):
    question,prof_answer=challenge.split("\n\n# ANSWER\n\n")
    prof_answer,references=prof_answer.split("\n\n# References\n\n")
    if len(references)==0:
        return question, prof_answer, []
    references=references.split("\n")
    ref_pairs=[]
    for ref in references:
        filename, title = ref.split('|')
        ref_pairs.append(['docs\\'+filename+".md",title])
    return question, prof_answer, ref_pairs
def create_ref(ref_pairs):
    ref_str=""
    for ref in ref_pairs:
        section=extract_section(ref[0],ref[1])
        ref_str+=section
    return ref_str
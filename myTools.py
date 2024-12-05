import requests
import sys


class Tee:
    """
    A class that duplicates standard output to multiple outputs.
    Attributes:
        files (tuple): A tuple of file-like objects to which the data will be written.
    Methods:
        __init__(*files):
            Initializes the Tee object with multiple file-like objects.
        write(data):
            Writes the given data to all file-like objects and flushes them to ensure immediate writing.
        flush():
            Flushes all file-like objects to ensure all data is written.
    """

    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for f in self.files:
            f.write(data)
            f.flush()  # To make sure data is written immediately

    def flush(self):
        for f in self.files:
            f.flush()


def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def decompose_challenge(challenge):
    """
    Decomposes a challenge string into its components: question, professor's answer, and references.
    Args:
        challenge (str): The challenge string containing the question, professor's answer, and references.
    Returns:
        tuple: A tuple containing:
            - question (str): The question part of the challenge.
            - prof_answer (str): The professor's answer part of the challenge.
            - ref_pairs (list): A list of reference pairs, where each pair is a list containing:
                - filename (str): The path of the markdown reference document related in the folder `docs`.
                - title (str): The title of the section related to the challenge in the reference file.
    """
    question, prof_answer = challenge.split("\n\n# ANSWER\n\n")
    prof_answer, references = prof_answer.split("\n\n# References\n\n")
    if len(references) == 0:
        return question, prof_answer, []
    references = references.split("\n")
    ref_pairs = []
    for ref in references:
        if ref == "":
            continue
        filename, title = ref.split("|")
        ref_pairs.append(['docs\\'+filename+".md", title])
    return question, prof_answer, ref_pairs


def extract_section(file_path, section_title):
    """
    Extracts the content of a specific section marked by a heading in a markdown file.

    :param file_path: The path to the markdown file.
    :param section_title: The title of the section to extract (e.g., "## Title").
    :return: The content of the section as a string, or None if the section is not found.
    """
    section_heading = section_title
    section_content = []
    inside_section = False

    with open(file_path, 'r', encoding='utf-8') as file:
        titles = section_title.split('|')
        current_level = 0
        title_levels = ["#", "##", "###", "####", "#####", "######"]

        for line in file:
            stripped_line = line.strip()
            if current_level < len(titles) and stripped_line.startswith(title_levels[current_level]) and titles[current_level] in stripped_line:
                current_level += 1
            if current_level == len(titles):
                inside_section = True
                continue

            if inside_section:
                if any(stripped_line.startswith(level) for level in title_levels[:current_level]):
                    break
            section_content.append(line)

    return ''.join(section_content).strip() if section_content else None


def create_ref(ref_pairs):
    ref_str = ""
    for ref in ref_pairs:
        section = extract_section(ref[0], ref[1])
        ref_str += section
    return ref_str

# send code to online compiler and check if it compiles


def check_compilation(script):
    """
    # Example usage: check_compilation(extract_code(stud_sentence))
    """
    url = "https://try.lokad.com/w/script/trycompile"
    payload = {
        "Script": script
    }
    try:
        # Send POST request
        response = requests.post(url, json=payload)

        # Check for successful response
        if response.status_code == 200:
            result = response.json()
            if result["IsCompOk"]:
                return True
            else:
                print("#### Compilation Failed")
                for message in result["CompMessages"]:
                    print(
                        f"Error: {message['Text']} (Line: {message['Line']}, Start: {message['Start']}, Length: {message['Length']}, Severity: {message['Severity']})")
                    return False
        else:
            print("Error: Unable to reach the compilation service.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Extract the 'real' code from the student answer (cut away the ```envision bit at the start and end)
# Example: print(extract_code(stud_sentence))
def extract_code(stud_sentence):
    lines = stud_sentence.strip().split('\n')
    return '\n'.join(lines[1:-1])


if __name__ == "__main__":
    import shutil
    import re

    def bold(text):
        return "\033[1m" + text + "\033[0m"

    def strip_ansi_codes(text):
        """Remove ANSI escape codes from the text."""
        ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mK]')
        return ansi_escape.sub('', text)

    def center_text(text):
        width = shutil.get_terminal_size().columns
        stripped_length = len(strip_ansi_codes(text))
        """Center the text considering the length of the escape codes."""
        total_spaces = width - stripped_length
        if total_spaces <= 0:
            return text
        left_padding = total_spaces // 2
        right_padding = total_spaces - left_padding
        return "-" * left_padding + text + "-" * right_padding

    # Test the `decompose_challenge` function
    challenge_path = "mychallenges/c010.md"
    print("Reading challenge from: ", challenge_path)
    challenge = read_file(challenge_path)
    question, prof_answer, references = decompose_challenge(challenge)
    # print
    print(center_text(bold("Challenge Question")))
    print(question)
    print(center_text(bold("Teacher Answer")))
    print(prof_answer)
    print(center_text(bold("References")))
    print(references)

    # Test the `create_ref` function
    ref_str = create_ref(references)
    print(center_text(bold("References String")))
    print(ref_str)

    # Test the `check_compilation` function
    script = extract_code(prof_answer)
    print(center_text(bold("Code to Compile")))
    print(script)
    print(center_text(bold("Compilation Result")))
    print("IsCompOK" if check_compilation(script) else "Compilation Failed")

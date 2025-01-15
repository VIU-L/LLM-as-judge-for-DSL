from apikey import api_key
from openai import OpenAI
from myTools import read_file
import os
docu = read_file(os.path.join("docs", "envision-brief.md"))
demander_personality = "You are a coder's assistant. The coder will be coding in a Domain Specific Language called Envision. You are given the BASIC DOCUMENTATION of Envision: \n&BASIC DOCUMENTATION"+docu + \
    "END OF BASIC DOCUMENTATION\n&\nThe user will give you a CODING TASK as input. You shall not try to code yourself; instead, based on the BASIC DOCUMENTATION you have seen above, you shall propose some grammar points or function usage that are NOT specified in the BASIC DOCUMENTATION but that a coder will nevertheless need to know in order to complete the CODING TASK. Output your answer as one or more concise bullet points, like [- the 'cos' function'] or [- handle dates] or [- defining a 'zedfunc']. Do not give any intermediate thinking or explain what you need the information for."
client = OpenAI(api_key=api_key)


def RAGdemand(question, demander_personality=demander_personality):
    """
    Generates a response to a given question using the demander's personality.
    Specifically, the demander is asked to propose some grammar points or
    function usage that are NOT specified in the BASIC DOCUMENTATION but that a
    coder will nevertheless need to know in order to complete the CODING TASK.
    The output of the demander is a list of bullet points, e.g. [- the 'cos'
    function'] or [- handle dates] or [- defining a 'zedfunc']. Args:
        question (str): The question to be answered. demander_personality (str):
        The personality to be used for generating the response.

    Returns:
        list: A list of strings containing the response, split by newline
        characters, containing the proposed grammar points or function usage.
    """
    demander_response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": demander_personality},
            {"role": "user", "content": question}
        ],
        max_tokens=1000,  # Adjust the number of tokens based on your needs
        temperature=0.1,
    ).choices[0].message.content
    return demander_response.split('\n')


# %%
if __name__ == "__main__":
    question = "Define a table T with 5 names with corresponding score. Show the maximum of these 5 scores at the tile a1b2, together with the name that achieves this best score at c1d2.  "
    ideas = RAGdemand(question)
    print(ideas)
    print(len(ideas))
# %%

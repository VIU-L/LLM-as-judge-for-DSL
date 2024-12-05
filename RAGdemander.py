from apikey import api_key
from openai import OpenAI
from myTools import read_file
docu = read_file(os.path.join("docs", "envision-brief.md"))
demander_personality = "You are a coder's assistant. The coder will be coding in a Domain Specific Language called Envision. You are given the BASIC DOCUMENTATION of Envision：\n&BASIC DOCUMENTATION"+docu + \
    "END OF BASIC DOCUMENTATION\n&\nThe user will give you a CODING TASK as input. You shall not try to code yourself; instead, based on the BASIC DOCUMENTATION you have seen above, you shall propose some grammar rules or function usage that are NOT seen in the BASIC DOCUMENTATION but that a coder will nevertheless want to know in order to complete the CODING TASK. Output your answer as several bulletpoint phrases. Do not output any intermediate thinking."
client = OpenAI(api_key=api_key)


def RAGdemand(question, demander_personality=demander_personality):
    return client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": demander_personality},
            {"role": "user", "content": question}
        ],
        max_tokens=1000,  # Adjust the number of tokens based on your needs
        temperature=0.1,
    ).choices[0].message.content


# %%
if __name__ == "__main__":
    question = "Define a table T with 5 names with corresponding score. Show the maximum of these 5 scores at the tile a1b2, together with the name that achieves this best score at c1d2.  "
    response = RAGdemand(question)
    print(response)
# %%

# %%
from transformers import AutoModel, AutoTokenizer
from RAGdemander import RAGdemand
from myTools import read_file
from LLMasJudge import client
import json
import warnings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re
import numpy as np
from docProcessing import *
import torch
from chapterTitleFinder import *
doc_embedded_path = os.path.join("embeddings", "doc_embedded.pt")
ref_embedded_path = os.path.join("embeddings", "ref_embedded.pt")
doc_text_path = os.path.join("embeddings", "doc_text.json")
ref_text_path = os.path.join("embeddings", "ref_text.json")
# %%


def penalize(x):
    return 100/(1+np.exp(0.003*(x-700)))


def query_related_titles(question, embedded_path, pure_texts, valid_indexes, count=5):
    """Retrieve titles related to the input question based on embeddings similarity."""
    query_embedding = model.encode(
        [question], convert_to_tensor=True).to("cpu")
    # Load embedded texts
    embedded_texts = torch.load(embedded_path)
    embedded_texts = embedded_texts[valid_indexes]

    # embedded_texts = model.encode(pure_texts, convert_to_tensor=True).to("cpu")

    similarities = cosine_similarity(query_embedding,   embedded_texts)
    similarities = similarities * \
        np.array([penalize(len(pure_texts[q]))
                 for q in range(len(embedded_texts))])
    # Sort in descending order
    ranked_indices = similarities[0].argsort()[::-1]
    original_indices = [valid_indexes[i] for i in ranked_indices]
    # Adjust the number as needed
    return original_indices[:count]


def text_to_feed(doc_embedded_path, pure_doc, pure_ref, question, ideas, countDocu=5):

    # ideas are formulated as eg. ['- Relational algebra', '- Natural joins', '- Table comprehensions', '- Table sizes', '- Dashboards', '+ extend.range', '+ concat', '+ sum', '+ show', '+ text'] where - signifies grammar and + signifies function

    # all paragraphs in pure_doc starts with &Title: (title).

    toFeed = ""
    print(ideas)
    valid_doc_paragraph_indexes = []
    for idea in ideas:
        title = idea[2:]
        chaptertitle = ""
        if idea.startswith('-'):
            for key in findtitle.keys():
                if key in title:
                    chaptertitle = findtitle[key]
                    break
            if chaptertitle != "":
                valid_doc_paragraph_indexes = valid_doc_paragraph_indexes+[i for i, paragraph in enumerate(
                    pure_doc) if paragraph.startswith(f"&Title: {chaptertitle}")]
    original_indexes = query_related_titles(
        question, doc_embedded_path, pure_doc, valid_doc_paragraph_indexes, countDocu)
    for idx in original_indexes:
        text = pure_doc[idx]
        toFeed += "[[A piece of grammar documentation:]]\n\n "+text+"\n\n"
    chosen_references = []
    for idea in ideas:
        title = idea[2:]
        if (idea.startswith('+')):
            pure_ref_under_this_title = [
                paragraph for paragraph in pure_ref if paragraph.startswith(f'+++\ntitle = "{title}"')]
            chosen_references = chosen_references+pure_ref_under_this_title
    print("eligible functions:", len(chosen_references))
    for reference in chosen_references:
        toFeed += "[[A piece of function documentation:]]\n\n " + \
            reference+"\n\n"
    print("docs RAGed:", len(original_indexes),
          "refs RAGed", len(chosen_references))
    return toFeed

# Example usage


def feed_to_RAG(question, ideas):
    warnings.filterwarnings("ignore")
    with open(doc_text_path, "r") as file:
        pure_doc = json.load(file)
    with open(ref_text_path, "r") as file:
        pure_ref = json.load(file)
    return text_to_feed(doc_embedded_path, pure_doc, pure_ref, question, ideas)


docu = read_file(os.path.join("docs", "envision-brief.md"))

RAGcoder_personality = "You are a proficient coder in the Domain Specific Language called Envision. \
    Your task is to generate response to the given challenge. \
    Some challenges will ask you to generate Envision code,\
    others will ask you to explain given code or answer questions related to the Envision language. \
    Do not output any intermediate thinking or explanation, only give the final answer.\
    Below is the Basic Documentation of Envision, which will be followed by several pieces of potentially relevant Auxiliary Documentation. Note that it is possible that some documentations pieces can be irrelevant or misleading, you need to judge yourself.\
    ### Basic Documentation\n" + docu


def RAG_pipeline(question, coder_personality=RAGcoder_personality):
    # enhance by ragdemander
    ideas = RAGdemand(question)
    toFeed = feed_to_RAG(question, ideas)
    # information += feed_to_RAG(ideas)
    # print(toFeed)
    coder_prompt = question
    coder_response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": coder_personality+toFeed},
            {"role": "user", "content": coder_prompt}
        ],
        max_tokens=1000,  # Adjust the number of tokens based on your needs
        temperature=0.1,
    )
    stud_sentence = coder_response.choices[0].message.content
    return stud_sentence


# %%
if __name__ == "__main__":
    question = '''Let's display, as text, an expression "y = a * x + b" where `a` and `b` are replaced by their numerical values. The goal is to have the text composed dynamically based on the number values of `a` and `b`. Here, for the sake of the example, take `a = 13` and `b = 7`.'''
    print(RAG_pipeline(question))

# %%

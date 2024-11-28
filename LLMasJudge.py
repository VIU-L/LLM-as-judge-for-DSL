"""
A py copy of the original LLMasJudge.ipynb to avoid merging conflicts.
It uses OpenAI's GPT-3.5-turbo model to generate and judge responses based on predefined personalities and rules.
Functions:
----------
- pipeline_verify:
    1. Generate a student's response to a given challenge.
    2. Check the response for compilation errors. if it does not compile, go back to step 1.
    2. Verity the response using a judge.
    3. Then a verifier converts the judge's decision to a binary output.

- pipeline_score_allchallenge:
    Test on a list of challenges by verifying each one using the pipeline_verify function.
    It prints the number of correct responses and the overall percentage accuracy.

Variables:
----------
- client: An instance of the OpenAI client initialized with the provided API key.
- docu: The documentation content read from the "envision-brief.md" file.
- coder_personality: A string defining the coder's personality and task.
- judge_personality_teacherAuthority: A string defining the judge's personality and rules for evaluating responses.

Usage:
------
- The script can be run directly, and it will score a predefined list of challenges.
- The main function to execute is `pipeline_score_allchallenge`, which takes a list of challenge indexes and the coder personality as input.
"""

# %% Initialization
from openai import OpenAI
from apikey import api_key
from myTools import *
import os
import sys

client = OpenAI(api_key=api_key) 

# %% Defining the personalities, rules, and docs for the coder and judge
docu = read_file(os.path.join("docs","envision-brief.md"))

coder_personality="You are a proficient coder in the Domain Specific Language called Envision. \
    Your task is to generate response to the given challenge. \
    Some challenges will ask you to generate Envision code,\
    others will ask you to explain given code or answer questions related to the Envision language. \
    Do not output any intermediate thinking or explanation, only give the final answer.\
    Here is the documentation of Envision:\
    ### Documentation\n" + docu

# this personality sticks more to professor's answer.

judge_personality_teacherAuthority=judge_personality_teacherAuthority="Your goal is to judge the correctness of STUDENT ANSWER, as an answer to the QUESTION.\
In order to judge the STUDENT ANSWER, you are given the PROFESSOR ANSWER with a piece of related documentation.\
Your main job is not to check the syntax correctness, but the logical correctness.\
If the STUDENT ANSWER does not treat the QUESTION logically, it is UNACCEPTABLE.\
Pay special attention to the comments in the PROFESSOR ANSWER. If these comments include\
a rule and if the STUDENT ANSWER violates it, this is UNACCEPTABLE.\
If in the show command, the STUDENT ANSWER add or omit a print position (like a1b2) compared to the PROFESSOR ANSWER, ignore this: this is always ACCEPTABLE.\
The use of extra variable or table to temporarily contain a intermediate quantity is ACCEPTABLE.\
Differences in variable names, column names, table names and label names etc. shall systematically be ACCEPTABLE! \
There are sometimes various ways or logics to treat the same QUESTION, and this is ACCEPTABLE, as long as the goal of the QUESTION is achieved.\
Let's think aloud step by step before making your judgement. Tell each ACCEPTABLE or UNACCEPTABLE point. \
At the end of your output, you should judge 0 if there is anything UNACCEPTABLE (even only 1 mark of UNACCEPTABLE) in the STUDENT ANSWER;\
and judge 1 if everything is ACCEPTABLE. End your judgment by the digit either 0 or 1. \
Here is the piece of related documentation : \n ## DOCUMENTATION\n"

verifier_personality="Your task is to summarize the input given by the judge:\
    - If the judge has found nothing unacceptable, you should output 1.\
    - If the judge has found anything unacceptable, you should output 0.\
    - Focus on the last line of the judge's sentence: if it has already announced the final judgement, you should output the same (0 or 1).\
    Do not output anything other than pur digit 0 or 1, without font, punctuation or any special character."

# %% Functions
# for each question, try 3 generation-compilations.
# if compiles, further check with judge.
def pipeline_verify(challenge, coder_personality, judge_personality = judge_personality_teacherAuthority, n_tries = 3, verbose=True):
    """
    1. Generate a student's response to a given challenge.
    2. Check the response for compilation errors. if it does not compile, go back to step 1.
    2. Verity the response using a judge.
    3. Then a verifier converts the judge's decision to a binary output.
    """
     
    question,prof_answer,references=decompose_challenge(challenge)
    ref_str = create_ref(references)    

    # generate an answer and compile the student's answer until it compiles or the number of tries is reached
    for compile_try in range(1, n_tries+1):
        coder_prompt=question
        coder_response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": coder_personality},
                {"role": "user", "content": coder_prompt}
            ],
            max_tokens=1000,  # Adjust the number of tokens based on your needs
            temperature=0.2,
        )
        stud_sentence=coder_response.choices[0].message.content
        
        if verbose:
            print('### compile try:', compile_try)
            print('#### STUDENT ANSWER:\n', stud_sentence)

        if (question.split("\n")[0] ==\
        '# this question expects a textual answer and not generation of code. #'):
            print('#### Compilation: theoretical question, no compile.')
            break
        if(check_compilation(extract_code(stud_sentence))):
            print('#### Compilation: OK')
            break
        if compile_try == n_tries:
            print( "### Compilation: too many failures !")
            if not verbose:
                print('badcode', extract_code(stud_sentence))
            return stud_sentence,"too many compilation failures!", False

    # judge the student's answer
    judge_prompt = "### QUESTION: "+question+"\n### PROFESSOR ANSWER: "+prof_answer+"\n### STUDENT ANSWER: "+stud_sentence
    judge_response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": judge_personality+ref_str},
            {"role": "user", "content": judge_prompt}
        ],
        max_tokens=800,  # Adjust the number of tokens based on your needs
        temperature=0.2,
    )
    judge_sentence=judge_response.choices[0].message.content

    if verbose: print('### JUDGE ANSWER:\n', judge_sentence)

    # verify the judge's decision
    verifier_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": verifier_personality},
        {"role": "user", "content": judge_sentence}
    ],
    max_tokens=800,  # Adjust the number of tokens based on your needs
    temperature=0.05)

    judge_decision = (verifier_response.choices[0].message.content == '1')

    if verbose: print ('### judge_decision:',judge_decision)
    if not verbose and not judge_decision:
        print('### BADCODE:\n', extract_code(stud_sentence))
        print('### judge explanation:\n', judge_sentence)

    return stud_sentence, judge_sentence, judge_decision

def pipeline_score_allchallenge(paths, coder_personality, verbose=True):
    """A all-in-one function to score a model on a list of challenges"""
    challenges = [read_file(path) for path in paths]
    score = 0
    compilation_success = 0
    for i in range(len(challenges)): 
        challenge = challenges[i]
        print('## verifying challenge ' + paths[i], '\n')
        _, judge_sentence, judge_decision = pipeline_verify(challenge,coder_personality,verbose=verbose)
        if (judge_sentence=='too many compilation failures!'):
            continue
        compilation_success += 1
        if (judge_decision): score+=1
        print('\n')

    print('## Compilation success rate:\n'+str(compilation_success)+' out of '+str(len(challenges))+', '+str(compilation_success/len(challenges)*100)+'%')
    print('## Accuracy:\n'+str(score)+' out of '+str(len(challenges))+', '+str(score/len(challenges)*100)+'%')

# %% main
if __name__ == '__main__':

    from datetime import datetime
    
    # Get the date and time as YYYY-mm-dd-xx:xx
    input_challenge_folder = "mychallenges"
    folder_path = os.path.join("output","LLMasJudge")
    output_path = os.path.join(folder_path, f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}.md")
    
    # Create the output folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Duplicate stdout to a file
    with open(output_path, 'w') as f:
        tee = Tee(sys.stdout, f)
        sys.stdout = tee
        # Attention, cela coûte cher en argent
        # challenge_paths = [os.path.join(input_challenge_folder, filename) 
        #          for filename in os.listdir(input_challenge_folder)
        #          if filename.endswith('.md') and filename!='description.md']
        
        challenge_paths = ["mychallenges/c010.md"]
        pipeline_score_allchallenge(challenge_paths, coder_personality, verbose=True)
        sys.stdout = sys.__stdout__  # Reset stdout to default
# %%
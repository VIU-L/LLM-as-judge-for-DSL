### This reposit is for the group project in Ecole Polytechnique. ###
### Please do not use or download the files in this reposit if you are not involved with the project, thank you ! ###

Newly done:  
*new RAGdemander*:   
combined search, propose [function names & grammar chapter names].  
*new RAGsearcher*: (please use RAGsearcher_v2)   
For the proposed functions, directly concatenate their documentation.  
For (and only for) the proposed grammars, do embedding match.  

Results: argmax ok :)  



ToDo:   
1. Evaluate on all benchmark  
2. Test deepseek  (super-long context?)
3. Test Langchain   
4. After a 1st output, if does not pass compilation, retract doc for each error point. (how to detect?)     
5. After a 1st batch retrieved, make a 2nd retrieval based on the 1st-batch material?

## Main entries

`LLMasJudge.py`

```
- pipeline_verify:
    1. Generate a student's response to a given challenge.
    2. Check the response for compilation errors. if it does not compile, go back to step 1.
    2. Verity the response using a judge.
    3. Then a verifier converts the judge's decision to a binary output.

- pipeline_score_allchallenge:
    Test on a list of challenges by verifying each one using the pipeline_verify function.
    It prints the number of correct responses and the overall percentage accuracy.
```

`RAGsearcher.py`

```
This module provides functionality to retrieve relevant documentation based on a
given question and generate responses using a RAG pipeline. Functions:
    feed_to_RAG(question):
        Loads documentation and reference texts, and generates text to feed into
        the RAG model based on the input question.
    RAG_pipeline(question, coder_personality=RAGcoder_personality):
        Enhances the input question using RAGdemand, retrieves relevant
        documentation, and generates a response using the RAG model.
```

Question: These two functionalities are not yet merged?
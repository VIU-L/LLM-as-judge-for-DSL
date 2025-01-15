### This reposit is for the group project in Ecole Polytechnique. ###
### Please do not use or download the files in this reposit if you are not involved with the project, thank you ! ###


Newly done:
LLM RAGdemander, it is now connected to RAGsearcher  
results: RAGdemander ok in proposing relevant ideas, but the transformer cannot robustly match to the paragraph.  
potential solution: point 4 in ToDo  

ToDo:  
3. fix and refine LLM judge    
4. heavy method: split exceedingly-long paragraphs in documentation; write a concise summary of every paragraph in documentation, eg 'how to use argmax'; once done we will match LLMdemander-proposed Ideas only on the summary    
OR alternatively  
light method: try only matching text, neglecting envision code when encoding paragraphs. (will try this week)  
5. Change model / transformer to allow for precise matching with long paragraphs  
6. After a 1st output, if does not pass compilation, retract doc for each error point. (how to detect?)     
7. After a 1st batch retrieved, make a 2nd retrieval based on the 1st-batch material?

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
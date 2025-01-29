### This reposit is for the group project in Ecole Polytechnique. ###
### Please do not use or download the files in this reposit if you are not involved with the project, thank you ! ###

Newly done:  
*new RAGdemander*: combined search, propose [function names & grammar chapter names].  
*new RAGsearcher*: (please use RAGsearcher_v2)  
For the proposed functions, directly concatenate their documentation.
For (and only for) the proposed grammars, do embedding match.  

Results: argmax ok :)  



ToDo:  
0. Evaluate on all benchmark  
1. Test deepseek  
2. Test Langchain (super-long context?)  
6. After a 1st output, if does not pass compilation, retract doc for each error point. (how to detect?)     
7. After a 1st batch retrieved, make a 2nd retrieval based on the 1st-batch material?

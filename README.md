### This reposit is for the group project in Ecole Polytechnique. ###
### Please do not use or download the files in this reposit if you are not involved with the project, thank you ! ###

Newly done:
LLM RAGdemander, it is now connected to RAGsearcher  
results: RAGdemander ok in proposing relevant ideas, but the transformer cannot robustly match to the paragraph.  
potential solution: point 4 in ToDo  

ToDo:  
3. fix and refine LLM judge    
4. split exceedingly-long paragraphs in documentation; write a concise summary of every paragraph in documentation, eg 'how to use argmax'; once done we will match LLMdemander-proposed Ideas only on the summary  
OR alternatively
try only matching text, removing envision code when encoding paragraphs. (will do this week)  
5. Change model / transformer to exploit specific coding expertise  
6. After a 1st output, if does not pass compilation, retract doc for each error point. (how to detect?)   

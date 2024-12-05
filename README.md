### This reposit is for the group project in Ecole Polytechnique. ###
### Please do not use or download the files in this reposit if you are not involved with the project, thank you ! ###

ToDo:
1. LLM RAGdemander who, when given a coding quest, outputs a textual summary of what a coder would want to know about the language.(which will be fed to RAGsearcher) (the RAGdemander shall see the basic docs, then demands what it lacks.)
3. fix and refine LLM judge
4. split exceedingly-long paragraphs in documentation; try to key-word every paragraph in documentation; we can combine key-word matching and content matching.
5. Change model / transformer to exploit specific coding expertise
6. After a 1st output, if does not pass compilation, retract doc for each error point. (how to detect?) 

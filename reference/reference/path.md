+++
title = "path"
+++

## path, concepts

A typical Lokad account contains two separate trees: 

 - The script tree, which contains all Envision scripts, synchronization scripts, and script sequences.
 - The file tree, which contains all data files. 

These are hierarchies of _folders_ that can contain _scripts_ (respectively, _files_) or nested folders. Each folder, script or file has a unique text identifier based on its location, which is called its **path**. 

Paths are [a very common concept in computing](https://en.wikipedia.org/wiki/Path_(computing)). Lokad uses `/` as the path separator. 

Example paths: 

 - `/` is the path of the root folder that contains everything else.
 - `/input/catalog.csv` is a typical path for a "catalog" input file uploaded to the account. It would appear in a `read "/input/catalog.csv"` statement, or in a `schema '/input/catalog.csv'` definition.
 - `/.utilities/Functions` is a typical path for a module containing shared functions within an account. It would appear in an `import "/.utilities/Functions"` statement.
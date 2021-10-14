# CosineVectorSpaceModel
This project contains the implementation of a vector space model, which calculates the similarity between various query and document vectors provided.

It uses the inverted indexing scheme of the documents, and each vector is represented as the weight of that vector which is calculated as the term frequency
multiplied by the inverted document frequency.

The algorithm also computes the precision, recall and the top N documents in decreasing order of relevancy with the queries.

The algorithm does not use any in built numpy or pandas libraries, the entire model is built based on pure python code. This is done so to display proficiency
in designing and creating algorithms from scratch.


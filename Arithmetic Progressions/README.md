Calculates whether there exists a set of size M which intersects
every arithmetic progression of length N in {0,1,2,...,L-1}.

Usage:
1)  Modify N, M, and L in the code to the desired values.
2) In Python interpreter, run from directory containing ap.py
   > from ap import *
   
   > main()
 
 General Idea:
 This is an improvement on the brute-force search.
 We think of the subsets of size M in {0,1,...,L-1
 as a branches of a binary tree of height L.
 We order these subsets by lexicographic order
 of their characeristic functions, and search through
 the entire set of branches of 2^L from left to right.
 But we do a naive pruning: if an arithmetic progression
is contained in the complement of X intersect {0,1,...k}
for some k < L, we can prune all the branches whose 
intersection with {0,1,...k} is equal to that of X's. 

This algorithm always produces the "left-most" example
if there is one.

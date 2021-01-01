Title: More Go Data Structures with Heap and Tree and Trie
Date: 2018-02-10 07:07
Tags: go, golang, heap, tree, bst, trie

[TOC]

Idiomatic Go depends heavily on the standard library.  Given that performance is often implementation dependent and directly related to the data being stored,
it makes sense that one must write some of the more common data structures from scratch.

While slices (a.k.a. dynamic arrays) are included (as is a double linked list), a Set must be implemented using a map (for the specific type(s) of interest)
<https://blog.john-pfeiffer.com/golang-interfaces-stack-linked-list-queue-map-set/>

Some of my favorite data structures are based upon trees...

## Heap

A heap (<https://en.wikipedia.org/wiki/Heap_%28data_structure%29>) is a tree that maintains a specific property, i.e. the parent is always larger than its children
A binary heap (aka "priority queue" <https://en.wikipedia.org/wiki/Binary_heap>) has some very helpful and efficient qualities, especially when implemented by using an array (using computations leveraging the inherent relationship with powers of 2).
For instance, it is possible to use something like heapsort to sort an array in-place.

A common use for a min-heap or max-heap is to be able to answer a query in O(1). (The top/first item retrieved is the answer!)

**And after you get that answer, the next root item you "pop" is the next best answer!**

<https://golang.org/pkg/container/heap/> is already included in the standard library =]

## Binary Search Tree

A binary search tree maintains a specific property between all nodes in the tree.  This is most often used to keep a collection of items sorted in order.

If the tree is balanced (<https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree>) we can mathematically guarantee the time for various operations.

**Because each branch splits into 2 it follows intuitively that time bounds are logn (the fancy way of saying the inverse of 2^x)** <https://en.wikipedia.org/wiki/Binary_logarithm>

- <https://github.com/johnpfeiffer/gotree>

## Trie

An interesting variation of a tree is a trie that allows for very fast retrieval of information (if it exists)

<https://en.wikipedia.org/wiki/Trie>

A common example is quickly identifying if a string is available (i.e. autocompletion suggestions of words or names, or "boggle")
(Hence the obvious application of a trie also-known-as a "prefix tree") , video of Zelenski at Stanford explaining: <https://youtu.be/TJ8SkcUSdbU?t=13m21s>

- <https://github.com/johnpfeiffer/gotree>

### Benefits

- A trie is fast, like O(m) where m = the length of the search string (assuming that m is far smaller than all n keys in the tree)
- Unlike hashtables no hashing algorithm is required
- "intermediate" or "subset" solutions/queries are possible by returning a subtree
- Iterating through the trie can return the keys in a specific (e.g. alphabetical) order






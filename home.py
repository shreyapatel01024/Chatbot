import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -------------------------------
# Route to render the chatbot UI
# -------------------------------
@app.route("/")
def chatbot():
    return render_template("chatbot.html")

# -------------------------------
# API to get chatbot response
# -------------------------------
@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    user_msg = request.form['msg'].strip()
    best_match, best_score = find_best_match(user_msg)

    if best_score >= 0.8:
        response = dsa_responses[best_match]
        return jsonify(response)

    return jsonify("Sorry, I don't have an answer for that yet. Try asking about Linked List, Stack, Queue, Tree, Graph, Hash Table, etc.")

# -------------------------------
# Levenshtein Similarity Functions
# -------------------------------
def levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[len_s1][len_s2]

def calculate_similarity(str1, str2):
    lev_dist = levenshtein_distance(str1, str2)
    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 1.0
    return 1 - lev_dist / max_len

def find_best_match(user_msg):
    best_match = None
    best_score = 0.0
    for topic in dsa_responses.keys():
        score = calculate_similarity(user_msg.lower(), topic.lower())
        if score > best_score:
            best_score = score
            best_match = topic
    return best_match, best_score

# -------------------------------
# DSA Topics & Responses
# -------------------------------
dsa_responses = {
    "linkedlist": "A linked list is a data structure that stores a sequence of elements. Each element in the list is called a node, and each node has a reference to the next node in the list. The first node in the list is called the head, and the last node in the list is called the tail.",
    "stack": "Stacks are Last In First Out (LIFO) data structures.",
    "queue": "Queues are First In First Out (FIFO) data structures.",
    "tree": "A tree is a hierarchical data structure consisting of nodes connected by edges.",
    "graph": "A graph is a collection of nodes (vertices) and edges connecting pairs of nodes.",
    "hashtable": "A hash table stores key-value pairs and is optimized for fast lookups.",
    "binarytree": "A binary tree is a tree where each node has at most two children.",
    "bfs": "Breadth-First Search (BFS) is an algorithm for traversing or searching tree or graph data structures.",
    "dfs": "Depth-First Search (DFS) is an algorithm for traversing or searching tree or graph data structures.",
    "sorting": "Sorting is the process of arranging items in a systematic order, often numerically or alphabetically.",
    "quick sort": "Quick Sort is a divide-and-conquer algorithm that works by selecting a 'pivot' element.",
    "merge sort": "Merge Sort is a divide-and-conquer algorithm that divides the array into two halves and merges them.",
    "heap": "A heap is a special tree-based data structure that satisfies the heap property.",
    "bubble sort": "Bubble Sort is a simple sorting algorithm that repeatedly steps through the list.",
    "insertion sort": "Insertion Sort is a simple sorting algorithm that builds the sorted array one element at a time.",
    "selection sort": "Selection Sort is an in-place comparison-based sorting algorithm.",
    "radix sort": "Radix Sort is a non-comparative integer sorting algorithm that sorts numbers digit by digit.",
    "bucket sort": "Bucket Sort is a sorting algorithm that divides the data into buckets and sorts each bucket.",
    "dijkstra's algorithm": "Dijkstra's Algorithm is used to find the shortest path between nodes in a graph.",
    "bellman-ford algorithm": "Bellman-Ford Algorithm is used to find the shortest path in a weighted graph.",
    "floyd-warshall algorithm": "Floyd-Warshall Algorithm finds shortest paths in a weighted graph with positive or negative edge weights.",
    "kmp algorithm": "The Knuth-Morris-Pratt (KMP) algorithm is a string-searching algorithm.",
    "trie": "A Trie is a tree-like data structure that stores strings in a way that allows fast search, insert, and delete operations.",
    "binary search": "Binary Search is an efficient algorithm for finding an item from a sorted list of items.",
    "knapsack problem": "The Knapsack Problem is a combinatorial optimization problem where the goal is to select items with given weights and values.",
    "fibonacci series": "The Fibonacci series is a sequence of numbers where each number is the sum of the two preceding ones.",
    "lru cache": "Least Recently Used (LRU) Cache is a cache eviction algorithm where the least recently used entry is removed first.",
    "greedy algorithm": "A greedy algorithm is a simple, intuitive algorithm that makes locally optimal choices at each stage.",
    "divide and conquer": "Divide and Conquer is a problem-solving paradigm that solves a problem by breaking it into subproblems.",
    "dynamic programming": "Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems.",
    "backtracking": "Backtracking is a general algorithmic technique that considers all possible solutions by building incrementally.",
    "bloom filter": "A Bloom Filter is a space-efficient probabilistic data structure used to test if an element is a member of a set.",
    "union-find": "The Union-Find data structure is a way to keep track of a partition of a set into disjoint subsets.",
    "topological sort": "Topological Sort is a linear ordering of vertices in a Directed Acyclic Graph (DAG).",
    "bit manipulation": "Bit manipulation refers to using bitwise operations (AND, OR, XOR) to manipulate data at the bit level.",
    "matrix multiplication": "Matrix multiplication is the operation of multiplying two matrices to produce a third matrix.",
    "string matching": "String matching algorithms are designed to find a substring within a string.",
    "edit distance": "Edit distance measures how dissimilar two strings are by counting the minimum number of operations required to transform one string into the other.",
    "huffman coding": "Huffman Coding is a lossless data compression algorithm.",
    "morse code": "Morse code is a method of encoding textual information using sequences of dots and dashes.",
    "lcs": "The Longest Common Subsequence (LCS) problem is finding the longest subsequence common to two sequences.",
    "longest increasing subsequence": "The Longest Increasing Subsequence problem involves finding the longest subsequence of a given sequence where the elements are sorted in strictly increasing order.",
    "palindrome": "A palindrome is a word, phrase, or number that reads the same backward as forward.",
    "subsets": "Subsets are the collections of elements that can be derived from a set by including or excluding each element.",
    "permute": "Permute refers to rearranging the elements of a set or list into all possible orderings.",
    "matrix traversal": "Matrix traversal refers to the process of visiting all elements of a matrix in a systematic way.",
    "graph traversal": "Graph traversal is the process of visiting all vertices in a graph, typically done via BFS or DFS."
}

# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

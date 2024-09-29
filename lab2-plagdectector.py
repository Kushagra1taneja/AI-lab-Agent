import heapq
import re

class Node:
    def __init__(self, g, h, state, parent=None):
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.state = state
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def preprocess_text(text):
    sentences = re.split(r'[.!?]', text)
    normalized_sentences = [re.sub(r'[^\w\s]', '', sentence.strip().lower()) for sentence in sentences if sentence.strip()]
    return normalized_sentences

def heuristic(state, doc1_sentences, doc2_sentences):
    i, j = state
    remaining_sentences_doc1 = doc1_sentences[i:]
    remaining_sentences_doc2 = doc2_sentences[j:]
    h = 0
    for sentence1 in remaining_sentences_doc1:
        if remaining_sentences_doc2:
            h += min([levenshtein_distance(sentence1, sentence2) for sentence2 in remaining_sentences_doc2])
        else:
            h += len(sentence1)
    return h

def get_successors(node, doc1_sentences, doc2_sentences):
    i, j = node.state
    successors = []
    if i < len(doc1_sentences) and j < len(doc2_sentences):
        g = node.g + levenshtein_distance(doc1_sentences[i], doc2_sentences[j])
        h = heuristic((i + 1, j + 1), doc1_sentences, doc2_sentences)
        successors.append(Node(g, h, (i + 1, j + 1), node))
    if i < len(doc1_sentences):
        g = node.g + len(doc1_sentences[i])
        h = heuristic((i + 1, j), doc1_sentences, doc2_sentences)
        successors.append(Node(g, h, (i + 1, j), node))
    if j < len(doc2_sentences):
        g = node.g + len(doc2_sentences[j])
        h = heuristic((i, j + 1), doc1_sentences, doc2_sentences)
        successors.append(Node(g, h, (i, j + 1), node))
    return successors

def a_star_search(doc1_sentences, doc2_sentences):
    start_node = Node(0, heuristic((0, 0), doc1_sentences, doc2_sentences), (0, 0))
    goal_state = (len(doc1_sentences), len(doc2_sentences))
    open_set = []
    heapq.heappush(open_set, start_node)
    visited = set()
    while open_set:
        current_node = heapq.heappop(open_set)
        if current_node.state == goal_state:
            return current_node
        if current_node.state in visited:
            continue
        visited.add(current_node.state)
        for successor in get_successors(current_node, doc1_sentences, doc2_sentences):
            if successor.state not in visited:
                heapq.heappush(open_set, successor)
    return None

def reconstruct_alignment(goal_node, doc1_sentences, doc2_sentences):
    alignment = []
    node = goal_node
    while node.parent is not None:
        i, j = node.state
        prev_i, prev_j = node.parent.state
        if i > prev_i and j > prev_j:
            alignment.append((doc1_sentences[prev_i], doc2_sentences[prev_j]))
        elif i > prev_i:
            alignment.append((doc1_sentences[prev_i], ""))
        elif j > prev_j:
            alignment.append(("", doc2_sentences[prev_j]))
        node = node.parent
    alignment.reverse()
    return alignment

def detect_plagiarism(doc1, doc2):
    doc1_sentences = preprocess_text(doc1)
    doc2_sentences = preprocess_text(doc2)
    goal_node = a_star_search(doc1_sentences, doc2_sentences)
    if goal_node:
        alignment = reconstruct_alignment(goal_node, doc1_sentences, doc2_sentences)
        return alignment
    else:
        return "No alignment found"

def classify_plagiarism_average(avg_edit_distance):
    if avg_edit_distance == 0:
        return "High Plagiarism"
    elif 1 <= avg_edit_distance <= 5:
        return "Partial Plagiarism"
    elif 6 <= avg_edit_distance <= 10:
        return "Low Plagiarism"
    else:
        return "No Plagiarism"

def calculate_average_edit_distance(alignment_result):
    total_distance = 0
    for aligned_pair in alignment_result:
        total_distance += levenshtein_distance(aligned_pair[0], aligned_pair[1])
    return total_distance / len(alignment_result) if alignment_result else float('inf')

def print_test_case_result(doc1, doc2, test_case_name):
    print(f"{test_case_name}:")
    alignment_result = detect_plagiarism(doc1, doc2)
    total_edit_distance = 0
    for aligned_pair in alignment_result:
        edit_distance = levenshtein_distance(aligned_pair[0], aligned_pair[1])
        print(f"Doc1: {aligned_pair[0]}")
        print(f"Doc2: {aligned_pair[1]}")
        print(f"Edit Distance: {edit_distance}\n")
        total_edit_distance += edit_distance
    avg_edit_distance = total_edit_distance / len(alignment_result)
    plagiarism_type = classify_plagiarism_average(avg_edit_distance)
    print(f"Overall Plagiarism: {plagiarism_type} (Average Edit Distance: {avg_edit_distance})\n")

# Test cases
doc1 = "This is the first test case. It contains several sentences. These sentences are identical."
doc2 = "This is the first test case. It contains several sentences. These sentences are identical."
print_test_case_result(doc1, doc2, "Test Case 1")

doc1 = "This is the second test case. It contains several sentences. These sentences are identical."
doc2 = "This is the second test case. It includes multiple sentences. These sentences are very similar."
print_test_case_result(doc1, doc2, "Test Case 2")

doc1 = "The grass is green. I love playing games."
doc2 = "Artificial intelligence is fascinating. Machine learning algorithms are powerful."
print_test_case_result(doc1, doc2, "Test Case 3")

doc1 = "The quick brown fox jumps over the lazy dog. Machine learning is a growing field. Programming languages are essential."
doc2 = "Machine learning is a growing field. Deep learning is a subset of machine learning. The quick brown fox jumps over the lazy dog."
print_test_case_result(doc1, doc2, "Test Case 4")

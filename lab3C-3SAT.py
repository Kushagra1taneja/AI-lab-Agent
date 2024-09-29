import random

def generate_3sat(k, m, n):
    pos_vars = [chr(i) for i in range(97, 97 + n)]
    neg_vars = [f"-{var}" for var in pos_vars]
    total_vars = pos_vars + neg_vars
    
    combinations = []
    get_combinations(total_vars, len(total_vars), k, [], combinations)
    
    unique_clauses = set()
    while len(unique_clauses) < m:
        clause = tuple(random.choice(combinations))
        if clause not in unique_clauses:
            unique_clauses.add(clause)

    for clause in unique_clauses:
        print(" ∨ ".join(clause))

def get_combinations(vars_list, size, k, indices, combinations):
    if len(indices) == k:
        comb = [vars_list[i] for i in indices]
        combinations.append(comb)
        return

    for i in range(size):
        if i not in indices:
            get_combinations(vars_list, size, k, indices + [i], combinations)

def main():
    k = int(input("Enter the number of literals per clause (k): "))
    m = int(input("Enter the number of clauses (m): "))
    n = int(input("Enter the number of variables (n): "))

    generate_3sat(k, m, n)

if __name__ == "__main__":
    main()
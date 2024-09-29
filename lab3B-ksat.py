import random

def generate_random_k_sat(n, m, k):
    if k > n:
        raise ValueError("k must be less than or equal to n.")
    if m <= 0:
        raise ValueError("m must be a positive integer.")

    clauses = []
    for _ in range(m):
        variables = random.sample(range(1, n + 1), k)
        clause = set()
        for var in variables:
            if random.choice([True, False]):
                clause.add(var)
            else:
                clause.add(-var)
        clauses.append(clause)
    
    return clauses

def print_k_sat_instance(clauses):
    for clause in clauses:
        print(" ".join(str(lit) for lit in clause) + " 0")

def main():
    n = int(input("Enter the number of variables (n): "))
    m = int(input("Enter the number of clauses (m): "))
    k = int(input("Enter the clause length (k): "))
    
    try:
        clauses = generate_random_k_sat(n, m, k)
        print("\nGenerated k-SAT Problem:")
        print_k_sat_instance(clauses)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

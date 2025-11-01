import numpy as np
from collections import Counter
import math

# -----------------------------------------------------------------------------------------------------------------------
# 1/ Information Quantity and Source Entropy

def information_quantity(probability):
    """
    Calculates the information quantity (self-information) of an event
    I(x) = -log2(P(x))
    Args:
        probability: Probability of the event (between 0 and 1)
    Returns:
        Information quantity in bits
    """
    if probability <= 0 or probability > 1:
        raise ValueError("Probability must be in the interval ]0, 1]")

    return -math.log2(probability)


def calculate_probabilities(source):
    """
    Calculates the probabilities of elements in a source
    Args:
        source: List or string of symbols
    Returns:
        Dictionary {symbol: probability}
    """
    counter = Counter(source)
    total = len(source)
    probabilities = {symbol: count / total for symbol, count in counter.items()}
    
    return probabilities


def source_entropy(probabilities):
    """
    Calculates the Shannon entropy of a source
    H(X) = -Σ P(x) * log2(P(x))
    Args:
        probabilities: Dictionary {symbol: probability} or list of probabilities
    Returns:
        Entropy in bits
    """
    if isinstance(probabilities, dict):
        probs = list(probabilities.values())
    else:
        probs = probabilities
    
    # Check that sum of probabilities = 1
    total_sum = sum(probs)
    if not total_sum == 1:
        raise ValueError(f"Sum of probabilities must be 1 (sum = {total_sum})")
    
    entropy = 0
    for p in probs:
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy


def analyze_source(source):
    """
    Complete analysis of a source: probabilities, information quantities and entropy
    Args:
        source: List or string of symbols
    Returns:
        None
    """
    print("SOURCE ANALYSIS ", "-" * 35)
    
    
    probabilities = calculate_probabilities(source)
    
    print(f"\nSource: {source}")
    print(f"Number of symbols: {len(source)}")
    print(f"Alphabet: {set(source)}")
    
    print("\n--- Probabilities and Information Quantities ---")
    for symbol, prob in sorted(probabilities.items()):
        info = information_quantity(prob)
        print(f"P({symbol}) = {prob:.2f} → I({symbol}) = {info:.2f} bits")
    
    H = source_entropy(probabilities)
    print(f"\n--- Source Entropy ---")
    print(f"H(X) = {H:.2f} bits")
    print(f"Maximum possible entropy: {math.log2(len(probabilities)):.2f} bits")
    print(f"Efficiency: {H / math.log2(len(probabilities)) * 100:.2f}%")
    print("-" * 50)


# =-----------------------------------------------------------------------------------------------------------------------
# 2/ Joint Entropy, Conditional Entropy and Mutual Information

def calculate_joint_probabilities(source_x, source_y):
    """
    Calculates joint probabilities P(X,Y)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Dictionary {(x, y): P(x, y)}
    """
    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")
    
    pairs = list(zip(source_x, source_y))
    counter = Counter(pairs)
    total = len(pairs)
    
    joint_probabilities = {pair: count / total for pair, count in counter.items()}
    return joint_probabilities


def joint_entropy(joint_probabilities):
    """
    Calculates joint entropy H(X,Y)
    H(X,Y) = -Σ P(x,y) * log2(P(x,y))
    Args:
        joint_probabilities: Dictionary {(x, y): P(x, y)}
    Returns:
        Joint entropy
    """
    H_xy = 0
    for prob in joint_probabilities.values():
        if prob > 0:
            H_xy -= prob * math.log2(prob)
    return H_xy


def conditional_entropy(joint_probabilities, prob_x):
    """
    Calculates average conditional entropy H(Y|X)
    H(Y|X) = -Σ P(x,y) * log2(P(y|x))
           = -Σ P(x,y) * log2(P(x,y) / P(x))
    Args:
        joint_probabilities: Dictionary {(x, y): P(x, y)}
        prob_x: Dictionary {x: P(x)}
    Returns:
        Conditional entropy in bits
    """
    H_y_given_x = 0
    for (x, y), prob_xy in joint_probabilities.items():
        if prob_xy > 0 and prob_x[x] > 0:
            prob_y_given_x = prob_xy / prob_x[x]
            H_y_given_x -= prob_xy * math.log2(prob_y_given_x)
    return H_y_given_x


def mutual_information(joint_probabilities, prob_x, prob_y):
    """
    Calculates mutual information I(X;Y)
    I(X;Y) = Σ P(x,y) * log2(P(x,y) / (P(x) * P(y)))
           = H(X) + H(Y) - H(X,Y)
    Args:
        joint_probabilities: Dictionary {(x, y): P(x, y)}
        prob_x: Dictionary {x: P(x)}
        prob_y: Dictionary {y: P(y)}
    Returns:
        Mutual information in bits
    """
    I_xy = 0
    for (x, y), prob_xy in joint_probabilities.items():
        if prob_xy > 0 and prob_x[x] > 0 and prob_y[y] > 0:
            I_xy += prob_xy * math.log2(prob_xy / (prob_x[x] * prob_y[y]))
    return I_xy


def analyze_two_sources(source_x, source_y):
    """
    Complete analysis of two sources
    Args:
        source_x, source_y: Lists or strings of symbols (same length)
    """
    print("=" * 60)
    print("ANALYSIS OF TWO SOURCES")
    print("=" * 60)
    
    # Calculate probabilities
    prob_x = calculate_probabilities(source_x)
    prob_y = calculate_probabilities(source_y)
    joint_probabilities = calculate_joint_probabilities(source_x, source_y)
    
    print(f"\nSource X: {source_x}")
    print(f"Source Y: {source_y}")
    print(f"Number of observations: {len(source_x)}")
    
    # Marginal entropies
    H_x = source_entropy(prob_x)
    H_y = source_entropy(prob_y)
    
    print("\n--- Marginal Entropies ---")
    print(f"H(X) = {H_x:.4f} bits")
    print(f"H(Y) = {H_y:.4f} bits")
    
    # Joint entropy
    H_xy = joint_entropy(joint_probabilities)
    print("\n--- Joint Entropy ---")
    print(f"H(X,Y) = {H_xy:.4f} bits")
    
    # Conditional entropies
    H_y_given_x = conditional_entropy(joint_probabilities, prob_x)
    H_x_given_y = conditional_entropy(
        {(y, x): p for (x, y), p in joint_probabilities.items()},
        prob_y
    )
    
    print("\n--- Conditional Entropies ---")
    print(f"H(Y|X) = {H_y_given_x:.4f} bits")
    print(f"H(X|Y) = {H_x_given_y:.4f} bits")
    
    # Mutual information
    I_xy = mutual_information(joint_probabilities, prob_x, prob_y)
    
    print("\n--- Mutual Information ---")
    print(f"I(X;Y) = {I_xy:.4f} bits")
    
    # Verifications
    print("\n--- Verifications ---")
    print(f"H(X,Y) = H(X) + H(Y|X) : {H_xy:.4f} = {H_x + H_y_given_x:.4f} ✓" if math.isclose(H_xy, H_x + H_y_given_x, rel_tol=1e-5) else f"H(X,Y) ≠ H(X) + H(Y|X) ✗")
    print(f"I(X;Y) = H(X) + H(Y) - H(X,Y) : {I_xy:.4f} = {H_x + H_y - H_xy:.4f} ✓" if math.isclose(I_xy, H_x + H_y - H_xy, rel_tol=1e-5) else f"I(X;Y) ≠ H(X) + H(Y) - H(X,Y) ✗")
    print(f"I(X;Y) = H(Y) - H(Y|X) : {I_xy:.4f} = {H_y - H_y_given_x:.4f} ✓" if math.isclose(I_xy, H_y - H_y_given_x, rel_tol=1e-5) else f"I(X;Y) ≠ H(Y) - H(Y|X) ✗")
    print()


# -----------------------------------------------------------------------------------------------------------------------
# main menu for terminal

def main_menu():
    while True:
        print("MAIN MENU", "-" * 35)
        print("1. Analyze a single source")
        print("2. Analyze two sources")
        print("3. Enter probabilities manually")
        print("4. Quit")
        choice = input("Enter your choice (1-4) : ")

        if choice == "1":
            source = input("Enter your sequence of symbols (ex: AADCCB) : ")

            analyze_source(source)


        elif choice == "2":
            print("For two sources, enter symbols separated by spaces")
            print("Example: A A B B C for sequence AABBC")

            source_x = input("Enter the first source : ").split()
            source_y = input("Enter the second source : ").split()

            analyze_two_sources(source_x, source_y)


        elif choice == "3":
            print("Enter probabilities in the form 'symbol:probability'")
            print("One entry per line. Press Enter twice to finish.")
            print("Example :")
            print("A:0.4")
            print("B:0.35")
            print("C:0.05")
            print("D:0.2")
            print("(probabilities must sum to 1)")
            probs = {}
            while True:
                line = input()
                if not line:
                    break
                try:
                    symbol, prob = line.split(":")
                    probs[symbol.strip()] = float(prob.strip())
                except:
                    print("Invalid format. Use 'symbol:probability'")
                    continue

            if abs(sum(probs.values()) - 1.0) > 1e-5:
                print("\nError : The sum of probabilities must equal 1 !")
                continue

            print(f"\nEntered probabilities : {probs}")
            print(f"Entropy : {source_entropy(probs):.4f} bits")


        elif choice == "4":
            print("\nGoodbye !", "-" * 35)
            break

if __name__ == "__main__":
    main_menu()
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


def calculate_equiproba(source):
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


def source_entropy(source):
    """
    Calculates the entropy of a source
    H(X) = -Σ P(x) * log2(P(x)) = Σ pi * I(pi)
    Args:
        source: Dictionary {symbol: probability} or list of probabilities
    Returns:
        Entropy in bits/symbol
    """
    entropy = 0.0
    # Accept either a dict of {symbol: prob} or an iterable of probabilities
    probabilities_iter = source.values() if isinstance(source, dict) else source
    for prob in probabilities_iter:
        if prob > 0:
            ProbInfo = information_quantity(prob)
            entropy += ProbInfo * prob
    return entropy


def source_max_entropy(source):
    """
    Calculate the Max entropy of a given source
    Hmax(X) = log2(n) , n = number of elements if the source
    Args:
        source: Dictionary {symbol: probability} or list of probabilities
    return:
        max entropy in bits/symbol
    """

    # Only two supported inputs: dict of probabilities or list of floats
    n = len(source)
    if n <= 0:
        raise ValueError("Source must contain at least one symbol/probability")

    return math.log2(n)






def analyze_source(source):
    """
    Complete analysis of a source: probabilities, information quantities and entropy
    Args:
        source: List or dist of symbols
    Returns:
        None
    """
    print("SOURCE ANALYSIS ", "-" * 35)
    
    print(f"\nSource: {source}")
    print(f"Number of symbols: {len(source)}")
    print(f"Alphabet: {set(source)}")
    
    print("\n--- Probabilities and Information Quantities ---")
    if isinstance(source, dict):
        for symbol, prob in sorted(source.items()):
            info = information_quantity(prob)
            print(f"P({symbol}) = {prob:.2f} → I({symbol}) = {info:.2f} bits")
    else:
        for prob in sorted(source.items()):
            info = information_quantity(prob) 
            print(f"I({prob}) = {info:.2f} bits")

    H = source_entropy(source)
    Hmax = source_max_entropy(source)
    print(f"\n--- Source Entropy ---")
    print(f"H(X) = {H:.2f} bits")
    print(f"Maximum possible entropy: {Hmax:.2f} bits")
    print(f"Efficiency: {(H / Hmax * 100):.2f} %")
    print("-" * 50)


# =-----------------------------------------------------------------------------------------------------------------------
# 2/ Joint Entropy, Conditional Entropy and Mutual Information

def source_joint_entropy_independant(source_x, source_y):
    """
    Calculates joint entropy H(X,Y)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Joint entropy in bits/symbols
    """
    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")
    
    Hx= source_entropy(source_x)
    Hy= source_entropy(source_y)

    return Hx + Hy

def source_joint_entropy_dependent(source_x, source_y):
    """
    Calculates joint entropy H(X,Y)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Joint entropy in bits/symbols
    """
    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")
    
    return source_entropy(source_x)


def conditional_entropy(source_x, source_y):
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
    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")
    
    H_x_given_y = source_joint_entropy_independant(source_x, source_y) - source_entropy(source_y)
    return H_x_given_y



def mutual_information(source_x, source_y):
    """
    Calculates mutual information I(X;Y)
    I(X;Y) = Σ P(x,y) * log2(P(x,y) / (P(x) * P(y)))
           = H(X) + H(Y) - H(X,Y)
    Args:
        source_x, source_y: Lists or dict of symbols (same length)
    Returns:
        Mutual information in bits
    """
    I_xy = source_entropy(source_x) + source_entropy(source_y) - source_joint_entropy_independant(source_x, source_y)
    return I_xy

def joint_probabilities_independant(source_x, source_y):
    """
    Calculate joint probabilities P(x,y)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Dictionary {(x, y): P(x, y)}
    """
    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")

    joint_prob = {}
    for symbol, prob in source_x.items():
        for symbol2, prob2 in source_y.items():
            joint_prob[(symbol, symbol2)] = prob * prob2
    
    return joint_prob



def joint_probabilities_dependent(source_x, source_y):
    """
    Calculate joint probabilities P(x,y)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Dictionary {(x, y): P(x, y)}
    """
    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")

    joint_prob = {}
    cond_prob = conditional_probabilities(source_x, source_y)
    for symbol, prob in source_x.items():
        for symbol2, prob2 in source_y.items():
            joint_prob[(symbol, symbol2)] = cond_prob[symbol, symbol2] * prob2  # P(x,y) = P(x|y) * P(y)
    
    return joint_prob


def conditional_probabilities(source_x, source_y):
    """
    Calculate conditional probabilities P(y|x)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Dictionary {(x, y): P(y|x)}
    """
    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")

    cond_prob = {}
    joint_prob = joint_probabilities_independant(source_x, source_y)
    for symbol, prob in source_x.items():
        for symbol2, prob2 in source_y.items():
            cond_prob[(symbol, symbol2)] =   joint_prob[(symbol, symbol2)] / prob2 if prob2 > 0 else 0  
            # since P(x|y) = P(x,y)/p(y)
    
    return cond_prob


def analyze_two_sources(source_x, source_y, dependant):
    """
    Complete analysis of two sources
    Args:
        source_x, source_y: Lists or strings of symbols (same length)
    """
    print("=" * 60)
    print("ANALYSIS OF TWO SOURCES")
    print("=" * 60)
    
    print(f"\nSource X: {source_x}")
    print(f"Source Y: {source_y}")
    print(f"Number of observations: {len(source_x)}")

    if len(source_x) != len(source_y):
        raise ValueError("The two sources must have the same length")
    
    if not dependant:
        #joint probabilities
        joint_prob = joint_probabilities_independant(source_x, source_y)
        print("\n--- Joint Probabilities P(X,Y) ---")
        for (sym_x, sym_y), prob in sorted(joint_prob.items()):
            print(f"P({sym_x}, {sym_y}) = {prob:.4f}")
        
        #conditional probabilities
        cond_prob = conditional_probabilities(source_x, source_y)
        print("\n--- Conditional Probabilities P(Y|X) ---")
        for (sym_x, sym_y), prob in sorted(cond_prob.items()):
            print(f"P({sym_y}|{sym_x}) = {prob:.4f}")

        # Marginal entropies
        H_x = source_entropy(source_x)
        H_y = source_entropy(source_y)

        print("\n--- Marginal Entropies ---")
        print(f"H(X) = {H_x:.2f} bits")
        print(f"H(Y) = {H_y:.2f} bits")
        
        # Joint entropy
        H_xy = source_joint_entropy_independant(source_x, source_y)
        print("\n--- Joint Entropy ---")
        print(f"H(X,Y) = {H_xy:.2f} bits")
        
        # Conditional entropies
        H_x_given_y = conditional_entropy(source_x, source_y)
        H_y_given_x = conditional_entropy(source_y, source_x)

        print("\n--- Conditional Entropies ---")
        print(f"H(X|Y) = {H_x_given_y:.2f} bits")
        print(f"H(Y|X) = {H_y_given_x:.2f} bits")
        
        # Mutual information
        I_xy = mutual_information(source_x, source_y)
        
        print("\n--- Mutual Information ---")
        print(f"I(X;Y) = {I_xy:.2f} bits")
        
        # Verifications
        print("\n--- Verifications ---")
        print(f"H(X,Y) = H(X) + H(Y|X) : {H_xy:.2f} = {H_x + H_y_given_x:.2f} ✓" if math.isclose(H_xy, H_x + H_y_given_x, rel_tol=1e-5) else f"H(X,Y) ≠ H(X) + H(Y|X) ✗")
        print(f"I(X;Y) = H(X) + H(Y) - H(X,Y) : {I_xy:.2f} = {H_x + H_y - H_xy:.2f} ✓" if math.isclose(I_xy, H_x + H_y - H_xy, rel_tol=1e-5) else f"I(X;Y) ≠ H(X) + H(Y) - H(X,Y) ✗")
        print(f"H(Y|X) = H(X,Y) - H(X) : {H_y_given_x:.2f} = {H_xy - H_x:.2f} ✓" if math.isclose(H_y_given_x, H_xy - H_x, rel_tol=1e-5) else f"H(Y|X) ≠ H(X,Y) - H(X) ✗")
        print(f"H(X|Y) = H(X,Y) - H(Y) : {H_x_given_y:.2f} = {H_xy - H_y:.2f} ✓" if math.isclose(H_x_given_y, H_xy - H_y, rel_tol=1e-5) else f"H(X|Y) ≠ H(X,Y) - H(Y) ✗")
        print()
    else:
        #joint probabilities
        joint_prob = joint_probabilities_dependent(source_x, source_y)
        print("\n--- Joint Probabilities P(X,Y) ---")
        for (sym_x, sym_y), prob in sorted(joint_prob.items()):
            print(f"P({sym_x}, {sym_y}) = {prob:.4f}")

        #conditional probabilities
        cond_prob = conditional_probabilities(source_x, source_y)
        print("\n--- Conditional Probabilities P(Y|X) ---")
        for (sym_x, sym_y), prob in sorted(cond_prob.items()):
            print(f"P({sym_y}|{sym_x}) = {prob:.4f}")
            
        # Marginal entropies
        H_y = source_entropy(source_y)

        print("\n--- Marginal Entropies ---")
        print(f"H(X) = {H_x:.2f} bits")
        print(f"H(Y) = {H_y:.2f} bits")

        # Joint entropy
        H_xy = source_joint_entropy_dependent(source_x, source_y)
        print("\n--- Joint Entropy ---")
        print(f"H(X,Y) = H(X) = H(Y) = {H_xy:.2f} bits")

        # Conditional entropies
        H_y_given_x = conditional_entropy(source_x, source_y)

        print("\n--- Conditional Entropies ---")
        print("since X depends totally on Y then H(X|Y) = 0")
        print(f"H(Y|X) = {H_y_given_x:.2f} bits")

        # Mutual information
        I_xy = mutual_information(source_x, source_y)
        print("\n--- Mutual Information ---")
        print(f"since Y determines totally X then I(X;Y) = H(X) = H(Y) = {H_y:.2f} bits")

        # Verifications
        print("\n--- Verifications ---")
        print(f"H(X,Y) = H(Y) = H(X) : {H_xy:.2f} = {H_y :.2f} ✓")
        print(f"I(X;Y) = H(X) = H(Y) : {I_xy:.2f} = {H_y:.2f} ✓")
        print(f"H(Y|X) = 0 ✓")
        print(f"H(X|Y) = 0 ✓")
        print()


# -----------------------------------------------------------------------------------------------------------------------
# main menu for terminal

def main_menu():
    while True:
        print()
        print()
        print("MAIN MENU", "-" * 35)
        print("1. Analyze a single source")
        print("2. Analyze two sources")
        print("3. Quit")
        choice = input("Enter your choice (1-3) : ")
        print()

        if choice == "1":
            print("Enter your sequence of symbols : \n")
            print("Enter probabilities in the form 'symbol:probability'")
            print("One entry per line. Press Enter twice to finish.")
            print("Example :")
            print("A:0.4")
            print("B:0.35")
            print("C:0.05")
            print("D:0.2")
            print("(probabilities must sum to 1)")
            source = {}
            while True:
                line = input()
                if not line:
                    break
                try:
                    symbol, prob = line.split(":")
                    source[symbol.strip()] = float(prob.strip())
                except:
                    print("Invalid format. Use 'symbol:probability'")
                    continue

            if abs(sum(source.values()) - 1.0) > 1e-5:
                print("\nError : The sum of probabilities must equal 1 !")
                continue

            print(f"\nEntered probabilities : {source.values()}\n")

            analyze_source(source)


        elif choice == "2":
            print("For two sources, enter symbols separated by spaces")
            
            print("Enter probabilities in the form 'symbol:probability'")
            print("One entry per line. Press Enter twice to finish.")
            print("Example :")
            print("A:0.4")
            print("B:0.35")
            print("C:0.05")
            print("D:0.2")
            print("(probabilities must sum to 1)")
            print("SOURCE X :-------")
            source_x = {}
            while True:
                line = input()
                if not line:
                    break
                try:
                    symbol, prob = line.split(":")
                    source_x[symbol.strip()] = float(prob.strip())
                except:
                    print("Invalid format. Use 'symbol:probability'")
                    continue

            if abs(sum(source_x.values()) - 1.0) > 1e-5:
                print("\nError : The sum of probabilities must equal 1 !")
                continue

            print("SOURCE Y :-------")
            source_y = {}
            while True:
                line = input()
                if not line:
                    break
                try:
                    symbol, prob = line.split(":")
                    source_y[symbol.strip()] = float(prob.strip())
                except:
                    print("Invalid format. Use 'symbol:probability'")
                    continue

            if abs(sum(source_y.values()) - 1.0) > 1e-5:
                print("\nError : The sum of probabilities must equal 1 !")
                continue

            print("are the two sources independant ? (y/n) : ")
            dep_choice = input().strip().lower()
            if dep_choice == 'y':
                dependant = False
            elif dep_choice == 'n':
                dependant = True
            else:
                print("Invalid choice. Assuming independant sources.")
                dependant = False

            analyze_two_sources(source_x, source_y, dependant)


        elif choice == "3":
            print("\nGoodbye !", "-" * 35)
            break

if __name__ == "__main__":
    main_menu()
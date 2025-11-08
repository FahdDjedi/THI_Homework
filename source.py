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
            print(f"P({symbol}) = {prob:.5f} → I({symbol}) = {info:.5f} bits")
    else:
        for prob in sorted(source.items()):
            info = information_quantity(prob) 
            print(f"I({prob}) = {info:.5f} bits")

    H = source_entropy(source)
    Hmax = source_max_entropy(source)
    print(f"\n--- Source Entropy ---")
    print(f"H(X) = {H:.5f} bits")
    print(f"Maximum possible entropy: {Hmax:.5f} bits")
    print(f"Efficiency: {(H / Hmax * 100):.5f} %")
    print("-" * 50)


# =-----------------------------------------------------------------------------------------------------------------------
# 2/ Joint Entropy, Conditional Entropy and Mutual Information

def source_joint_entropy_independent(source_x, source_y):
    """
    Calculates joint entropy H(X,Y)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Joint entropy in bits/symbols
    """
    
    
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
    joint_entropy = 0.0
    joint_prob = joint_probabilities_independent(source_x, source_y)
    for (symbol_x, symbol_y), prob in joint_prob.items():
        if prob > 0:
            ProbInfo = information_quantity(prob)
            joint_entropy += ProbInfo * prob

    return joint_entropy



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
    
    
    H_x_given_y = source_joint_entropy_independent(source_x, source_y) - source_entropy(source_y)
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
    I_xy = source_entropy(source_x) + source_entropy(source_y) - source_joint_entropy_dependent(source_x, source_y)
    return I_xy

def joint_probabilities_independent(source_x, source_y):
    """
    Calculate joint probabilities P(x,y)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Dictionary {(x, y): P(x, y)}
    """
    

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
    

    joint_prob = {}
    cond_prob = conditional_probabilities(source_x, source_y)
    for symbol, prob in source_x.items():
        for symbol2, prob2 in source_y.items():
            joint_prob[(symbol, symbol2)] = cond_prob[symbol, symbol2] * prob2  # P(x,y) = P(x|y) * P(y)
    
    return joint_prob

def joint_probabilities_dependent_from_cond(source_x, source_y, cond_prob):
    """
    Calculate joint probabilities P(x,y) from conditional probabilities
    Args:
        source_x: List of symbols
        cond_prob: Dictionary {(x, y): P(x|y)}
    Returns:
        Dictionary {(x, y): P(x,y)}
    """
    joint_prob = {}
    for symbol, prob in sorted(source_x.items()):
        for symbol2, prob2 in sorted(source_y.items()):
           joint_prob[(symbol, symbol2)] = prob * cond_prob[symbol, symbol2]  # P(x,y) = P(x) * P(y|x)
    return joint_prob

def conditional_probabilities(source_x, source_y):
    """
    Calculate conditional probabilities P(y|x)
    Args:
        source_x, source_y: Lists of symbols (same length)
    Returns:
        Dictionary {(x, y): P(y|x)}
    """

    cond_prob = {}
    joint_prob = joint_probabilities_independent(source_x, source_y)
    for symbol, prob in sorted(source_x.items()):
        for symbol2, prob2 in sorted(source_y.items()):
            cond_prob[(symbol, symbol2)] =   joint_prob[(symbol, symbol2)] / prob2 if prob2 > 0 else 0
            # since P(x|y) = P(x,y)/p(y)
    
    return cond_prob

def probabilities_of_a_source_dependant(joint_prob, source_y):
    """
    Calculate probabilities of a dependant source from joint probabilities
    Args:
        joint_prob: Dictionary {(x, y): P(x,y)}
        source_y: List of symbols
    Returns:
        Dictionary {y: P(y)}
    """
    prob_y = {}
    for symbol_y, prob1 in sorted(source_y.items()):
        probtemp = 0
        for (symbol, symbol_y2), prob2 in sorted(joint_prob.items()):
            if symbol_y == symbol_y2:
                probtemp += prob2
                prob_y[symbol_y] = probtemp # P(y) = Σ P(x,y)
    return prob_y



def analyze_two_sources_independent(source_x, source_y):
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

    
    #joint probabilities
    joint_prob = joint_probabilities_independent(source_x, source_y)
    print("\n--- Joint Probabilities P(X,Y) ---")
    for (sym_x, sym_y), prob in sorted(joint_prob.items()):
        print(f"P({sym_x}, {sym_y}) = {prob:.4f}")
    
    #conditional probabilities
    cond_prob = conditional_probabilities(source_x, source_y)
    print("\n--- Conditional Probabilities P(Y|X) ---")
    for (sym_x, sym_y), prob in sorted(cond_prob.items()):
        print(f"P({sym_y}|{sym_x}) = {prob:.4f}")
    print()
    print("\n--- Conditional Probabilities P(X|Y) ---")
    cond_prob_x_given_y = conditional_probabilities(source_y, source_x)
    for (sym_y, sym_x), prob in sorted(cond_prob_x_given_y.items()):
        print(f"P({sym_x}|{sym_y}) = {prob:.4f}")

    # Marginal entropies
    H_x = source_entropy(source_x)
    H_y = source_entropy(source_y)

    print("\n--- Marginal Entropies ---")
    print(f"H(X) = {H_x:.5f} bits/symbol")
    print(f"H(Y) = {H_y:.5f} bits/symbol")

    # Joint entropy
    H_xy = source_joint_entropy_independent(source_x, source_y)
    print("\n--- Joint Entropy ---")
    print(f"H(X,Y) = {H_xy:.5f} bits/symbol")
    
    # Conditional entropies
    H_x_given_y = conditional_entropy(source_x, source_y)
    H_y_given_x = conditional_entropy(source_y, source_x)

    print("\n--- Conditional Entropies ---")
    print(f"H(X|Y) = {H_x_given_y:.5f} bits/symbol")
    print(f"H(Y|X) = {H_y_given_x:.5f} bits/symbol")

    # Mutual information
    I_xy = mutual_information(source_x, source_y)
    
    print("\n--- Mutual Information ---")
    print(f"I(X;Y) = {I_xy:.5f} bits")
    
    # Verifications
    print("\n--- Verifications ---")
    print(f"H(X,Y) = H(X) + H(Y|X) : {H_xy:.5f} = {H_x + H_y_given_x:.5f} ✓" if math.isclose(H_xy, H_x + H_y_given_x, rel_tol=1e-5) else f"H(X,Y) ≠ H(X) + H(Y|X) ✗")
    print(f"I(X;Y) = H(X) + H(Y) - H(X,Y) : {I_xy:.5f} = {H_x + H_y - H_xy:.5f} ✓" if math.isclose(I_xy, H_x + H_y - H_xy, rel_tol=1e-5) else f"I(X;Y) ≠ H(X) + H(Y) - H(X,Y) ✗")
    print(f"H(Y|X) = H(X,Y) - H(X) : {H_y_given_x:.5f} = {H_xy - H_x:.5f} ✓" if math.isclose(H_y_given_x, H_xy - H_x, rel_tol=1e-5) else f"H(Y|X) ≠ H(X,Y) - H(X) ✗")
    print(f"H(X|Y) = H(X,Y) - H(Y) : {H_x_given_y:.5f} = {H_xy - H_y:.5f} ✓" if math.isclose(H_x_given_y, H_xy - H_y, rel_tol=1e-5) else f"H(X|Y) ≠ H(X,Y) - H(Y) ✗")
    print()
    

def analyze_two_sources_dependent(source_x, source_y, prob_y_given_x):
    """
    Complete analysis of two dependant sources
    Args:
        source_x, source_y: Lists or strings of symbols (same length)
        prob_y_given_x: Dictionary {(x, y): P(y|x)}
    """
    print("=" * 60)
    print("ANALYSIS OF TWO DEPENDANT SOURCES")
    print("=" * 60)
    
    print(f"\nSource X: {source_x}")
    print(f"Source Y: {source_y}")


    
    #joint probabilities
    joint_prob = joint_probabilities_dependent_from_cond(source_x, source_y, prob_y_given_x)
    print("\n--- Joint Probabilities P(X,Y) ---")
    for (sym_x, sym_y), prob in sorted(joint_prob.items()):
        print(f"P({sym_x}, {sym_y}) = {prob:.4f}")

    #probabilities of the source y 
    NewSource_y = {}
    prob_y = probabilities_of_a_source_dependant(joint_prob, source_y)
    print("\n--- Probabilities of Source Y P(Y) ---")
    for symbol_y, prob in sorted(prob_y.items()):
        print(f"P({symbol_y}) = {prob:.4f}")
        NewSource_y[symbol_y] = prob

    #conditional probabilities
    print("\n--- Conditional Probabilities P(Y|X) ---")
    for (sym_x, sym_y), prob in sorted(prob_y_given_x.items()):
        print(f"P({sym_y}|{sym_x}) = {prob:.4f}")
    print()
    print("\n--- Conditional Probabilities P(X|Y) ---")
    cond_prob_x_given_y = conditional_probabilities(source_x, NewSource_y)
    for (sym_x, sym_y), prob in sorted(cond_prob_x_given_y.items()):
        print(f"P({sym_x}|{sym_y}) = {prob:.4f}")


    # Marginal entropies
    H_x = source_entropy(source_x)
    H_y = source_entropy(NewSource_y)

    print("\n--- Marginal Entropies ---")
    print(f"H(X) = {H_x:.5f} bits/symbol")
    print(f"H(Y) = {H_y:.5f} bits/symbol")
    
    # Joint entropy
    H_xy = source_joint_entropy_dependent(source_x, NewSource_y)
    print("\n--- Joint Entropy ---")
    print(f"H(X,Y) = {H_xy:.5f} bits")

    # Conditional entropies
    H_x_given_y = conditional_entropy(source_x, NewSource_y)
    H_y_given_x = conditional_entropy(NewSource_y, source_x)
    print("\n--- Conditional Entropies ---")
    print(f"H(X|Y) = {H_x_given_y:.5f} bits/symbol")
    print(f"H(Y|X) = {H_y_given_x:.5f} bits/symbol")

    # Mutual information
    I_xy = mutual_information(source_x, NewSource_y)
    
    print("\n--- Mutual Information ---")
    print(f"I(X;Y) = {I_xy:.5f} bits/symbol")



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

            print("are the two sources independent ? (y/n) : ")
            dep_choice = input().strip().lower()
            print()
            print()
            if dep_choice == 'y':
                dependant = False
            elif dep_choice == 'n':
                dependant = True
            else:
                print("Invalid choice. Assuming independent sources.")
                dependant = False

            if dependant:
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

                print("PROBABILITIES OF P(Y|X) :-------")
                print("Enter conditional probabilities in the form 'symbol_y|symbol_x:probability'")
                print("One entry per line. Press Enter twice to finish.")
                prob_y_given_x = {}
                while True:
                    line = input()
                    if not line:
                        break
                    try:
                        symbol_pair, prob = line.split(":")
                        symbol_y, symbol_x = symbol_pair.split("|")
                        prob_y_given_x[(symbol_x.strip(), symbol_y.strip())] = float(prob.strip())
                    except:
                        print("Invalid format. Use 'symbol_y|symbol_x:probability'")
                        continue

                print("SOURCE Y :-------")
                print("Enter symbols in the form 'symbol'")
                source_y = {}
                while True:
                    line = input()
                    if not line:
                        break
                    symbol = line.strip()
                    source_y[symbol.strip()] = "?"
                
                analyze_two_sources_dependent(source_x, source_y, prob_y_given_x)
            elif not dependant:
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
                analyze_two_sources_independent(source_x, source_y)
        elif choice == "3":
            print("\nGoodbye !", "-" * 35)
            break

if __name__ == "__main__":
    main_menu()
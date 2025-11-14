import math
from operator import index

PROB_KEY = 'prob'
CODE_KEY = 'code'
LEN_KEY = 'len'

#huffman code calculation
def Huffman_code(source):
    source = dict(sorted(source.items(), key=lambda item: item[1]))
    #save a copy of the list 
    save_source = source.copy()

    #create a dictionary to store the huffman codes
    huffman_source = {
        symbol: {PROB_KEY: prob, CODE_KEY: "", LEN_KEY: 0}
        for symbol, prob in source.items()
    }

    while len(source) > 1:
        #get the two symbols with the lowest probabilities
        symbols = list(source.keys())
        sym1 = symbols[0]
        sym2 = symbols[1]

        #assign codes
        for symbol in sym1:
            huffman_source[symbol][CODE_KEY] = '0' + huffman_source[symbol][CODE_KEY]
        for symbol in sym2:
            huffman_source[symbol][CODE_KEY] = '1' + huffman_source[symbol][CODE_KEY]

        #combine the two symbols
        new_symbol = sym1 + sym2
        new_prob = source[sym1] + source[sym2]

        #remove the two symbols from the source
        source.pop(sym1)
        source.pop(sym2)

        #add the new symbol to the source
        source[new_symbol] = new_prob

        #sort the source by probability
        source = dict(sorted(source.items(), key=lambda item: item[1]))

    source = save_source.copy()
        
    return huffman_source


#calculate length of each code
def length_huffman(huffman_source):
    #calculate length of each code
    for symbol, info in huffman_source.items():
        info[LEN_KEY] = len(info[CODE_KEY])



#calculate entropy of the source
def entropy(source):
    entropy = 0
    #calculate entropy
    for symbol, info in source.items():
        if info[PROB_KEY] > 0:
            entropy += info[PROB_KEY] * math.log2(1/info[PROB_KEY])
    return entropy


#calculate average length of the huffman source
def average_length(huffman_source):
    return sum(info[PROB_KEY] * info[LEN_KEY] for info in huffman_source.values())


#calculate the efficency of the huffman source
def efficiency(source):
    #calculate efficiency
    return entropy(source) / average_length(source)


def main():
    #main menu
    print()
    print()
    print("=" * 20)
    print("HUFFMAN CODING PROGRAM")
    print("=" * 20)
    print()
    print()
    #define the source
    print("------SOURCE INPUT------")
    print()
    print("Enter your sequence of symbols : \n")
    print("Enter probabilities in the form 'symbol:probability'")
    print("One entry per line. Press Enter twice to finish.")
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
            print("ERROR INVALID FORMAT. Use 'symbol:probability'")
            continue

    if abs(sum(source.values()) != 1):
        print("\nError : The sum of probabilities must equal 1 !")
        print(f"Current sum: {sum(source.values()):.4f}")
        raise SystemExit(1)

    print(f"\nEntered probabilities : {source}\n")
    print()
    print("------HUFFMAN CODING------")
    print()
    huffman_source = Huffman_code(source)
    length_huffman(huffman_source)
    avg_len = average_length(huffman_source)
    ent = entropy(huffman_source)
    eff = efficiency(huffman_source)

    for symbol, info in huffman_source.items():
        print(f"Symbol: {symbol} | Probability: {info[PROB_KEY]} | Code: {info[CODE_KEY]} | Length: {info[LEN_KEY]}")

    print()
    print("------RESULTS------")
    print()
    print(f"AVERAGE LENGTH : avg_len(huffman_source) = Σ Pi * li = {avg_len}")
    print()
    print(f"ENTROPY : H(huffman_source) = Σ Pi * log2(Pi) = {ent}")
    print()
    print(f"EFFICIENCY : eff(huffman_source) = H(huffman_source) / avg_len(huffman_source) = {eff * 100} %")



if __name__ == "__main__":
    main()
    #source = {'A': 0.4, 'B': 0.3, 'C': 0.3}
    #huffman_source = Huffman_code(source)
    #length_huffman(huffman_source)
    #avg_len = average_length(huffman_source)
    #ent = entropy(huffman_source)
    #eff = efficiency(huffman_source)
    #print("Test Run with source {'A': 0.4, 'B': 0.3, 'C': 0.3}")
    #print(f"\nEntered probabilities : {source}\n")
    #print()
    #print("------HUFFMAN CODING------")
    #print()
    #
    #for symbol, info in huffman_source.items():
    #    print(f"Symbol: {symbol} | Probability: {info[PROB_KEY]} | Code: {info[CODE_KEY]} | Length: {info[LEN_KEY]}")

    #print()
    #print("------RESULTS------")
    #print()
    #print(f"AVERAGE LENGTH : avg_len(huffman_source) = Σ Pi * li = {avg_len}")
    #print()
    #print(f"ENTROPY : H(huffman_source) = Σ Pi * log2(Pi) = {ent}")
    #print()
    #print(f"EFFICIENCY : eff(huffman_source) = H(huffman_source) / avg_len(huffman_source) = {eff * 100} %")
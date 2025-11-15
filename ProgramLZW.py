def compress(text, dictionary):
    # dictionary is assumed to be a dict: key = string, value = memory number (int)
    buffer = "" # start with empty word
    output = {} # list of output codes
    next_code = 256 # next available code

    for current in text:
        entry = buffer + current # input = w + c

        if entry in dictionary:
            buffer = entry # w = w + c
        else:
            dictionary[entry] = next_code # save w + c in dict
            next_code += 1

            output[buffer] = dictionary[buffer] # output w

            buffer = current # w ← c

    if buffer:
        output[buffer] = dictionary[buffer] # at the end of the text if w not empty we output w once more

    return output

def decompress(text, dictionary):
    buffer = ""
    output = ""



    return output

def main() :
    
    return

if __name__ == "__main__" :
    # testing
    dictionary = {
        "A": 65,
        "B": 66
    }
    output = compress("ABABABA", dictionary)
    for symbol, memory in output.items(): 
        if memory < 256 :
            print(f'{symbol} ', end="")
        else :
            print(f'<{memory}> ', end="")
    print()
    print()
    print("-------------")
    print()
    print(dictionary)
    print()
    print(len(output))
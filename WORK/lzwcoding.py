import math 

def compress(text, dictionary, size):
    """
    text : a string of characters from a given dictonary of alphabets and sumbols
    dictionary : dict mapping initial codes → characters (ex: {A:'65', B:'66', ...})
    """
    # dictionary is assumed to be a dict: key = string, value = memory number (int)
    buffer = "" # start with empty word
    output_codes = [] # list of output codes (integers)
    table_data = [] # To store intermediate steps for display

    next_code = 2 ** size # next available code
    new_dict = {
        symbol: memory
        for symbol, memory in dictionary.items()
    }
    
    buffer = "" # start with empty word

    for char_c in text:
        entry_wc = buffer + char_c # input = w + c

        w_val = buffer
        c_val = char_c
        wc_val = entry_wc
        sortie_val = ""
        dictionnaire_val = ""

        if entry_wc in new_dict:
            buffer = entry_wc # w = w + c
        else:
            new_dict[entry_wc] = next_code # save w + c in dict
            dictionnaire_val = f"{entry_wc} = <{next_code}>"
            next_code += 1

            output_code = new_dict[buffer]
            output_codes.append(output_code) # output w
            sortie_val = f"<{output_code}>" if output_code >= (2**size) else buffer # Display symbol if it's an initial code, else its code

            buffer = char_c # w ← c
        
        table_data.append({
            'w': w_val,
            'c': c_val,
            'wc': wc_val,
            'sortie': sortie_val,
            'dictionnaire': dictionnaire_val
        })

    if buffer:
        output_code = new_dict[buffer]
        output_codes.append(output_code) # at the end of the text if w not empty we output w once more
        table_data.append({
            'w': buffer,
            'c': '', # No 'c' for the last buffer output
            'wc': buffer,
            'sortie': f"<{output_code}>" if output_code >= (2**size) else buffer,
            'dictionnaire': ''
        })

    return output_codes, new_dict, table_data

def decompress(code_list, initial_code_to_char_dict, size):
    """
    code_list : list of integer codes (compressed data)
    initial_code_to_char_dict : dict mapping initial codes (integers) → characters (strings)
    """

    decompression_table_data = [] # To store intermediate steps for display

    next_code_val = 2 ** size # next available code
    new_dict = {}
    for memory, symbol in initial_code_to_char_dict.items(): # Initial dictionary is code:symbol
        new_dict[memory] = symbol

    output = ""
    table_ouptup = ""
    buffer = ""
    
    # Handle the first code
    current_code = code_list[0]
    entry = new_dict[current_code]
    output += entry
    table_ouptup = entry
    buffer = entry

    decompression_table_data.append({
        'code': f"<{current_code}>",
        'w': '', # 'w' is empty for the first step
        'entry': entry,
        'output': table_ouptup,
        'dictionnaire': ''
    })

    # Loop for the rest of the codes
    for i in range(1, len(code_list)):
        prev_buffer = buffer # Store previous buffer for dictionary addition
        current_code = code_list[i]
        dictionnaire_val = ""

        if current_code in new_dict:
            entry = new_dict[current_code]
        else:
            # If code is not in dictionary, it must be w + w[0]
            entry = buffer + buffer[0]

        output += entry

        # Add new entry to dictionary
        new_dict_entry_string = prev_buffer + entry[0]
        new_dict[next_code_val] = new_dict_entry_string
        dictionnaire_val = f"{next_code_val} = '{new_dict_entry_string}'"
        next_code_val += 1

        buffer = entry # Update buffer for next iteration

        decompression_table_data.append({
            'code': f"<{current_code}>",
            'w': prev_buffer,
            'entry': entry,
            'new_dict_entry_string': new_dict_entry_string, # New column
            'output': entry,
            'dictionnaire': dictionnaire_val
        })

    return output, new_dict, decompression_table_data

def display_compression_table(table_data):
    print("\n--- LZW Compression Table ---")
    headers = ["w", "c", "wc", "sortie", "dictionnaire"]
    
    # Calculate maximum column widths
    col_widths = {header: len(header) for header in headers}
    for row in table_data:
        for header in headers:
            col_widths[header] = max(col_widths[header], len(str(row[header])))

    # Print header
    header_line = " | ".join(header.ljust(col_widths[header]) for header in headers)
    print(header_line)
    print("-+-".join("-" * col_widths[header] for header in headers))

    # Print data rows
    for row in table_data:
        row_line = " | ".join(str(row[header]).ljust(col_widths[header]) for header in headers)
        print(row_line)


def display_decompression_table(table_data):
    print("\n--- LZW Decompression Table ---")
    headers = ["code", "w", "entry", "w + entry[0]", "output", "dictionnaire"]
    
    # Calculate maximum column widths
    col_widths = {header: len(header) for header in headers}
    for row in table_data:
        for header in headers:
            # Handle the new column name for width calculation
            if header == "w + entry[0]":
                col_widths[header] = max(col_widths[header], len(str(row.get('new_dict_entry_string', ''))))
            else:
                col_widths[header] = max(col_widths[header], len(str(row[header])))

    # Print header
    header_line = " | ".join(header.ljust(col_widths[header]) for header in headers)
    print(header_line)
    print("-+-".join("-" * col_widths[header] for header in headers))

    # Print data rows
    for row in table_data:
        row_values = []
        for header in headers:
            if header == "w + entry[0]":
                row_values.append(str(row.get('new_dict_entry_string', '')).ljust(col_widths[header]))
            else:
                row_values.append(str(row[header]).ljust(col_widths[header]))
        row_line = " | ".join(row_values)
        print(row_line)

def main():
    print()
    print("=" * 20)
    print("LZW COMPRESSION/DECOMPRESSION PROGRAM")
    print("=" * 20)
    print()

    while True:
        
        initial_dict = {chr(i): i for i in range(256)}
        final_dict = initial_dict
        print("\nMAIN MENU")
        print("1. Compress a text")
        print("2. Decompress a code")
        print("3. Quit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print()
            print("-" * 50)
            print()
            text = input("Enter the text to compress : ")
            
            size_input = input("What is the initial dictionary size (e.g., 8 for ASCII): ")
            try:
                size = int(size_input)
            except ValueError:
                print("Invalid size. Using default size of 8.")
                size = 8
            
            compressed_output_codes, final_dict, table_data = compress(text, initial_dict, size)

            display_compression_table(table_data)

            print("\n--- Final Compressed Output ---")
            print("Codes: ", end="")
            for code in compressed_output_codes:
                print(f"<{code}>", end=" ")
            print("\n")
            print("Output: ", end ="")
            for code in compressed_output_codes:
                if code < (2**size): # Use 2**size for initial dictionary size
                    print(f"'{chr(code)}'", end=" ")
                else:
                    print(f"<{code}>", end=" ")

            print("\n---Final Dictionary addings:---")
            for symbol, memory in final_dict.items():
                if memory >= 2 ** size :
                    print(f'{symbol} : {memory}')
            
            print()
            print(f'old lenght was: {len(text)} * 8 = {len(text) * 8}')
            print(f'new lenght is: {len(compressed_output_codes)} * 9 = {len(compressed_output_codes) * 9}')
            print(f'compression rate is = {len(compressed_output_codes)/len(text)}')
            print()
            print("-" * 50)

        elif choice == '2':
            print()
            print("-" * 50)
            print()
            print("Enter the compressed codes as a space-separated sequence of integers.")
            print("Example: 65 66 256 258")
            print()
            codes_input_str = input("Enter codes: ")
            try:
                compressed_code_list = [int(code_str) for code_str in codes_input_str.split()]
            except ValueError:
                print("Invalid input. Please enter space-separated integers.")
                continue

            print()
            size_input = input("What is the initial dictionary size (e.g., 8 for ASCII): ")
            try:
                size = int(size_input)
            except ValueError:
                print("Invalid size. Using default size of 8.")
                size = 8
            
            # Reconstruct initial dictionary for decompression (code:char mapping)
            initial_code_to_char_dict = {i: chr(i) for i in range(2**size)}

            decompressed_text, decomp_dict, decompression_table_data = decompress(compressed_code_list, initial_code_to_char_dict, size)
            
            display_decompression_table(decompression_table_data)

            print("\n--- Decompression Results ---")
            print(f"Decompressed Text: {decompressed_text}")
            print()
            print("\n---Final Dictionary addings:---")
            for symbol, memory in final_dict.items():
                if memory >= 2 ** size :
                    print(f'{symbol} : {memory}')
            print()
            print("-" * 50)

        elif choice == '3':
            print()
            print("Goodbye!")
            print() * 4
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    # testing
    
    #dictionary = {
    #    "A": 65,
    #    "B": 66
    #}
    #output, new_dict = compress("ABABABA", dictionary, 8)
    #for symbol, memory in output.items(): 
    #    if memory < 256 :
    #        print(f'{symbol} ', end="")
    #    else :
    #        print(f'<{memory}> ', end="")
    #print()
    #print()
    #print("-------------")
    #print()
    #print(new_dict)
    #print()
    #print(len(output))
    #print()
    #print("-------------")
    #print(dictionary)
    #output2, new_dict2 = decompress(output, dictionary, 8)
    #print(output)
    #print()
    #print()
    #print("-------------")
    #print()
    #print(new_dict)
    #print()
    #print(output2)
    #print()

if __name__ == "__main__":
    main()

'''
#################################################################

    Project #1      : Combinational Logic Simulator (Python)
    Class           : ECE 480 - Software Engineering
    Instructor      : Dr. Chandra
    Date            : January 10, 2014
    
    Group           : Orr Karney
                      Christian Miranda
                      Kevin Sellon
                      Jesse Taylor

#################################################################
'''

import sys

MAX_GATES =     50      # Maximum number of gates allowed.
MAX_IO =        26      # Maximum number of input and outputs allowed.
MAX_FANIN =     8       # Maximum fan-in of devices

# Command list used to translate LDF boolean expressions to python eval boolean expressions.
commands = {'AND': '&', 'OR': '|', 'XOR': '^','NAND':'&','XNOR':'^','NOR':'|'}

def read_file():
    if (len(sys.argv) > 1):
        inputFile = open(sys.argv[1])
        args = []
        file = lines = [line.strip() for line in inputFile]
        args = [None]*len(file)
        for y in range(0, len(file)):
            args[y] = file[y].split();
        inputFile.close()
        return args
    else:
        print('No input file found.')
        sys.exit()

# Organize file lines by gate index.
def organize_array(array):
    # Added a double pass to ensure everything gets organized.
    for a in range(2):
        for x in range (1,len(array)):
            node_number = array[x-1][0]
            if (eval(node_number) != x):
                swap = array[eval(node_number)-1]
                array[eval(node_number)-1] = array[x-1]
                array[x-1] = swap

# Recursively obtain boolean expressions
def recursive_logic (node,array):
    if (array[node-1][2] == 'NOT'):
        if (array[node-1][3].isalpha()):
            return "inv("+array[node-1][3]+")"
        else:
            logic_equ="inv(" + recursive_logic((eval(array[node-1][x])),array) + ")"
    for x in range (3,len(array[node-1])):
        if (x==3):
            if (array[node-1][x].isalpha()):
                logic_equ = array[node-1][x]
            else:
                logic_equ="(" + recursive_logic((eval(array[node-1][x])),array) + ")"
        else:
            if (array[node-1][x].isalpha()):
                logic_equ=logic_equ + commands[array[node-1][2]] + array[node-1][x]
            else:
                logic_equ=logic_equ + commands[array[node-1][2]] + "(" + recursive_logic((eval(array[node-1][x])),array) + ")"
    if (array[node-1][2] == 'NAND' or array[node-1][2] == 'NOR' or array[node-1][2] == 'XNOR'):
        return "inv(" + logic_equ + ")"
    else:
        return logic_equ



# Find output nodes from netlist
def find_top_nodes(array):
    top_node_list = []
    for x in range (0,len(array)):
        top_node_list.append(array[x][0])
    for x in range (0,len(array)):
        for y in range (3,len(array[x])):
            for z in range (0,len(top_node_list)):
                if (array[x][y] == top_node_list[z]):
                    #print(top_node_list)
                    top_node_list.remove(array[x][y])
                    break
    return top_node_list

# Convert int to binary bit array
def binary_dict(integer,input_array):
    b_dict = {}
    bin_number = bin(integer)[2:]
    bin_number = bin_number.zfill(len(input_array))
    values = []
    values.extend(bin_number)
    for x in range (len(input_array)):
        b_dict[input_array[x]] = values[x]
    return b_dict

# Find all alphabetic inputs (A-Z)
def find_base_input(array):
    inputs =[]
    for x in range (0,len(array)):
        for y in range (3,len(array[x])):
            if (array[x][y].isalpha()):
                if (inputs == []):
                    inputs.append(array[x][y])
                else:
                    shouldadd = True
                    for item in inputs:
                        if (array[x][y] == item):
                            shouldadd = False
                            break
                    if(shouldadd):
                        inputs.append(array[x][y])
    return inputs

# Simulate boolean expressions with all possible inputs
def simulate_logic (input_array,node_array,file_array):
    #creates input+output X input**2+1
    simulate_array=[[] for y in range ((2**len(input_array))+1)]
    simulate_array[0].extend(input_array)
    for x in range (len(node_array)):
        simulate_array[0].append(file_array[eval(node_array[x])-1][1])
    #create dictionary for logic equations useing recursion method
    logic_dict = {}
    for x in range (len(node_array)):
        logic_dict[node_array[x]]=recursive_logic(eval(node_array[x]),file_array)
    # create dicitonary for lookup and simulate
    for x in range (2**len(input_array)):
        b_dict = binary_dict(x,input_array)
        for y in range (len(input_array)):
            exec(input_array[y] + "=" + b_dict[input_array[y]])
            simulate_array[x+1].append(b_dict[input_array[y]])
        for z in range (len(node_array)):
            simulate_array[x+1].append(eval(logic_dict[node_array[z]]))
    return simulate_array

# Print multidimensional array with a better visual
def array_print(array):
    for x in range (len(array)):
        print(array[x])

# Not logic (regular not expression returns boolean instead of binary)
def inv(logic_equ):
    return 0 if logic_equ else 1

# Display netlist
def display_netlist(netlist):
    output = "Circuit Listing\n"
    output += "---------------\n"

    for x in range (len(netlist)):
        for y in range (len(netlist[x])):
            output += netlist[x][y] + '\t'
        output += "\n"
    return output

# Display truth table
def display_truthtable(truthtable):
    output = "Truth Table for Selected Outputs\n"
    output += "--------------------------------\n"

    for x in range (len(truthtable)):
        for y in range (len(truthtable[x])):
            #widths.append(len(max(truthtable[x][y], key=len)))
            output += str(truthtable[x][y]).ljust(6)
        output += "\n"
        if (x==0):
            output += "\n"
    return output

# Save display
def save_display (filename,output):
    f = open(filename,'w')
    f.write(output)
    f.close

# Validate gate count
def validate_gate_count(array):
    if (len(array) > MAX_GATES):
        print("Maximum number of gates (%d) exceeded." % MAX_GATES)
        sys.exit()

# Validate circuit input or output count
def validate_io_count(array, io):
    if (len(array) > MAX_IO):
        out = "Maximum number of "
        #       out += ("inputs" if io==0 else "outputs")
        out += ("inputs", "outputs")[io]
        out += " (%d) exceeded." % MAX_IO
        print(out)
        sys.exit()


def main():
    
    # Read netlist from file
    netlist = read_file()
    
    # Determine the number of gates in circuit
    validate_gate_count(netlist);
    
    # Organize netlist in ascending order
    organize_array(netlist)
    
    # Finds all inputs and validate input count
    inputs = find_base_input(netlist)
    validate_io_count(inputs, 0)
    
    # Finds all output nodes
    top_nodes = find_top_nodes(netlist)
    validate_io_count(top_nodes, 1)
    
    # Simulate logic
    simulate = simulate_logic(inputs,top_nodes,netlist)
    
    # Display netlist
    output = display_netlist(netlist)
    output += "\n\n"
    
    # Display truth table
    output += display_truthtable(simulate)
    
    # Save or display results
    if (len(sys.argv) == 3):
        save_display(sys.argv[2],output)

    # Print output to screen regardless of disk operations.
    print(output)

main()

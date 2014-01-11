#first file of project 1

import sys

MAX_GATES   = 50
MAX_PIO     = 26
MAX_NAME    = 12
MAX_TYPE    = 5
MAX_INP     = 8

commands = {'AND': '&', 'OR': '|', 'XOR': '^','NAND':'&','XNOR':'^','NOR':'|'}

# DEBUG - file = ['6\tCARRY\tOR\t3\t4\t5', '1\tXOR1\tXOR\tA\tB', '3\tAND2\tAND\tA\tC', '4\tAND1\tAND\tA\tB', '5\tAND3\tAND\tB\tC', '2\tSUM\tXOR\t1\tC']
# DEBUG -file = ['1\tNOTA\tNOT\tA', '2\tNOTB\tNOT\tB', '3\tY0\tAND\t1\t2', '4\tY1\tAND\t1\tB', '5\tY2\tAND\t2\tA', '6\tY3\tAND\tA\tB']

# Load file lines into array.
''' For DEBUG -
def read_file (file):
    args = [None]*len(file)
    for y in range(0, len(file)):
        args[y] = file[y].split();
    return args'''
def read_file():
    if(len(sys.argv)>1):
        input_file =  open(sys.argv[1])
        file = lines = [line.strip() for line in input_file]
        input_file.close()
        print(file)
        return file
    else:
        print("No input file...")
        sys.exit()

# Organize file lines by gate index.
def organize_array(array):
    for x in range (1,len(array)):
        node_number = array[x-1][0]
        if (eval(node_number) != x):
            swap = array[eval(node_number)-1]
            array[eval(node_number)-1] = array[x-1]
            array[x-1] = swap

# Creates logic function for each node - use only after read_file and sort
def create_logic_functions(array):
    logic_equs=[]#creates empty list for logic equations
    for x in range (0,len(array)):  #loop netlist from node 1 to last ndoe
        if(array[x][3].isalpha()):  #if the input is alphabetic
            logic_equs.append(array[x][3]) # create new list element and add input
        else:
            logic_equs.append("(" + logic_equs[eval(array[x][3])-1] + ")")# adds logic equation called from earlier logic equation
        for y in range (4,len(array[x])):
            if(array[x][y].isalpha()):
                logic_equs[x] = logic_equs[x] + commands[array[x][2]] + array[x][y]
            else:
                logic_equs[x] = logic_equs[x] + commands[array[x][2]] + "(" + logic_equs[eval(array[x][y])-1] + ")"

    return logic_equs
# logic function recursively
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



#finds top nodes of logic equations
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

#decimal to binary
def binary_dict(integer,input_array):
    b_dict = {}
    bin_number = bin(integer)[2:]
    bin_number = bin_number.zfill(len(input_array))
    values = []
    values.extend(bin_number)
    for x in range (len(input_array)):
        b_dict[input_array[x]] = values[x]
    return b_dict

#find all alphabetic inputs
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

#print_array function
def array_print(array):
    for x in range (len(array)):
        print(array[x])

def inv(logic_equ):
    return 0 if logic_equ else 1

def display_netlist(netlist):
    output =  "Circuit Listing\n"
    output += "---------------\n"
    for x in range (len(netlist)):
        for y in range (len(netlist[x])):
            output += netlist[x][y] + "\t"
        output += "\n"
    return output

def display_truthtable(truthtable):
    output =  "Truth Table for Selected Outputs\n"
    output += "--------------------------------\n"
    for x in range (len(truthtable)):
        for y in range (len(truthtable[x])):
            output += truthtable[x][y] + "\t"
        output += "\n"
    return output

def save_display (filename,output):  
    if (len(sys.argv) == 3):
        f = open(filename,'w')
        f.write(output)
        f.close
    else:
        print(output)
  
    
def main():
    #read netlist from file
    netlist = read_file()
    #sets netlist in ascending order
    organize_array(netlist)
    #finds all inputs that are not nodes
    inputs = find_base_input(netlist)
    #print(inputs)
    #finds all nodes not used as inputs
    top_nodes = find_top_nodes(netlist)
    #print(top_nodes)
    #creates logic equations by recursion
    #simulates for all bit combinations
    #outputs into array
    simulate = simulate_logic(inputs,top_nodes,netlist)
    #display netlist
    output = display_netlist(netlist)
    #display truthtable
    output += "\n\n" + display_truthtable(simulate)
    #save truth table to file
    save_display(sys.argv[2],output)
    
main()

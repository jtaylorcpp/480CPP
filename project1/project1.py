#first file of project 1
MAX_GATES   = 50
MAX_PIO     = 26
MAX_NAME    = 12
MAX_TYPE    = 5
MAX_INP     = 8

commands = {'AND': '&', 'OR': '|', 'XOR': '^'}

file = ['6\tCARRY\tOR\t3\t4\t5', '1\tXOR1\tXOR\tA\tB', '3\tAND2\tAND\tA\tC', '4\tAND1\tAND\tA\tB', '5\tAND3\tAND\tB\tC', '2\tSUM\tXOR\t1\tC']

# Load file lines into array.
def read_file (file):
    args = [None]*len(file)
    for y in range(0, len(file)):
        args[y] = file[y].split();
    return args

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
    for x in range (0,len(array)-1):#finds number of total node lines
        logic_equations[x]=array[x][3]#sets initial input to first in list (position 4 from sorted list)
        for y in range (4,len(array[x])-1):#from position 4 forward - include inputs
            if (array[x][y].isalpha()):# is input is alphabetic it is added directly to equation
                logic_equation[x]=logic_equation[x] + commands[array[x][2]] + array[x][y]
            else:#else, in () add equation from earlier node
                logic_equation[x]=logic_equation[x] + commands[array[x][2]] + "(" + loggic_equation[eval(array[x][y])]+ ")"
    return logic_equation

# Print nodes array to check organization.
for z in range(0, len(nodes)):
    print (nodes[z])

#print array
def print_array(array):
    for x in range (0,len(array)):
        print(array[x])

# From this point on, everything is still in the works.
A = 1;
B = 1;
C = 1;
one = 1;
str = ''
stop = 0
    #while (stop <= len(nodes)):
for z in range(0, len(nodes)):
    if (nodes[z][3].isdigit()):
        str = result[int(nodes[z][3])-1]
    else:
        str = nodes[z][3]
    print (str)
    for y in range(0, len(nodes[z])-4):
        str += commands[int(nodes[z][2])]
        if (nodes[z][y+4].isdigit()):
            #str += result[int(nodes[z][y+4])-1]
            print('isDigit: ' + result[int(nodes[z][y+4])-1])
        else:
            str += nodes[z][y+4]
    result[int(nodes[z][0])-1] = eval(str)
    print(int(nodes[z][0])-1)
    print (str + '\n')

#stop += 5;

#for q in range(0, len(result)):
#    print (result[q])

output = '\n\nCircuit Listing\n-------------------\n'
for z in range(0, len(nodes)):
    for y in range(0, len(nodes[z])):
        output += nodes[z][y] + '\t'
    output += '\n'

output += '\n\nTruth Table for the Selected Outputs\n-------------------------------------\n'
print(output)

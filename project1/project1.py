#first file of project 1
MAX_GATES   = 50
MAX_PIO     = 26
MAX_NAME    = 12
MAX_TYPE    = 5
MAX_INP     = 8

commands = {'AND': '&', 'OR': '|', 'XOR': '^'}

file = ['6\tCARRY\tOR\t3\t4\t5', '1\tXOR1\tXOR\tA\tB', '3\tAND2\tAND\tA\tC', '4\tAND1\tAND\tA\tB', '5\tAND3\tAND\tB\tC', '2\tSUM\tXOR\t1\tC']

# Load file lines into array.
args = [None]*len(file)
for y in range(0, len(file)):
    args[y] = file[y].split();

# Organize file lines by gate index.
nodes = [None]*len(file)
result = [None]*len(file)
for z in range(0, len(args)):
    nodes[int(''.join(args[z][0]))-1] = args[z];

# Print nodes array to check organization.
for z in range(0, len(nodes)):
    print (nodes[z])


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

# Function definition is here
#def AND( a, b ):
#   # Add both the parameters and return them."
#   c = int(a == b == 1);
#   return c;

file = ['6\tcarry\tOR\t3\t4\t5', '1\txor1\tXOR\tA\tB', '3\tand2\tAND\tA\tC', '4\tAND1\tAND\tA\tB', '5\tAND3\tAND\tB\tC', '2\tSUM\tXOR\t1\tC']

print('one\n');
args = [None]*len(file);
for y in range(0, len(file)):
    args[y] = file[y].split();

print('two\n')
for z in range(0, len(args)):
    print (args[z])

# to get the parameters




print('\n');

def analyze(method, *args):
    result = args[0];
    for a in range(1, len(args)):
        result = {
            'AND': (args[a] & result),
            'NAND': (args[a] & result),
            'OR': (args[a] | result),
            'XOR': (args[a] ^ result),
            #'NAND': (not(args[a]) | (result==0)),
            'XNOR': (args[a] ^ (result==0))
        }[method]
        if (method == 'NAND'):
            result = result
    return result

# For NAND, since result is affected by feedback: ((AB)'C)' => ((A'+B')+C').
# DeMorgan's is used to accomodate this.


# Now you can call sum function
args = { 0, 0, 0, 0 }
a = b = c = d = 0
print ('A   B   C \t F\n----------------')
for a in range(0,2):
 for b in range(0,2):
  for c in range(0,2):
      #for d in range(0,2):
   print ('%d   %d   %d\t %d' % (a, b, c,  eval('c ^ (b ^ a)')))

#print (map(int,list(bin(8))[-4:]))
print ('\n')
a = b = c = 1
sum = eval('c ^ (b ^ a)')
print (sum)

#gates[1][XOR][A][B]
#gates[2][XOR][z][C]

#for x in range(0, len(gates)):

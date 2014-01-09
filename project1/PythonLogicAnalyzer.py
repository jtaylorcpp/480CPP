#baseline commit for the logic analyzer project
#please comment on all additions and chnages to code before commit
#if there is a bug foundplease comment on the bug and commit with the bug issue in the notes
#	then recommit before fixing

#algorithm for reading type of logic and creating login equation

file = ["1 and1 AND a b c","2 and2 AND a 1"]

print(file)

def create_logic_function (logic, *inputs):
    string = str(input[0])
    return {
    "AND":
        for x in range (1,len(inputs)):
            string = string + "&" +  str(inputs[x])
        ,
    }[logic]
            

## Usage: python day14.py input iterations


import sys
import re

NUMBER = (int)(sys.argv[1])

# debug
def dump(elf1,elf2,recipes):
    idx = 0
    for r in recipes:
        if idx == elf1:
            sys.stdout.write("({0:d})".format(r))
        elif idx == elf2:
            sys.stdout.write("[{0:d}]".format(r))
        else:
            sys.stdout.write(" {0:d} ".format(r))
        idx+=1
    print ""
    

elf1 = 0
elf2 = 1
recipes = [3,7]

while len(recipes) < NUMBER+10:
    elf1Val = recipes[elf1]
    elf2Val = recipes[elf2]
    
    # add recipes
    total = elf1Val+elf2Val
    if total < 10:
        recipes.append(total)
    else:
        recipes.append(1)
        recipes.append(total-10)
    
    # step elfs
    elf1 = (elf1+elf1Val+1)%len(recipes)
    elf2 = (elf2+elf2Val+1)%len(recipes)

    # print
    #dump(elf1,elf2,recipes)

solution = ""
for c in range(10):
    solution += str(recipes[c+NUMBER])

print "Solution is %s" % solution


# part 2

elf1 = 0
elf2 = 1
recipes = [3,7]

NUMBER = str(NUMBER)
while True:
    elf1Val = recipes[elf1]
    elf2Val = recipes[elf2]
    
    # add recipes
    total = elf1Val+elf2Val
    if total < 10:
        recipes.append(total)
    else:
        recipes.append(1)
        recipes.append(total-10)
    
    # step elfs
    elf1 = (elf1+elf1Val+1)%len(recipes)
    elf2 = (elf2+elf2Val+1)%len(recipes)

    lastDigits = recipes[(len(recipes)-len(NUMBER)-2):]
    asString = "".join(str(r) for r in lastDigits)
    found = asString.find(NUMBER)
    #print "Evaluating %s" % asString
    if found > 0:
        result = len(recipes)-len(NUMBER)-2+found
        #dump(elf1,elf2,recipes)
        print "Solution is %s recipes" % (result)
        exit(0)
    

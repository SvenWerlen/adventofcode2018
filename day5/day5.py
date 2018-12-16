## Usage: python day5.py input

import sys
import string

FILE = sys.argv[1]

content = None
with open(FILE) as f:

    for line in f:
        
        input = line[:-1]
        break
    
print input


## function that computes the polymer reaction (count)
def getPolymer(input):
    content = list(input)
    changed = True
    while changed:
        changed = False
        idx = 0
        while idx < len(content)-1:
            char1 = content[idx]
            char2 = content[idx+1]
            
            if char1 != char2 and char1.upper() == char2.upper():
                content.pop(idx+1)
                content.pop(idx)
                changed = True
            else:
                idx+=1

    return len(''.join(content))


print "Answer is: %s" % getPolymer(input)



## Part 2

## function that removes
def removeUnits(input,char):
    content = list(input)
    idx = 0
    while idx < len(content):
        c = content[idx]
        
        if c.upper() == char.upper():
            content.pop(idx)
        else:
            idx+=1
                
    return ''.join(content)


bestChar = None
bestLen = 0
for c in string.ascii_lowercase:
    inputNew = removeUnits(input,c)
    inputRes = getPolymer(inputNew)
    print "Polymer for '%s' is: %s" % (c,inputRes)
    
    if not bestChar or inputRes < bestLen:
        bestChar = c
        bestLen = inputRes
        
print "Answer is: %s for char %s" % (bestLen, bestChar)






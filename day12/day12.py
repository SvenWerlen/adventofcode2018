## Usage: python day12.py input iterations


import sys
import re

FILE = sys.argv[1]
ITERATIONS = int(sys.argv[2])

index = 0
state = None
notes = []

with open(FILE) as f:

    for line in f:
        
        m = re.search('(.....) => (.)', line[:-1])
        if line.startswith("initial state: "):
            state=line[15:-1]
        
        elif m:
            #print "%s => %s" % (m.group(1),m.group(2))
            notes.append({'pattern':m.group(1), 'result':m.group(2)})


def applyState(state,notes):
    #print "State: %s" % state
    for n in notes:
        found = True
        if state == n['pattern']:
            #print "Match for %s => %s" % (state,n['result'])
            return n['result']
        
    # no match => return initial state
    return '.'
    

index = 0
#print "%4s: %s" % (0,state)
loop = 1

prevIndex = None
prevPattern = None
while loop <= ITERATIONS:
    
    # remove useless chars
    charBeg = state.find('#')
    charEnd = state.rfind('#')
    curPattern = state[charBeg:charEnd+1]
    state = '....' + curPattern + '....'
    index = index + charBeg - 4
    if prevPattern == None:
        prevPattern = curPattern
        prevIndex = index
    elif prevPattern == curPattern:
        print "Pattern scheme found at iteration %s (%s)" % (loop,index-prevIndex)
        index+=(ITERATIONS - loop + 1)*(index-prevIndex)
        break
    else:
        prevPattern = curPattern
        prevIndex = index
    
    stateList = list(state)
    for idx in range(len(state)-4):
        pos = idx+2
        stateList[idx+2]=applyState(state[idx:idx+5],notes)
    state = "".join(stateList)
    
    # debug
    #print "%4s: %s" % (loop,state)
    
    loop+=1

# compute answer
total = 0
for p in state:
    if p == '#':
        total += index
    index+=1

print "Answer is : %s" % total

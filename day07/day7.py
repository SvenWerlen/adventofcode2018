## Usage: python day7.py input 5 60

import sys
import re


FILE = sys.argv[1]
WORKERS = int(sys.argv[2])
EFFORT = int(sys.argv[3])

print "%s workers, base effort = %s second(s)" % (WORKERS, EFFORT)

## Structure
## Dict with dependencies
flow = {}
with open(FILE) as f:

    for line in f:
        instruction = line[:-1]
        m = re.search('Step (.+?) must be finished before step (.+?) can begin.', instruction)
        if m:
            cond1 = m.group(1)
            cond2 = m.group(2)
            
            if cond2 in flow:
                flow[cond2].append(cond1)
            else:
                flow[cond2] = [cond1]
                
            if not cond1 in flow:
                flow[cond1] = []
            
        else:
            print "Error while reading %s" % instruction
            exit(1)

#print flow

def updatedDeps(depList, depRemoved):
    newDeps = []
    for el in depList:
        if el != depRemoved:
            newDeps.append(el)
        
    return newDeps




sequence = []
while len(flow)>0:
    #print flow
    # find element without dependencies
    noDep = []
    for el in flow:
        if len(flow[el]) == 0:
            noDep.append(el)
    
    if not noDep:
        print "No element without dependency could be found!"
        exit(1)
    
    noDep.sort()
    
    # remove element from dict
    nextElement = noDep[0]
    del(flow[nextElement])
    sequence.append(nextElement)
        
    # update dependencies
    for el in flow:
        if nextElement in flow[el]:
            flow[el].remove(nextElement)
    
print "Answer is: %s" % (''.join(sequence))    
    


# PART 2

with open(FILE) as f:

    for line in f:
        instruction = line[:-1]
        m = re.search('Step (.+?) must be finished before step (.+?) can begin.', instruction)
        if m:
            cond1 = m.group(1)
            cond2 = m.group(2)
            
            if cond2 in flow:
                flow[cond2].append(cond1)
            else:
                flow[cond2] = [cond1]
                
            if not cond1 in flow:
                flow[cond1] = []
            
        else:
            print "Error while reading %s" % instruction
            exit(1)
            
time = 0
sequence = []
workers = [{'el': None, 'finished': -1} for w in range(WORKERS)]
while len(flow)>0:

    #print "Time is now %s" % time

    # find element without dependencies
    noDep = []
    for el in flow:
        if len(flow[el]) == 0:
            # check that it's not already worked
            hasWorker = False
            for w in workers:
                if w['el'] == el:
                    hasWorker = True
            if not hasWorker:
                noDep.append(el)
        
    noDep.sort()
    
    #load workers as much as possible
    for w in workers:
        if not w['el'] and len(noDep) > 0:
            # remove element from dict
            nextElement = noDep.pop(0)
            # assign to worker
            w['el'] = nextElement
            w['finished'] = time + EFFORT + ord(nextElement.lower()) - 96
            #print w
        
    #find next available time
    nextTime = None
    nextWorker = None
    for w in workers:
        if w['el']:
            if not nextWorker or w['finished'] < nextTime:
                nextWorker = w
                nextTime = w['finished']
    
    if not nextWorker:
        print "Not able to find next worker! Problem!!"
        exit(1)
    
    #worked finished
    nextElement = nextWorker['el']
    time = nextTime
    #reset worker
    nextWorker['el'] = None
    nextWorker['finished'] = -1
        
    del(flow[nextElement])
    sequence.append(nextElement)
            
    # update dependencies
    for el in flow:
        if nextElement in flow[el]:
            flow[el].remove(nextElement)
    
print "Answer is: %s (%s)" % (time,''.join(sequence))    

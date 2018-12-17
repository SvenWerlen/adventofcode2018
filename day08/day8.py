## Usage: python day8.py input

import sys
import re


FILE = sys.argv[1]

## Structure
tree = None
with open(FILE) as f:
    for line in f:
        tree = line[:-1]
        break

# convert to int list
tree = tree.split(' ')
for idx in range(len(tree)):
    tree[idx]=int(tree[idx])
    

def computeTree(tree, fromIdx):
    
    if fromIdx >= len(tree):
        print "Idx too big %s/%s" % (fromIdx,len(tree))
        exit(1)
        
    children = tree[fromIdx]
    metadata = tree[fromIdx+1]
    
    print "Computing from %s [%s,%s]" % (fromIdx,children,metadata)
    
    if children == 0:
        # compute metadata
        total = 0
        for c in range(metadata):
            total += tree[fromIdx+c+2]
        return {'total': total, 'totalIndexed': total, 'nextFrom': fromIdx+2+metadata}
    
    total = 0
    curFrom = fromIdx+2
    valueChild = [0 for c in range(children)]
    for idx in range(children):
        result = computeTree(tree, curFrom)
        total += result['total']
        curFrom = result['nextFrom']
        valueChild[idx] = result['totalIndexed']
        
    totalIndexed = 0
    for c in range(metadata):
        total += tree[curFrom+c]
        if tree[curFrom+c]-1 < len(valueChild):
            totalIndexed += valueChild[tree[curFrom+c]-1]
    
    return {'total': total, 'totalIndexed': totalIndexed, 'nextFrom': curFrom+metadata}
    

results = computeTree(tree, 0)

print "Result = %s" % results['total']
print "Result (indexed) = %s" % results['totalIndexed']

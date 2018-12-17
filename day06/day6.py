## Usage: python day6.py input 10000

import sys


FILE = sys.argv[1]
DIST = int(sys.argv[2])

coord = []
with open(FILE) as f:

    index = 1
    for line in f:
        x = line.split(',')[0].strip()
        y = line.split(',')[1].strip()
        coord.append({'x':int(x), 'y':int(y), 'idx':index})
        index+=1
    
# find min,max coordinates
minX = None
maxX = None
minY = None
maxY = None
for c in coord:
    if not minX or c['x'] < minX:
        minX = c['x']
    if not maxX or c['x'] > maxX:
        maxX = c['x']
    if not minY or c['y'] < minY:
        minY = c['y']
    if not maxY or c['y'] > maxY:
        maxY = c['y']

print "%s < x < %s" % (minX,maxX)
print "%s < y < %s" % (minY,maxY)


def getShortest(x,y,coordList):
    minDist = None
    minEl = None
    for c in coordList:
        dist = abs(c['x']-x)+abs(c['y']-y)
        if minDist is None or dist < minDist:
            minEl = c['idx']
            minDist = dist
        elif minDist and minDist == dist:
            minEl = 0
    return minEl

# compute grid 
grid = [[0 for y in range(maxY-minY+1)] for x in range(maxX-minX+1)] 
coordTot = [0 for c in range(len(coord))]
for yIter in range(maxY-minY+1):
    for xIter in range(maxX-minX+1):
        x = minX + xIter
        y = minY + yIter
        idx = getShortest(x,y,coord)
        grid[xIter][yIter]=idx
        
        # exclue all coordines on the border (=> infinite)
        if x == minX or x == maxX or y == minY or y == maxY:
            coordTot[idx-1] = -1
        else:
            if coordTot[idx-1] >= 0:
                coordTot[idx-1]+=1
        
        #sys.stdout.write("{0:02d} ".format(idx))
    #sys.stdout.write('\n')

idx = 1
maxVal = 0
maxEl = None
for c in coordTot:
    val = c if c >= 0 else '-'
    if not maxEl or maxVal < c:
        maxEl = idx
        maxVal = c
    
    print "Count for %s: %s" % (idx,val)
    idx+=1
    
print "Result is %s for element %s" % (maxVal,maxEl)


def getTotal(x,y,coordList):
    total = 0
    for c in coordList:
        total += abs(c['x']-x)+abs(c['y']-y)
        
    return total

# part 2
grid = [[' ' for y in range(maxY-minY+1)] for x in range(maxX-minX+1)] 
count = 0
for yIter in range(maxY-minY+1):
    for xIter in range(maxX-minX+1):
        x = minX + xIter
        y = minY + yIter
        total = getTotal(x,y,coord)
        #print "Total for (%s,%s) is %s" % (x,y,total)
        if total < DIST:
            count+=1
            grid[xIter][yIter]='x'
        
        #sys.stdout.write(grid[xIter][yIter])
    #sys.stdout.write('\n')

print "Result is %s" % (count)

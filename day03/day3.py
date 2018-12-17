## Usage: python day3.py input 1000

import sys
from sets import Set

FILE = sys.argv[1]
SIZE = int(sys.argv[2])

# Get square inches (part1)

# prepare grid
grid = [[0 for x in range(SIZE)] for y in range(SIZE)] 
for x in range(SIZE):
    for y in range(SIZE):
        grid[x][y]=0

with open(FILE) as f:
    for line in f:
        var1 = line[:-1].split('@')
        var2 = var1[1].split(':')
        
        claimID = var1[0].strip()
        margins = var2[0].strip()
        sizes = var2[1].strip()
        
        #print "%s %s %s" % (claimID, margins, sizes)
        
        marginX = int(margins.split(',')[0])
        marginY = int(margins.split(',')[1])
        sizeX = int(sizes.split('x')[0])
        sizeY = int(sizes.split('x')[1])
        
        #print "%s %sx%s %sx%s" % (claimID, marginX, marginY, sizeX, sizeY)
        
        for x in range(sizeX):
            for y in range(sizeY):
                grid[marginX+x][marginY+y]+=1
        
count = 0
for x in range(SIZE):
    for y in range(SIZE):
        #sys.stdout.write(str(grid[x][y]))
        #sys.stdout.write('\n')
        if grid[x][y] > 1:
            count+=1
        
print "Square inches = %s" % count
        
# Get unique claimID (part2)
# How to do it: check claim for which only 1s are in grid

with open(FILE) as f:
    for line in f:
        var1 = line[:-1].split('@')
        var2 = var1[1].split(':')
        
        claimID = var1[0].strip()
        margins = var2[0].strip()
        sizes = var2[1].strip()
        
        #print "%s %s %s" % (claimID, margins, sizes)
        
        marginX = int(margins.split(',')[0])
        marginY = int(margins.split(',')[1])
        sizeX = int(sizes.split('x')[0])
        sizeY = int(sizes.split('x')[1])
        
        found = True
        for x in range(sizeX):
            for y in range(sizeY):
                if grid[marginX+x][marginY+y] != 1:
                    found = False
                    break
            if not found:
                break
        
        if found:
            print "claimId is %s" % claimID
            exit(0)
        


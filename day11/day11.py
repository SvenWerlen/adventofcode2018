## Usage: python day11.py <grid-serial-number>
## Examples:
##    python day11.py 18 => 29
##    python day11.py 42 => 30


import sys
import re

GRIDNR = int(sys.argv[1])
SIZE = 300
SQUARE = 3

def getPowerLevel(x,y,serial):
    rackID = x+10
    power = rackID*y
    power = power+serial
    power = power*rackID
    digit = int(str(power)[-3])-5
    return digit

#print "Result = %s" % getPowerLevel(3,5,8)
#print "Result = %s" % getPowerLevel(122,79,57)
#print "Result = %s" % getPowerLevel(217,196,39)
#print "Result = %s" % getPowerLevel(101,153,71)

# compute grid
grid = [[0 for y in range(SIZE)] for x in range(SIZE)]
for y in range(SIZE):
    for x in range(SIZE):
        grid[x][y]=getPowerLevel(x+1,y+1,GRIDNR)

total = [[0 for y in range(SIZE-2)] for x in range(SIZE-2)]
maxX = None
maxY = None
maxTotal = None
for y in range(SIZE-2):
    for x in range(SIZE-2):
        total[x][y]=0
        for iY in range(SQUARE):
            for iX in range(SQUARE):
                total[x][y]+=grid[x+iX][y+iY]
        
        if maxTotal == None or total[x][y] > maxTotal:
            maxTotal = total[x][y]
            maxX = x
            maxY = y

print "Result is %s for square(%s,%s)" % (maxTotal, maxX+1, maxY+1)
for iY in range(SQUARE):
    for iX in range(SQUARE):
        sys.stdout.write("{0:4d} ".format(grid[maxX+iX][maxY+iY]))
    sys.stdout.write('\n')
    
#print ""
#for y in range(SIZE):
#    for x in range(SIZE):
#        sys.stdout.write("{0:4d} ".format(grid[x][y]))
#    sys.stdout.write('\n')

# part #2


### TOOO LONG!!!! (takes about 5 minutes)

total = [[0 for y in range(SIZE)] for x in range(SIZE)]
maxX = None
maxY = None
maxS = None
maxTotal = None
for y in range(SIZE):
    for x in range(SIZE):
        bestSize = None
        bestTotal = None
        tot=0
        for s in range(SIZE-max(x,y)-1):
            size = s+1
            # add 1 column and 1 line to total
            for iX in range(size-1):
                tot+=grid[x+iX][y+size-1]
            for iY in range(size):
                tot+=grid[x+size-1][y+iY]
            
            #print "Total for (%s,%s,%s) is %s" % (x,y,size,tot)
            if bestTotal == None or tot > bestTotal:
                bestTotal = tot
                bestSize = size
        
        total[x][y] = bestTotal
        
        if maxTotal == None or total[x][y] > maxTotal:
            maxTotal = total[x][y]
            maxX = x
            maxY = y
            maxS = bestSize
            
        if x % 10 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
    sys.stdout.write('\n')


print "Result is %s for square(%s,%s,%s)" % (maxTotal, maxX+1, maxY+1, maxS)

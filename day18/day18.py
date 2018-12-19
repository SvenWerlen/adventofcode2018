## Usage: python day18.py input <file> <days>


import sys
import re

FILE = sys.argv[1]
MINUTES = int(sys.argv[2])

grid = []

def dumpGrid(grid):
    for g in grid:
        print "".join(g)

# readfile
with open(FILE) as f:
    
    for line in f:        
        grid.append(list(line[:-1]))

# returns statistics
def adjacent(grid,posX,posY):
    open = 0
    trees = 0
    lumberyard = 0
    for dy in range(-1,2):
        y = posY+dy
        if y < 0 or y >= len(grid):
            continue
        for dx in range(-1,2):
            x = posX+dx
            if x < 0 or x >= len(grid[y]) or (x == posX and y == posY):
                continue
            if grid[y][x] == '.':
                open+=1
            elif grid[y][x] == '|':
                trees+=1
            elif grid[y][x] == '#':
                lumberyard+=1
            else:
                print "Invalid character!!"
                exit(1)
    return {'open': open, 'trees': trees, 'lumberyard': lumberyard }
            

def tick(grid):
    # copy grid
    newGrid = grid[:]
    for i in range(len(grid)):
        newGrid[i] = grid[i][:]
    
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            stat = adjacent(grid,x,y)
            if grid[y][x] == '.' and stat['trees'] >= 3:
                newGrid[y][x] = '|'
            elif grid[y][x] == '|' and stat['lumberyard'] >= 3:
                newGrid[y][x] = '#'
            elif grid[y][x] == '#' and (stat['lumberyard'] == 0 or stat['trees'] == 0):
                newGrid[y][x] = '.'
    return newGrid


def getPattern(grid):
    oneline = ""
    for g in grid:
        oneline += "".join(g)
    return oneline


def findPattern(patterns, pattern):
    index = 0
    for p in patterns:
        if pattern == p:
            return index
        index+=1
    return -1
    

#print "Initial state:"
#dumpGrid(grid)
#raw_input("")

patterns = []
same = []

minutes = 0
while minutes < MINUTES:
    grid = tick(grid)
    pattern = getPattern(grid)
    found = findPattern(patterns,pattern)
    if found >= 0:
        for s in same:
            if s['idx'] == found:
                repeat = minutes-s['min']
                print "Pattern was found in minutes %s and %s (repeats every %s minutes)" % (s['min'],minutes,repeat)
                # jump to last round
                remaining = (MINUTES - minutes) % repeat
                minutes = MINUTES - remaining
                patterns = []
                same = []
        same.append({'idx':found,'min':minutes})
    else:
        patterns.append(pattern)
    
    if False:
        dumpGrid(grid)
        raw_input("")
        
    minutes+=1

trees = 0
lumberyards = 0
for g in grid:
    for c in g:
        if c == '|':
            trees+=1
        elif c == '#':
            lumberyards+=1

print "Result is %s x %s = %s" % (trees, lumberyards, (trees*lumberyards))
    

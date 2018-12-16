## Usage: python day13.py input 


import sys
import re
import time

FILE = sys.argv[1]
FOLLOW = 5
INITIAL_HP = 200
ATTACK_POWER = 3

grid = []
with open(FILE) as f:

    for line in f:
        if len(line)>1:
            grid.append(list(line[:-1]))


def dumpGridPath(grid):
    print ""
    for line in grid:
        for i in range(len(line)):
            if line[i].isdigit():
                line[i]='.'
    for g in grid:
        print "".join(g)
        
def dumpGrid(grid, units):
    y = 0
    for g in grid:
        unitsString = "   "
        for u in units:
            if u['y']==y and u['HP']>0:
                unitsString += " " + u['type'] + str(u['#']) + "(" + str(u['HP']) + ")"
        y+=1
        print "".join(g) + unitsString

def dumpUnits(units):
    for u in units:
        if u['type']=='G':
            print "Gobelin #%s at (%s,%s) with %s LP" % (u['#'],u['x'],u['y'],u['HP'])
        else:
            print "Elf     #%s at (%s,%s) with %s LP" % (u['#'],u['x'],u['y'],u['HP'])


def cmp_units(u1, u2):
    if u1['y'] > u2['y']:
        return 1
    elif u1['y'] < u2['y']:
        return -1
    elif u1['x'] > u2['x']:
        return 1
    elif u1['x'] < u2['x']:
        return -1
    else:
        return 0

def abs_dist(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

def compute_dist(grid,u,x,y):
    # cell is adjacent to unit
    if abs_dist(x,y,u['x'],u['y']) == 1:
        return 1
    # find if adjacent to another path
    char = grid[y-1][x]
    if char.isdigit():
        return (int(char))+1
    char = grid[y][x-1]
    if char.isdigit():
        return (int(char))+1
    char = grid[y][x+1]
    if char.isdigit():
        return (int(char))+1
    char = grid[y+1][x]
    if char.isdigit():
        return (int(char))+1
    return 0

def next_path(grid,dist,xTo,yTo,xFrom,yFrom):
    if dist < 0:
        print "Error finding next step!!"
        exit(1)
    
    #dumpGrid(grid)
    #print "next_path (%s,%s) from (%s,%s) with dist %s" % (xTo,yTo,xFrom,yFrom,dist)
    
    # check if next to target destination (To)
    if abs_dist(xTo,yTo,xFrom,yFrom) == 1:
        return {'x':xTo,'y':yTo}
    # recursively find nearest with dist
    char = grid[yTo-1][xTo]
    if char.isdigit() and int(char)==dist:
        grid[yTo-1][xTo]='o'
        return next_path(grid,dist-1,xTo,yTo-1,xFrom,yFrom)
    char = grid[yTo][xTo-1]
    if char.isdigit() and int(char)==dist:
        grid[yTo][xTo-1]='o'
        return next_path(grid,dist-1,xTo-1,yTo,xFrom,yFrom)
    char = grid[yTo][xTo+1]
    if char.isdigit() and int(char)==dist:
        grid[yTo][xTo+1]='o'
        return next_path(grid,dist-1,xTo+1,yTo,xFrom,yFrom)
    char = grid[yTo+1][xTo]
    if char.isdigit() and int(char)==dist:
        grid[yTo+1][xTo]='o'
        return next_path(grid,dist-1,xTo,yTo+1,xFrom,yFrom)
    print "Couldn't find next step!!"
    exit(1)

def find_shortest_path(grid,u):
    # check that unit is not dead
    if u['HP']<=0:
        print "Error trying to find shortest path for dead unit!!"
        exit(1)
    # create a copy (to not alterate it)
    grid = grid[:]
    for idx in range(len(grid)):
        grid[idx]=grid[idx][:]
    # compute path
    curDist = 1
    hasChanged = True
    while(hasChanged):
        hasChanged = False
        for y in range(len(grid)):
            line = grid[y]
            for x in range(len(line)):
                if grid[y][x] in ('E','G') and grid[y][x] != u['type']:
                    dist = compute_dist(grid,u,x,y)
                    if dist == curDist:
                        # check paths (in order)
                        nextPath = next_path(grid,dist-1,x,y,u['x'],u['y'])
                        # find path recursively
                        #if u['#']==FOLLOW and u['type']=='E':
                        #    dumpGridPath(grid)
                        return nextPath
                        
                if grid[y][x] == '.':
                    dist = compute_dist(grid,u,x,y)
                    if dist == curDist:
                        grid[y][x]=str(dist)
                        hasChanged = True
        curDist+=1
    
    return None
        

def get_ennemy_in_range(units,u):
    # find if adjacent to ennemy (and ennemy alive)
    bestEnnemy = None
    bestHP = None
    for e in units:
        if (abs_dist(e['x'],e['y'],u['x'],u['y']) == 1) and (e['type'] != u['type']) and (e['HP']>0):
            if bestEnnemy == None or bestHP > e['HP']:
                bestEnnemy = e
                bestHP = e['HP']

    return bestEnnemy
    

def tick(grid,units):
    # sort units
    units.sort(cmp_units)
    
    # copy list
    allUnits = units[:]
    for u in allUnits:
        # check if ennemies
        hasEnnemies = False
        for e in units:
            if e['type'] != u['type'] and e['HP'] > 0:
                hasEnnemies = True
        if not hasEnnemies:
            print "No ennemy found for %s" % u
            return True
        # skip dead unit
        if u['HP']<=0:
            continue
        ennemy = get_ennemy_in_range(units,u)
        # find shortest path
        if not ennemy:
            path = find_shortest_path(grid,u)
            # move
            if path:
                #print "Shortest path for unit #%s at (%s,%s) is (%s,%s)" % (u['#'],u['x'],u['y'],path['x'], path['y'])
                # remove unit from last position
                grid[u['y']][u['x']]='.'
                # add unit to next position
                grid[path['y']][path['x']]=u['type']
                # update unit position
                u['x']=path['x']
                u['y']=path['y']
                # check if new ennemy in range
                units.sort(cmp_units)
                ennemy = get_ennemy_in_range(units,u)
                
                noAction=False

        # attack
        if ennemy:
            # update HP
            ennemy['HP']-=u['AP']
            # if ennemy dead remove it from grid
            if ennemy['HP']<=0:
                grid[ennemy['y']][ennemy['x']]='.'
            noAction=False
    
    return False
            

# initiate units
units = []
elfIdx = 0
gobIdx = 0
for y in range(len(grid)):
    line = grid[y]
    for x in range(len(line)):
        char = line[x]
        if char == 'E':
            elfIdx+=1
            units.append({'#':elfIdx,'x':x,'y':y,'type':char,'HP':INITIAL_HP,'AP':ATTACK_POWER})
        elif char == 'G':
            gobIdx+=1
            units.append({'#':gobIdx,'x':x,'y':y,'type':char,'HP':INITIAL_HP,'AP':ATTACK_POWER})
        grid[y]=line

print "Initial state:"
dumpGrid(grid,units)

rounds = 1
finished = False
while not finished:
    finished = tick(grid,units)
    if finished or True:
        #time.sleep(.5)
        print ""
        print "AFTER ROUND #%s" % rounds
        #dumpGrid(grid)
        dumpGrid(grid,units)
        #dumpUnits(units)
    if finished:
        break
    rounds+=1
    

# compute result
totalHP = 0
for u in units:
    if u['HP']>0:
        totalHP+=u['HP']

print "Finished during round %s with total HP %s. Result is then: %s" % (rounds-1,totalHP,(rounds-1)*totalHP)

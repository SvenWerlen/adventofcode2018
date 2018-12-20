## Usage: python day20.py input <file>


import sys
import re

FILE = sys.argv[1]

regex = None

# readfile
with open(FILE) as f:
    
    for line in f:        
        regex = line[:-1]
        break

# check input
if not regex or len(regex) <= 2 or regex[0]!='^' or regex[-1]!='$':
    print "Invalid regex! %s" % regex
    exit(1)

regex = regex[1:-1]


def dumpPaths(paths):
    for idx in range(len(paths)):
        if not isinstance(paths[idx],list):
            print "Invalid structure! %s" % paths[idx]
            exit(1)
        for element in paths[idx]:
            if isinstance(element,list):
                sys.stdout.write('(')
                dumpPaths(element)
                sys.stdout.write(')')
            else:
                sys.stdout.write(element)
        
        if idx+1 < len(paths):
            sys.stdout.write('|')   



def buildPaths(regex):
    idx = 0
    paths = []
    curPath = []
    while idx < len(regex):
        c = regex[idx]
        if c in ('N','S','W','E'):
            curPath.append(c)
        elif c == '|':
            # find other options
            paths.append(curPath)
            curPath = []
        elif c == '(':
            # find matching closing bracket
            level = 0
            substring = None
            for i in range(idx+1,len(regex)):
                #print regex[i]
                if regex[i] == '(':
                    level+=1
                elif regex[i] == ')' and level == 0:
                    substring = regex[idx+1:i]
                    idx = i
                    break
                elif regex[i] == ')':
                    level-=1
                    
            if substring == None:
                print "Something went wrong while finding closing bracket at %s" % idx
                exit(1)
            
            curPath.append(buildPaths(substring))
    
        idx+=1
        
    # add curPath to paths
    paths.append(curPath)
    return paths

# print map
def dumpMap(map):
    for y in map:
        print "".join(str(c) for c in y)

# generates a new map increased by dx,dy
def generateMap(map,dx,dy):
    lenX = len(map[0])+abs(dx)
    lenY = len(map)+abs(dy)
    newMap = []
    # add new y-rows before
    for y in range(dy,0):
        newMap.append(['#' for x in range(lenX)])
    # add existing y-rows
    for y in map:
        xrow = ['#' for x in range(dx,0)]
        for x in y:
            xrow.append(x)
        xrow += ['#' for x in range(0,dx)]
        newMap.append(xrow)
    # add new y-rows after
    for y in range(0,dy):
        newMap.append(['#' for x in range(lenX)])
    return newMap


def buildElement(map, element, x, y):
    #print "Trying to build %s at (%s,%s)" % (element, x, y)
    # check if map must be increased
    dx = 0
    dy = 0
    if x < 0:
        dx = -2
    elif x >= len(map[0]):
        dx = 2
    if y < 0:
        dy = -2
    elif y >= len(map):
        dy = 2
    if dx != 0 or dy != 0:
        map = generateMap(map,dx,dy)
        x+=max(0,-dx)
        y+=max(0,-dy)
    map[y][x]= element
    return {'map':map,'x':x,'y':y}
    


def buildMap(map, paths, curX, curY):
    dx = 0
    dy = 0
    for idx in range(len(paths)):
        for element in paths[idx]:
            
            
            if isinstance(element,list):
                for child in element:
                    #print "Building subelement at (%s,%s): %s" % (curX, curY, child)
                    result = buildMap(map, [child], curX, curY)
                    map = result['map']
                    curX += result['dx']
                    curY += result['dy']
                
            else:
                        
                # build buildMap
                if element == 'N':
                    result = buildElement(map,'.', curX, curY-2)
                    map = result['map']
                    dy -= curY-2-result['y']
                    curX = result['x']
                    curY = result['y']
                    buildElement(map,'-', curX, curY+1)
                elif element == 'S':
                    result = buildElement(map,'.', curX, curY+2)
                    map = result['map']
                    dy -= curY+2-result['y']
                    curX = result['x']
                    curY = result['y']
                    buildElement(map,'-', curX, curY-1)
                elif element == 'W':
                    result = buildElement(map,'.', curX-2, curY)
                    map = result['map']
                    dx -= curX-2-result['x']
                    curX = result['x']
                    curY = result['y']
                    buildElement(map,'|', curX+1, curY)
                elif element == 'E':
                    result = buildElement(map,'.', curX+2, curY)
                    map = result['map']
                    dx -= curX+2-result['x']
                    curX = result['x']
                    curY = result['y']
                    buildElement(map,'|', curX-1, curY)
                
                #dumpMap(map)
                #raw_input("")
            
    return { 'map': map, 'dx': dx, 'dy': dy }
                    

def computeMaxDistance(map):
    # copy map
    map = map[:]
    for y in range(len(map)):
        map[y]=map[y][:]
        
    maxValue = 0
    changed = True
    while changed:
        changed = False
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] in ('.','|','-'):
                    minVal = None
                    if isinstance(map[y-1][x],int) and (minVal == None or map[y-1][x]<minVal):
                        minVal = map[y-1][x]
                    elif isinstance(map[y+1][x],int) and (minVal == None or map[y+1][x]<minVal):
                        minVal = map[y+1][x]
                    elif isinstance(map[y][x-1],int) and (minVal == None or map[y][x-1]<minVal):
                        minVal = map[y][x-1]
                    elif isinstance(map[y][x+1],int) and (minVal == None or map[y][x+1]<minVal):
                        minVal = map[y][x+1]
                    if minVal != None:
                        map[y][x]=minVal+1
                        changed = True
                        if maxValue < minVal+1:
                            maxValue = minVal+1
                    
    return { 'map': map, 'max': (maxValue/2) }


def drawPath(map,mapDist,distance):
    # find coordinates
    curX = None
    curY = None
    for y in range(len(mapDist)):
        for x in range(len(mapDist[y])):
            if mapDist[y][x] == distance:
                curX = x
                curY = y
                distance-=1
                map[curY][curX] = ' '
    
    if curX == None:
        print "Something went wrong"
        exit(1)
    
    while distance > 0:
        
        # up
        if mapDist[curY-1][curX]==distance:
            curY = curY-1
        # down
        elif mapDist[curY+1][curX]==distance:
            curY = curY+1
        # left
        elif mapDist[curY][curX-1]==distance:
            curX = curX-1
        # right
        elif mapDist[curY][curX+1]==distance:
            curX = curX+1
        else:
            print "Something went wrong (next)"
            exit(1)
            
        map[curY][curX] = ' '
        distance-=1


#print regex
paths = buildPaths(regex)
#dumpPaths(paths)

print ""
map = [['#','#','#'],['#',0,'#'],['#','#','#']]
map = buildMap(map,paths,1,1)['map']
#dumpMap(map)
result = computeMaxDistance(map)
drawPath(map,result['map'],result['max']*2)
dumpMap(map)



print "Solution is %s" % result['max']

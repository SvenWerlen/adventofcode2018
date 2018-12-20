## Usage: python day20.py input <file>


import sys
import re

FILE = sys.argv[1]
sys.setrecursionlimit(10000)

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



def generatePaths(paths, queue, points):
    
    curPos = points
    
    for idx in range(len(paths)):
        for element in paths[idx]:
            
            if isinstance(element,list):
                max = None
                for child in element:
                    generatePaths([child], queue, curPos)
            else:
                x, y = curPos
                if element == 'N':
                    newPos = (x,y-1)
                elif element == 'S':
                    newPos = (x,y+1)
                elif element == 'E':
                    newPos = (x+1,y)
                elif element == 'W':
                    newPos = (x-1,y)
            
                if newPos not in queue:
                    queue[newPos]=set()
                    
                queue[newPos].add(curPos)
                queue[curPos].add(newPos)
                curPos = newPos


def shortest(queue, visited, point):
    distance = 0    
    maxDist = 0
    for c in queue[point]:
        if c in visited:
            continue
        
        visited.add(c)
        dist = 1 + shortest(queue, visited, c)
        if dist > maxDist:
            maxDist = dist
    
    return maxDist


def moreThan1000(queue, visited, point, curDist):
    count = 1 if curDist >= 1000 else 0
    
    for c in queue[point]:
        if c in visited:
            continue
        
        visited.add(c)
        count += moreThan1000(queue, visited, c, curDist+1)
    
    return count


#print regex
paths = buildPaths(regex)
#dumpPaths(paths)

queue = {(0,0):set()}
generatePaths(paths,queue, (0,0))

print "Solution (part 1) is %s" % shortest(queue, set(), (0,0))
print "Solution (part 2) is %s" % moreThan1000(queue, set(), (0,0), 0)

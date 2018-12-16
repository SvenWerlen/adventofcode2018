## Usage: python day10.py input.test


import sys
import re

FILE = sys.argv[1]
MAXITER = (int)(sys.argv[2])
MAXZONE = (int)(sys.argv[3])

point = []
with open(FILE) as f:

    for line in f:
        
        m = re.search('position=<(.+?),(.+?)> velocity=<(.+?),(.+?)>', line[:-1])
        
        if m:
            x = int(m.group(1))
            y = int(m.group(2))
            vx = int(m.group(3))
            vy = int(m.group(4))
            point.append({"x": x, "y": y, "vx": vx, "vy": vy})
        else:
            print "Cannot parse: %s" % line[:-1]
            exit(1)



def getZone(point):
    minX = None
    maxX = None
    minY = None
    maxY = None
    for p in point:
        if minX == None or p["x"]<minX:
            minX = p["x"]
        if maxX == None or p["x"]>maxX:
            maxX = p["x"]
        if minY == None or p["y"]<minY:
            minY = p["y"]
        if maxY == None or p["y"]>maxY:
            maxY = p["y"]
    
    return {'minX':minX,'maxX':maxX,'minY':minY,'maxY':maxY}
    
    
iteration = 0
maxDistance = None
while iteration < MAXITER:
    # compute new position
    for p in point:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
    
    
    totalDist = 0
    
    # quick check (zone should be < MAXZONE)
    zone = getZone(point)
    if zone["maxX"]-zone["minX"]>MAXZONE or zone["maxX"]-zone["minX"]>MAXZONE:
        totalDist = None
    else:
    # check if every point is adjacent to another
        idx1 = 0
        for p1 in point:
            # find most adjacent point
            minDist = None
            idx2 = 0
            for p2 in point:
                if (idx1 != idx2):
                    curDist = abs(p1["x"]-p2["x"])+abs(p1["y"]-p2["y"])
                    if minDist == None or curDist < minDist:
                        minDist = curDist
                idx2+=1
            
            totalDist += minDist
            idx1+=1
        
    if maxDistance == None:
        maxDistance = totalDist
    elif totalDist == None or totalDist < maxDistance:
        maxDistance = totalDist
    elif totalDist > maxDistance:
        # FOUND: go backwards 1 step
        # compute new position
        for p in point:
            p["x"] -= p["vx"]
            p["y"] -= p["vy"]
        break
    
    iteration+=1
    if totalDist == None:
        sys.stdout.write('.')
    else:
        print "%s => %s" % (iteration,totalDist)
    
sys.stdout.write('\n')


if iteration < MAXITER:
    print "Message found after %s iterations" % iteration
    # find min, max
    zone = getZone(point)
    print "Zone (%s,%s) to (%s,%s)" % (zone["minX"],zone["minY"],zone["maxX"],zone["maxY"])

    for y in range (zone["maxY"]-zone["minY"]+1):
        for x in range (zone["maxX"]-zone["minX"]+1):
            found = False
            curX = zone["minX"] + x
            curY = zone["minY"] + y
            for p in point:
                if p["x"]==curX and p["y"]==curY:
                    found = True
                    break
            if found:
                sys.stdout.write('#')
            else:
                sys.stdout.write('.')
        sys.stdout.write('\n')
    
else:
    print "Message not found :-("

## Usage: python day14.py input iterations


import sys
import re

FILE = sys.argv[1]
SPRINGX = 500
SPRINGY = 0
scans = []

with open(FILE) as f:
    
    for line in f:        
        m = re.search('(x|y)=(\d+), (x|y)=(\d+)\\.\\.(\d+)', line[:-1])
        if m:
            if m.group(1) == 'x':
                scans.append({ 'xmin': int(m.group(2)), 'xmax': int(m.group(2)), 'ymin': int(m.group(4)), 'ymax': int(m.group(5))})
            else:
                scans.append({ 'xmin': int(m.group(4)), 'xmax': int(m.group(5)), 'ymin': int(m.group(2)), 'ymax': int(m.group(2))})

xmin = None
xmax = None
ymin = 0
yminForTotal = None
ymax = None
for s in scans:
    if xmin == None or s['xmin']<xmin:
        xmin=s['xmin']
    if xmax == None or s['xmax']>xmax:
        xmax=s['xmax']
    if yminForTotal == None or s['ymin']<yminForTotal:
        yminForTotal=s['ymin']
    if ymax == None or s['ymax']>ymax:
        ymax=s['ymax']

# increase x on both sides (to let water flow)
xmin-=1
xmax+=1

#print "(%s,%s) to (%s,%s)" % (xmin,xmax,ymin,ymax)

def dumpFullGrid(grid):
    for lines in grid:
        print "".join(lines)


def dumpGrid(grid,minX,maxX,minY,maxY):
    #print "%s,%s,%s,%s" % (minX,maxX,minY,maxY)
    CTX = 3
    minX = max(0,minX-CTX)
    maxX = min(len(grid[0]),maxX+CTX)
    minY = max(0,minY-CTX)
    maxY = min(len(grid),maxY+CTX)
    for y in range(minY,maxY+1):
        print "".join(grid[y])[minX:maxX+1]

# prepare grid
grid = [['.' for x in range(xmax-xmin+1)] for y in range(ymax-ymin+1)]
for s in scans:
    for xi in range(s['xmax']-s['xmin']+1):
        for yi in range(s['ymax']-s['ymin']+1):
            x = s['xmin']+xi-xmin
            y = s['ymin']+yi-ymin
            grid[y][x]='#'
grid[SPRINGY-ymin][SPRINGX-xmin]='+'

# to check
gridOrigin = grid[:]
for i in range(len(grid)):
    gridOrigin[i] = grid[i][:]
    

# optimized for zone [minX,minY,maxX,maxY]
def tick(grid,minX,maxX,minY,maxY):
    changed=False
    
    newMinX = None
    newMaxX = None
    newMinY = None
    newMaxY = None
    
    for y in range(minY,maxY+1):
        
        for x in range(minX,maxX+1):
            c = grid[y][x]
            
            # rule 1 : drop
            if c == '.' and y > 0 and (grid[y-1][x] in ('+','|')):
                # try to fill
                down = y
                while down < len(grid) and grid[down][x] not in ('#','~','|'):
                    grid[down][x]='|'
                    down+=1
                changed=True
                # update minY/maxY
                if newMinX == None or x <= newMinX:
                    newMinX = max(0,x-1)
                if newMaxX == None or x >= newMaxX:
                    newMaxX = min(len(grid[0])-1,x+1)
                if newMinY == None or down-2 < newMinY:
                    newMinY = max(0,down-2)
                if newMaxY == None or down > newMaxY:
                    newMaxY = min(len(grid)-1,down)
                
            # rule 2 : block
            if c in ('#','~') and grid[y-1][x] == '|' and (grid[y-1][x-1] == '.' or grid[y-1][x+1] == '.' or (grid[y-1][x-1] == '#' and grid[y-1][x+1] == '#')):
                # try to fill the entire line
                leftBlocked = False
                rightBlocked = False
                left  = x-1
                right = x+1
                while left >= 0:
                    if grid[y-1][left] in ('.','|') and grid[y][left] in ('.','|'):
                        break
                    elif grid[y-1][left] == '#':
                        left+=1
                        leftBlocked = True
                        break
                    left-=1
                while right < len(grid[0]):
                    if grid[y-1][right] in ('.','|') and grid[y][right] in ('.','|'):
                        break
                    elif grid[y-1][right] == '#':
                        right-=1
                        rightBlocked = True
                        break
                    right+=1
                char = '~' if (leftBlocked and rightBlocked) else '|'
                for newX in range (left,right+1):
                    grid[y-1][newX]=char
                # update minY/maxY
                if newMinX == None or left <= newMinX:
                    newMinX = max(0,left-1)
                if newMaxX == None or right >= newMaxX:
                    newMaxX = min(len(grid[0])-1,right+1)
                if newMinY == None or y-2 < newMinY:
                    newMinY = max(0,y-2)
                if newMaxY == None or y > newMaxY:
                    newMaxY = min(len(grid)-1,y)
                changed=True
            x+=1
        y+=1
    
    # in case min/max have not changed
    newMinX = newMinX if newMinX != None else minX
    newMaxX = newMaxX if newMaxX != None else maxX
    newMinY = newMinY if newMinY != None else minY
    newMaxY = newMaxY if newMaxY != None else maxY
    
    return { 'changed': changed, 'minX': newMinX, 'maxX': newMaxX, 'minY': newMinY, 'maxY': newMaxY }

iter = 0
fromIter = 99999999
changed = True
data = { 'changed': True, 'minX': SPRINGX-xmin, 'maxX': SPRINGX-xmin, 'minY': 0, 'maxY': SPRINGY-ymin+1 }
while data['changed']:
    data = tick(grid,data['minX'],data['maxX'],data['minY'],data['maxY'])
    iter+=1
    if iter>fromIter:
        #dumpFullGrid(grid)
        #dumpGrid(grid,data['minX'],data['maxX'],data['minY'],data['maxY'])
        raw_input("")

# double check
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x]=='#' and gridOrigin[y][x]!='#':
            print "Something went wrong!!"
            exit(1)

# compute result
total = 0
totalRetained = 0
y=0
for lines in grid:
    # ignore lines until y>=yminForTotal
    if y<yminForTotal:
        y+=1
        continue
    for c in lines:
        if c in ('|','~'):
            total+=1
        if c == '~':
            totalRetained+=1
    y+=1

#dumpFullGrid(grid)

print "Result = %s and %s retained" % (total, totalRetained)
    

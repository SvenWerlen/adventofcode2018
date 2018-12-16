## Usage: python day13.py input 


import sys
import re

FILE = sys.argv[1]

tracks = []
with open(FILE) as f:

    for line in f:
        if len(line)>1:
            tracks.append(list(line[:-1]))


def dumpTracks(tracks, carts):
    # create a copy (to not alterate it)
    tracks = tracks[:]
    for idx in range(len(tracks)):
        tracks[idx]=tracks[idx][:]
    for c in carts:
        tracks[c['y']][c['x']]=c['dir']
    
    for l in tracks:
        print "".join(l)


def cmp_carts(c1, c2):
    if c1['y'] > c2['y']:
        return 1
    elif c1['y'] < c2['y']:
        return -1
    elif c1['x'] > c2['x']:
        return 1
    elif c1['x'] < c2['x']:
        return -1
    else:
        return 0

def tick(tracks,carts):
    carts.sort(cmp_carts)
    for c in carts:
        # move top
        if c['dir'] == '^':
            c['y']=c['y']-1
        # move bottom
        elif c['dir'] == 'v':
            c['y']=c['y']+1
        # move right
        elif c['dir'] == '>':
            c['x']=c['x']+1
        # move left
        elif c['dir'] == '<':
            c['x']=c['x']-1
        # ignore
        elif c['dir'] == 'X':
            continue
        else:
            print "Error!"
            exit(1)

        # change direction if needed
        newPos = tracks[c['y']][c['x']]
        if newPos == '|':
            if c['dir'] != '^' and c['dir'] != 'v':
                print "Invalid | position for (%s)" % c
                exit(1)
        elif newPos == '-':
            if c['dir'] != '<' and c['dir'] != '>':
                print "Invalid - position for (%s)" % c
                exit(1)
        elif newPos == '/':
            if c['dir'] == '^':
                c['dir']='>'
            elif c['dir'] == '>':
                c['dir']='^'
            elif c['dir'] == 'v':
                c['dir']='<'
            elif c['dir'] == '<':
                c['dir']='v'
            else:
                print "Invalid / position for (%s)" % c
                exit(1)
        elif newPos == '\\':
            if c['dir'] == '^':
                c['dir']='<'
            elif c['dir'] == '>':
                c['dir']='v'
            elif c['dir'] == 'v':
                c['dir']='>'
            elif c['dir'] == '<':
                c['dir']='^'
            else:
                print "Invalid \\ position for (%s)" % c
                exit(1)
        elif newPos == '+':
            c['inter']+=1
            # turn left
            if c['inter'] % 3 == 1:
                if c['dir'] == '^':
                    c['dir']='<'
                elif c['dir'] == '>':
                    c['dir']='^'
                elif c['dir'] == 'v':
                    c['dir']='>'
                elif c['dir'] == '<':
                    c['dir']='v'
            # turn right
            if c['inter'] % 3 == 0:
                if c['dir'] == '^':
                    c['dir']='>'
                elif c['dir'] == '>':
                    c['dir']='v'
                elif c['dir'] == 'v':
                    c['dir']='<'
                elif c['dir'] == '<':
                    c['dir']='^'
        else:
            print "Invalid %s position for (%s)" % (newPos,c)
            exit(1)
        
        # check for crash
        for c2 in carts:
            if c['dir']!= 'X' and c2['dir']!= 'X' and c['#'] != c2['#'] and c['x'] == c2['x'] and c['y'] == c2['y']:
                c['dir']='X'
                c2['dir']='X'
                #dumpTracks(tracks,carts)
                print "Crash at (%s,%s)" % (c['x'],c['y'])
        
    # check if only one cart remaining
    count = 0
    remaining = None
    for c in carts:
        if c['dir']=='X':
            count+=1
        else:
            remaining = c
    if count == len(carts)-1:
        print "Remaing cart at (%s,%s)" % (remaining['x'],remaining['y'])
        exit(0)
        

# initiate carts
carts = []
cartsIdx = 0
for y in range(len(tracks)):
    line = tracks[y]
    for x in range(len(line)):
        char = line[x]
        if char == '^' or char == 'v':
            line[x]='|'
            cartsIdx+=1
            carts.append({'#':cartsIdx,'x':x,'y':y,'dir':char,'inter':0})
        elif char == '<' or char == '>':
            line[x]='-'            
            cartsIdx+=1
            carts.append({'#':cartsIdx,'x':x,'y':y,'dir':char,'inter':0})
        tracks[y]=line

while True:
    #dumpTracks(tracks,carts)
    tick(tracks,carts)

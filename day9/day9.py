## Usage: python day9.py <num-players> <last-marble>

# SAMPLES
# python day9.py 9 25
# python day9.py 10 1618
# python day9.py 13 7999
# python day9.py 17 1104
# python day9.py 21 6111
# python day9.py 30 5807
#
# QUIZ
# python day9.py 462 71938
# python day9.py 462 7193800


import sys
import re


PLAYERS = (int)(sys.argv[1])
MARBLES = (int)(sys.argv[2])
SPECIAL = 23

playerScore = [0 for p in range(PLAYERS)]
print "%s players are playing with %s marbles" % (PLAYERS, MARBLES)

marble0 = { 'prev': None, 'next': None, 'value': 0 }
marble0['prev'] = marble0
marble0['next'] = marble0


def dumpForDebug(marble, current):
    
    sys.stdout.write("[{0:03d}] ".format(marble))
    
    nextEl = current['next']
    nextNext = current['next']['next']
    
    # print c-X
    curEl = nextNext['next']
    while curEl['value'] != current['value']:
        sys.stdout.write(str(curEl['value']) + ' ')
        curEl = curEl['next']
    
    # print c+1 and c+2
    sys.stdout.write('(' + str(current['value']) + ') ')
    if nextEl['value'] != current['value']:
        sys.stdout.write(str(nextEl['value']) + ' ')
    if nextNext['value'] != current['value']:
        sys.stdout.write(str(nextNext['value']) + ' ')
    
    sys.stdout.write('\n')


current = marble0
for m in range(MARBLES):
    
    marble = m + 1
    player = m % PLAYERS + 1
    
    # debug (if needed)
    #dumpForDebug(marble, current)

    # special if % 23
    if marble % SPECIAL == 0:
        # remove -7 marble
        toRem = current
        for idx in range(7):
            toRem = toRem['prev']

        toRem['prev']['next'] = toRem['next']
        toRem['next']['prev'] = toRem['prev']
        current = toRem['next']
        # update score
        playerScore[player-1] += toRem['value'] + marble
    else:
        # insert marble into [C+1 and C+2]
        current  = { 'prev': current['next'], 'next': current['next']['next'], 'value': marble }
        current['next']['prev'] = current
        current['prev']['next'] = current

bestScore = 0
bestPlayer = None

for p in range(PLAYERS):
    if not bestPlayer or bestScore < playerScore[p]:
        bestPlayer = p+1
        bestScore = playerScore[p]
        
print "Result is %s for player %s" % (bestScore, bestPlayer)
    

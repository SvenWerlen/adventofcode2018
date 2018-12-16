## Usage: sort input > input.sorted && python day4.py input

import sys
import datetime
import re


FILE = sys.argv[1]

def diff_dates(date1, date2):
    return abs(date2-date1).days

def format_date(date):
    return "{0:02d}-{1:02d}".format(date.month, date.day)


## Assuming entries are already sorted
entries = []
with open(FILE) as f:

    curDate = None
    for line in f:
        
        dateStr = line.split(']')[0][1:]
        date = datetime.datetime.strptime( dateStr, "%Y-%m-%d %H:%M" )
        
        event = line.split(']')[1][1:-1]
        entries.append({'date':date,'event':event})


firstDate = entries[0]['date']
firstDate = firstDate.replace(hour=0, minute=0, second=0)
lastDate = entries[-1]['date']

days = (lastDate-firstDate).days

print "First date: %s" % format_date(firstDate)
print "Last date:  %s" % format_date(lastDate)
print "Total days: %s" % days

# data
grid = [['.' for m in range(60)] for d in range(days+1)] 
guard = [0 for g in range(days+1)]

# iterate on list
curGuardId = 0
asleep = False
asleepFrom = None
for e in entries:
    m = re.search('Guard #(.+?) begins shift', e['event'])
    
    if m:
        curGuardId = int(m.group(1))
    elif e['event'] == "falls asleep":
        asleep = True
        asleepFrom = e['date']
    elif e['event'] == "wakes up" and asleep and asleepFrom and curGuardId > 0:
        # check dates
        if asleepFrom.day != e['date'].day:
            print "Slept > 1 day??? Impossible!"
            exit(1)
        
        # check hours
        if asleepFrom.hour != 0 or e['date'].hour != 0:
            print "Slept not between 00:00 and 01:00??? Impossible!"
            exit(1)
        
        day = (asleepFrom-firstDate).days
        # check guardId
        if guard[day] != 0 and guard[day] != curGuardId:
            print "Two guards on the same day???"
            print "%s (%s), #%s, #%s" % (asleepFrom, day, guard[day], curGuardId)
            exit(1)
            
        # set guard on specified day
        guard[day] = curGuardId
        
        # set minutes the guards was asleep
        minutesFrom = asleepFrom.minute
        minutesTo = e['date'].minute
        for m in range(minutesTo-minutesFrom):
            grid[day][minutesFrom+m]='#'
        
        #print "Slept from %s->%s (%s->%s)" % (minutesFrom, minutesTo, asleepFrom,e['date'])
        
        # update variables
        asleep = False
        asleepFrom = None
    else:
        print "Unsupported usecase: %s %s %s" % (asleep, asleepFrom, e['event'])
        exit(1)


# find guard (sleeping the most)
guardStats={}
for d in range(days+1):
    count = 0
    for m in range(60):
        if grid[d][m] == '#':
            count+=1
            
    if not guard[d] in guardStats:
        guardStats[guard[d]]=count
    else:
        guardStats[guard[d]]+=count

worstGuard = None
sleepTime = 0
for curGuard in guardStats:
    #print "Guard #%s with %s minutes" % (curGuard, guardStats[curGuard])
    if not worstGuard or guardStats[curGuard] > sleepTime:
        worstGuard = curGuard
        sleepTime = guardStats[curGuard]
        
print "Worst guard = #%s with %s minutes" % (worstGuard, sleepTime)



# find best minute
bestMinute = -1
bestCount = 0
for m in range(60):
    count = 0
    for d in range(days+1):
        if grid[d][m] == '#' and guard[d] == worstGuard:
            count+=1
    
    if bestMinute < 0 or count > bestCount:
        bestMinute = m
        bestCount = count

print "Best minute = %s with %s times" % (bestMinute, bestCount)
print "Answer is then %s * %s = %s" % (worstGuard,bestMinute,(worstGuard*bestMinute))



# part #2
worstGuard = None
worstMinute = -1
sleepTime = 0
for m in range(60):
    guardStats = {}
    for d in range(days+1):
        if grid[d][m] == '#':
            curGuard = guard[d]
            if curGuard not in guardStats:
                guardStats[curGuard] = 1
            else:
                guardStats[curGuard] += 1

    # find worst guard
    worstGuardForHour = None
    sleepTimeForHour = 0
    for g in guardStats:
        if not worstGuardForHour or sleepTimeForHour < guardStats[g]:
            worstGuardForHour = g
            sleepTimeForHour = guardStats[g]
    
    #print "Worst guard for minute #%s is %s with %s times" % (m,worstGuardForHour,sleepTimeForHour)
    
    # check if worst hour
    if not worstGuard or sleepTime < sleepTimeForHour:
        worstGuard = worstGuardForHour
        worstMinute = m
        sleepTime = sleepTimeForHour

print "Worst minute is %s for guard %s with %s times" % (worstMinute,worstGuard,sleepTime)
print "Answer is then %s * %s = %s" % (worstMinute,worstGuard,(worstMinute*worstGuard))


# comment if you want to see the table
exit(0)

print "=========================================================================="
print "              000000000011111111112222222222333333333344444444445555555555"
print "              012345678901234567890123456789012345678901234567890123456789"
for d in range(days+1):
    curDate = firstDate + datetime.timedelta(days=d)
    sys.stdout.write(format_date(curDate) + "  ")
    sys.stdout.write("#{0:04d}".format(guard[d]) + "  ")
    for m in range(60):
        sys.stdout.write(grid[d][m])
    sys.stdout.write('\n')

#awake = True
#while curDate < lastDate:
    #print format_date(curDate)
    #curDate = curDate + datetime.timedelta(days=1)

#print "Date range = %s -> %s" % (firstDate,entries[-1]['date'])

#m = re.search('Guard #(.+?) begins shift', text)
#newGuardId = m.group(1) if m else None
#print text
    
        
        
        
 


## Usage python day1.py input

import sys
from sets import Set

FILE = sys.argv[1]

# Get total
count = 0
with open(FILE) as f:
    for line in f:
        num = int(line)
        count += num
print "Resulting frequency = %s" % count




# Get first duplicate
frequencies = Set([0])
count = 0 
current = 0

while True:
    with open(FILE) as f:
        for line in f:
            num = int(line)
            count += num
            
            if count in frequencies:
                print "First duplicate frequency = %s" % count
                exit(0)
            
            frequencies.add(count)

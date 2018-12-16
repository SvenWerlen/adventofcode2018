## Usage python day2.py input

import sys
from sets import Set

FILE = sys.argv[1]

# Get checksum (part1)
count2 = 0
count3 = 0
with open(FILE) as f:
    for line in f:
        chars = {}
        # count each character
        for c in line:
            if c in chars:
                chars[c]+=1
            else:
                chars[c]=1
        # check if exactly 2 or 3
        check2 = False
        check3 = False
        for c in chars:
            if chars[c] == 2:
                check2 = True
            elif chars[c] == 3:
                check3 = True
        # increment 
        count2 = count2 + 1 if check2 else count2
        count3 = count3 + 1 if check3 else count3
        
print "Checksum = %s x %s = %s" % (count2,count3,(count2*count3))


# Get correct boxes (part2)
# UGLY implementation!!!
with open(FILE) as f1:
    for line1 in f1:
        with open(FILE) as f2:
            for line2 in f2:
                # compare the two strings assuming they have the same number of chars
                count = 0
                for idx in range(len(line1)-1):
                    #print "%s vs %s => %s" % (line1[idx],line2[idx],line1[idx]==line2[idx])
                    if line1[idx]!=line2[idx]:
                        count+=1
                
                #print "%s %s = %s" % (line1[:-1],line2[:-1],count)
                
                if count == 1:
                    print "Correct boxes are:"
                    print "%s%s" % (line1,line2)
                    exit(0)
                

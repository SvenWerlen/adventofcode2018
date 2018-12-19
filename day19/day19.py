## Usage: python day14.py input iterations


import sys
import re

FILE = sys.argv[1]

def execute(registers, instr):
    defName = INSTR[instr[0]]
    return defName(registers, instr)

def addr(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]+result[B]
    return result

def addi(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]+B
    return result

def mulr(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]*result[B]
    return result

def muli(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]*B
    return result

def banr(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]&result[B]
    return result

def bani(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]&B
    return result

def borr(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]|result[B]
    return result

def bori(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    result[C]=result[A]|B
    return result
    
def setr(registers, instr):
    result = registers[:]
    A = instr[1]
    C = instr[3]
    result[C]=result[A]
    return result

def seti(registers, instr):
    result = registers[:]
    A = instr[1]
    C = instr[3]
    result[C]=A
    return result

def gtir(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    if A > result[B]:
        result[C]=1
    else:
        result[C]=0
    return result

def gtri(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    if result[A] > B:
        result[C]=1
    else:
        result[C]=0
    return result

def gtrr(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    if result[A] > result[B]:
        result[C]=1
    else:
        result[C]=0
    return result

def eqir(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    if A == result[B]:
        result[C]=1
    else:
        result[C]=0
    return result

def eqri(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    if result[A] == B:
        result[C]=1
    else:
        result[C]=0
    return result

def eqrr(registers, instr):
    result = registers[:]
    A = instr[1]
    B = instr[2]
    C = instr[3]
    if result[A] == result[B]:
        result[C]=1
    else:
        result[C]=0
    return result

def isEqual(reg1, reg2):
    for i in range(4):
        if reg1[i]!=reg2[i]:
            return False
    return True

# find dividors
def getDivisors(n) : 
    results = []
    i = 1
    while i <= n : 
        if (n % i==0) : 
            results.append(i)
        i += 1
    return results


INSTR = {'addr':addr,'addi':addi,'mulr':mulr,'muli':muli,'banr':banr,'bani':bani,'borr':borr,'bori':bori,'setr':setr,'seti':seti,'gtir':gtir,'gtri':gtri,'gtrr':gtrr,'eqir':eqir,'eqri':eqri,'eqrr':eqrr}

ip = None
instructions = []
registers = [0, 0, 0, 0, 0, 0]

with open(FILE) as f:
    
    for line in f:
        
        m = re.search('#ip (\d+)', line[:-1])
        if m:
            if ip == None:
                ip = int(m.group(1))
            else:
                print "Multiple IP instructions not supported yet!!"
            continue
            
        m = re.search('(....) (\d+) (\d+) (\d+)', line[:-1])
        if m:
            instructions.append([m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4))])
        else:
            print "Something went wrong with %s" % line[:-1]
            exit(1)

pointer = registers[ip]
while pointer < len(instructions):
    instr = instructions[pointer]
    registersBefore = registers
    registers = execute(registers,instr)
    #print "ip=%s %s %s %s" % (pointer,registersBefore,instr,registers)
    registers[ip]+=1
    pointer = registers[ip]

print "Value left in register #0 = %s" % registers[0]



## SECOND PART: couldn't find a good way
## I figured out that it was the sum of all divisors of 10551350
## The code below is terrible

registers = [1, 0, 0, 0, 0, 0]
pointer = registers[ip]
idx = 0

# [1, 2, 5, 10, 25, 41, 50, 82, 205, 410, 1025, 2050, 5147, 10294, 25735, 51470, 128675, 211027, 257350, 422054, 1055135, 2110270, 5275675, 10551350]
divisors = getDivisors(10551350)
#total = 0
#for d in divisors:
#    total+=d
#print total


# from my understanding
# when [2]*[4]==[5], [0] gets increased by [2]
# when [4]>[5], then [2] gets increased by 1
# 
# Note: 25 * 422054 = 10551350
# strategy: speed up the process by always setting [4] == [5] when registers look like [*, 9, *, 0, ?, 10551350]
# 
while pointer < len(instructions):
    # speed up
    #if registers[1] == 3 and registers[3] == 0 and registers[5] == 10551350:
    #    registers[2]=25
    #    registers[4]=422054
    if registers[1] == 3 and registers[3] == 0 and registers[5] == 10551350:
        if registers[2] in divisors:
            divisor2 = registers[5]/registers[2]
            if registers[4] < divisor2:
                registers[4] = divisor2
        # find next divisors
        else:
            for d in divisors:
                if d > registers[2]:
                    registers[2] = d-1
                    break
    if registers[0] > 1 and registers[1] == 9 and registers[3] == 0 and registers[5] == 10551350:
        registers[4]=registers[5]+1
    
    instr = instructions[pointer]
    registersBefore = registers
    registers = execute(registers,instr)
    print "ip=%s %s %s %s" % (pointer,registersBefore,instr,registers)
    registers[ip]+=1
    pointer = registers[ip]

    idx +=1
    #if pointer == 3:
    #    print "ip=%s %s %s %s" % (pointer,registersBefore,instr,registers)

print "Value left in register #0 = %s" % registers[0]

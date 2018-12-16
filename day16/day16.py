## Usage: python day14.py input iterations


import sys
import re

FILE = sys.argv[1]


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

samples = []
tests = []
with open(FILE) as f:

    before = None
    instr  = None
    after  = None
    
    for line in f:
        
        m = re.search('Before: \\[(\d+), (\d+), (\d+), (\d+)\\]', line[:-1])
        if m:
            before = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
            continue
        m = re.search('After:  \\[(\d+), (\d+), (\d+), (\d+)\\]', line[:-1])
        if m:
            after = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
            continue
        m = re.search('(\d+) (\d+) (\d+) (\d+)', line[:-1])
        if before and m:
            instr = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
            continue
        elif m:
            tests.append([int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))])
        
        if after:
            samples.append({'before': before, 'instr': instr, 'after': after})
            before = None
            instr  = None
            after  = None

instr = [addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr]

totalMatch3 = 0
for s in samples:
    matches = 0
    for i in instr:
        before = s['before']
        after = i(before,s['instr'])
        ok = isEqual(after,s['after'])
        if ok:
            matches+=1
        
    if matches>=3:
        totalMatch3+=1

print "Number of samples which behave like three or more opcodes = %s" % totalMatch3

# part 2
instrByIdx = [None for i in range(len(instr))]

stop = False
while not stop:
    for s in samples:
        # skip if instruction already known
        instruction = s['instr'][0]
        if instrByIdx[instruction]:
            continue
        
        # try to reduce to 1 match
        matches = 0
        lastInstr = None
        for i in instr:
            # skip instruction that are already known
            if i in instrByIdx:
                continue
            
            before = s['before']
            after = i(before,s['instr'])
            ok = isEqual(after,s['after'])
            if ok:
                lastInstr = i
                matches+=1
        
        # found!
        if matches==1:
            instrByIdx[instruction]=lastInstr
        
    # stop when all instructions are known
    stop = True
    for i in instrByIdx:
        if not i:
            stop = False
            break

# debug
print ""
print "Instructions decoded:"
for i in range(len(instrByIdx)):
    print "#%s: %s" % (i,instrByIdx[i].__name__)
    
registers = [0, 0, 0, 0]
for t in tests:
    instr = t[0]
    registers = instrByIdx[t[0]](registers,t)
    print registers

print registers

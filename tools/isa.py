"""Canonical CPU4 v1 encoding and ALU semantics (architectural flags: Z/N).
Carry is a combinational ALU result, not a CPU status register.
"""
OPCODES = {'NOP':0, 'LOAD':1, 'STORE':2, 'MOV':3, 'LDI':3,
           'ADD':4, 'SUB':5, 'AND':6, 'OR':7, 'XOR':8, 'INC':9,
           'DEC':10, 'JMP':11, 'JZ':12, 'JN':13, 'OUT':14, 'HALT':15}
DECODE = {v:k for k,v in OPCODES.items() if k != 'LDI'}
REG_NAMES = {f'R{i}':i for i in range(4)}
ADDR_OPS = ('LOAD','STORE','JMP','JZ','JN')
RR_OPS = ('MOV','ADD','SUB','AND','OR','XOR')
ONE_REG_OPS = ('INC','DEC','OUT')
FLAG_OPS = ('LDI','ADD','SUB','AND','OR','XOR','INC','DEC')

def alu(op, a, b):
    """Return (result, Z, N, internal carry); SUB carry uses no-borrow."""
    if not 0 <= op <= 7 or not 0 <= a <= 15 or not 0 <= b <= 15:
        raise ValueError('ALU operand/op out of range')
    values = (a+b, a-b, a&b, a|b, a^b, a+1, a-1, b)
    r = values[op] & 15
    c = {0:int(a+b>=16),1:int(a>=b),5:int(a==15),6:int(a>=1)}.get(op,0)
    return r,int(r==0),r>>3,c

def decode(word):
    if not isinstance(word,int) or not 0 <= word <= 511:
        raise ValueError('Instruction must be 9-bit unsigned')
    opc=(word>>4)&15; operand=word&15
    return ('LDI' if opc==3 and word&256 else DECODE[opc]),operand

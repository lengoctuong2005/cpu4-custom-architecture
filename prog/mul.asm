; mul.asm - Multiply Mem[10] * Mem[11] via repeated addition
; Alg: R2 = 0; loop R1 (=Mem[10]) times: R2 += R3 (=Mem[11])
; RAM: Mem[10]=3, Mem[11]=4 -> Mem[12] = 12 = 0xC
LOAD  10      ; R0 = Mem[10] = 3 (loop count)
MOV   R1, R0  ; R1 = 3 (counter)
LOAD  11      ; R0 = Mem[11] = 4 (addend)
MOV   R3, R0  ; R3 = 4
LDI   #0      ; R0 = 0
MOV   R2, R0  ; R2 = 0 (accumulator)
LOOP:
ADD   R2, R3  ; R2 = R2 + 4
DEC   R1      ; R1 = R1 - 1
JZ    DONE    ; if R1 == 0 then done
JMP   LOOP    ; repeat
DONE:
MOV   R0, R2  ; R0 = product = 12
STORE 12      ; Mem[12] = 12
OUT   R0      ; OUT = 12
HALT

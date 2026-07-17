; fib.asm - Fibonacci sequence (4-bit), stop when result > 7
; Output: 1, 1, 2, 3, 5, 8 (next 13 has bit3=1 -> N=1 -> stop)
LDI   #1      ; R0 = 1
MOV   R1, R0  ; R1 = 1 (F_a)
MOV   R2, R0  ; R2 = 1 (F_b)
OUT   R1      ; OUT = 1
OUT   R2      ; OUT = 1
LOOP:
MOV   R3, R1  ; R3 = F_a (temp)
ADD   R1, R2  ; R1 = F_a + F_b (new term)
OUT   R1      ; print new term
MOV   R0, R1  ; R0 = R1
AND   R0, R0  ; N = bit3 of R1 (R1 >= 8?)
JN    END     ; if bit3=1 -> stop
MOV   R2, R3  ; F_b <- old F_a
JMP   LOOP    ; repeat
END:
HALT

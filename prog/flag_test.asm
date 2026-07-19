; Test program to verify flag_write functionality.
; A MOV instruction (which does not write flags) is inserted between DEC and JZ.
; If flag_write is implemented correctly, the Z flag remains 1 and JZ jumps to TARGET.

LDI #5          ; R0 = 5
MOV R1, R0      ; R1 = 5
LDI #1          ; R0 = 1
DEC R0          ; R0 = 0. Sets Z = 1.
MOV R2, R1      ; R2 = R1 = 5. Passes 5 to ALU (zero = 0).
                ; Since flag_write = 0 for MOV, zero_r remains 1.
JZ  TARGET      ; If flag_write is correct, this jumps to TARGET.
LDI #15         ; Fail case: out_port = 15.
OUT R0
HALT
TARGET:
LDI #12         ; Pass case: out_port = 12 (0xC).
OUT R0
HALT

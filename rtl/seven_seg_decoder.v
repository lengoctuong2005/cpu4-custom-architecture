// ============================================================================
// File Name:    seven_seg_decoder.v
// Project:      4-bit Custom CPU Architecture (TKVM / THTKVM)
// Description:  Hexadecimal to 7-segment display decoder (active-low).
//               Segment mapping: seg[6:0] = {g, f, e, d, c, b, a}.
//               Matches standard Altera / Intel Cyclone V DE10 board conventions.
// Standard:     Verilog-2001 (Fully synthesizable)
// ============================================================================

`timescale 1ns / 1ps

module seven_seg_decoder (
    input  wire [3:0] hex_in,   // 4-bit hexadecimal input (0x0 - 0xF)
    output reg  [6:0] seg_out   // 7-segment display output (active-low: 0=ON, 1=OFF)
);

    always @(*) begin
        case (hex_in)
            4'h0: seg_out = 7'b1000000; // '0'
            4'h1: seg_out = 7'b1111001; // '1'
            4'h2: seg_out = 7'b0100100; // '2'
            4'h3: seg_out = 7'b0110000; // '3'
            4'h4: seg_out = 7'b0011001; // '4'
            4'h5: seg_out = 7'b0010010; // '5'
            4'h6: seg_out = 7'b0000010; // '6'
            4'h7: seg_out = 7'b1111000; // '7'
            4'h8: seg_out = 7'b0000000; // '8'
            4'h9: seg_out = 7'b0010000; // '9'
            4'hA: seg_out = 7'b0001000; // 'A'
            4'hB: seg_out = 7'b0000011; // 'b'
            4'hC: seg_out = 7'b1000110; // 'C'
            4'hD: seg_out = 7'b0100001; // 'd'
            4'hE: seg_out = 7'b0000110; // 'E'
            4'hF: seg_out = 7'b0001110; // 'F'
            default: seg_out = 7'b1111111; // Off
        endcase
    end

endmodule

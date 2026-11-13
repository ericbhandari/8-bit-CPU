/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_ericbhandari_8bitCPU (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
  //Memory, 32 registers, 8 bits each
  reg [7:0] mem [31:0];
  reg [7:0] acc;
  reg [4:0] pc;

  wire [2:0] op = mem[pc][7:5]; //Operation select, 3 bits
  wire [4:0] in = mem[pc][4:0]; //Data input, 5 bits

  wire       load  = uio_in[7];
  wire [4:0] lndx  = uio_in[4:0];
  wire [7:0] ldata = ui_in;

  //Opcodes, 8 instructions, 3 bits each
  localparam [2:0]
    ADD = 3'b 000,
    SUB = 3'b 001,
    NOR = 3'b 010,
    LDA = 3'b 011,
    STA = 3'b 100,
    LDI = 3'b 101,
    BEQ = 3'b 110,
    JMP = 3'b 111;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      acc <= 8'd0;
      pc  <= 5'd0;
    end
    else if (load)
      mem[lndx] <= ldata;
    else begin
    pc <= pc + 5'b00001;
    case (op)
      ADD: acc <= acc + mem[in];
      SUB: acc <= acc - mem[in];
      NOR: acc <= ~(acc | mem[in]);
      LDA: acc <= mem[in];
      STA: mem[in] <= acc;
      LDI: acc <= {3'b000 , in};
      BEQ: if (acc == 8'd0) pc <= in;
      JMP: pc <= in;
    endcase
    end
  end


  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = acc;
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in[6:5], 1'b0};

endmodule

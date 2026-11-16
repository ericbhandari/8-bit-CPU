# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

async def store(dut, ndx, data):
    dut.uio_in.value = 0x80 | (ndx & 0x1F)
    dut.ui_in.value = data
    await ClockCycles(dut.clk, 1)


@cocotb.test()
async def store_fibonacci(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
 
    #Fibonacci sequence written in python with the assembly translations
    await store(dut, 0,  0b10100001)   # LDI 1
    await store(dut, 1,  0b10011000)   # STA 24
    await store(dut, 2,  0b10100001)   # LDI 1
    await store(dut, 3,  0b10011001)   # STA 25
    await store(dut, 4,  0b01111000)   # LDA 24
    await store(dut, 5,  0b00011001)   # ADD 25
    await store(dut, 6,  0b10011010)   # STA 26
    await store(dut, 7,  0b01111001)   # LDA 25
    await store(dut, 8,  0b00011010)   # ADD 26
    await store(dut, 9,  0b10011011)   # STA 27
    await store(dut, 10, 0b01111010)   # LDA 26
    await store(dut, 11, 0b00011011)   # ADD 27
    await store(dut, 12, 0b10011100)   # STA 28
    await store(dut, 13, 0b01111011)   # LDA 27
    await store(dut, 14, 0b00011100)   # ADD 28
    await store(dut, 15, 0b10011101)   # STA 29
    await store(dut, 16, 0b01111100)   # LDA 28
    await store(dut, 17, 0b00011101)   # ADD 29
    await store(dut, 18, 0b10011110)   # STA 30
    await store(dut, 19, 0b01111101)   # LDA 29
    await store(dut, 20, 0b00011110)   # ADD 30
    await store(dut, 21, 0b10011111)   # STA 31
    await store(dut, 22, 0b11110110)   # JMP 22

    dut.uio_in.value = 0
    dut.ui_in.value = 0
    
    await ClockCycles(dut.clk, 30)

    #Test case
    assert int(dut.uo_out.value) == 21
#!/bin/bash
# ============================================================================
# Script:        sim/run_sim.sh
# Project:       4-bit Custom CPU Architecture (TKVM / THTKVM)
# Description:   Compiles and executes CPU verification simulation via Icarus Verilog.
# ============================================================================

set -e

# Navigate to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "========================================================"
echo "Compiling 4-bit CPU RTL and Testbench using Icarus Verilog..."
echo "Command: iverilog -g2012 -s tb_cpu_top -o sim/cpu_sim rtl/*.v tb/tb_cpu_top.v"
echo "========================================================"

mkdir -p sim
iverilog -g2012 -s tb_cpu_top -o sim/cpu_sim rtl/*.v tb/tb_cpu_top.v

echo "Compilation successful. Executing simulation binary (vvp sim/cpu_sim)..."
echo "========================================================"
vvp sim/cpu_sim
echo "========================================================"
echo "Simulation finished successfully."

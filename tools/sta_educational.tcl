# OpenSTA one-corner cell-delay-only educational experiment; NOT signoff.
# LIBERTY must match the mapped netlist; units/load reflect the supplied library.
# Run from root with LIBERTY=/path/to/lib.lib sta -exit tools/sta_educational.tcl
foreach name {LIBERTY} {
  if {![info exists env($name)] || ![file exists $env($name)]} {
    error "Missing $name: external Liberty library required"
  }
}
read_liberty $env(LIBERTY)
set netlist build/synthesis/cpu_top_mapped.v
if {[info exists env(NETLIST)]} { set netlist $env(NETLIST) }
read_verilog $netlist
link_design cpu_top
create_clock -name clk -period 10.0 [get_ports clk]
set_clock_uncertainty -setup 0.2 [get_clocks clk]
set_clock_uncertainty -hold 0.05 [get_clocks clk]
set_input_delay -max 1.0 -clock clk [get_ports {clk_en rst_n}]
set_input_delay -min 0.1 -clock clk [get_ports {clk_en rst_n}]
set_input_transition 0.1 [get_ports {clk_en rst_n}]
set_output_delay -max 1.0 -clock clk [all_outputs]
set_output_delay -min 0.1 -clock clk [all_outputs]
# Nangate supplied file uses 1ff capacitance unit: 10 means 10fF, not 10pF.
set_load 10 [all_outputs]
puts "=== NO SPEF; IDEAL CLOCK; SINGLE TT LIBRARY; EDUCATIONAL ONLY ==="
report_units
check_setup -verbose
report_checks -path_delay max -group_path_count 10
report_checks -path_delay min -group_path_count 10
report_worst_slack -max
report_worst_slack -min
report_tns
report_check_types -max_slew -max_capacitance -min_pulse_width -violators

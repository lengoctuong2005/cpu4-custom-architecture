# SAED32 learning template, NOT signoff-certified constraints.
# Time/load units and I/O/reset requirements must match the real library/system.
create_clock -name clk -period 10.0 [get_ports clk]
set_clock_uncertainty -setup 0.2 [get_clocks clk]
set_clock_uncertainty -hold 0.05 [get_clocks clk]
set_clock_transition 0.1 [get_clocks clk]
set data_inputs [remove_from_collection [all_inputs] [get_ports {clk rst_n}]]
set_input_delay -max 2.0 -clock clk $data_inputs
set_input_delay -min 0.2 -clock clk $data_inputs
set_output_delay -max 2.0 -clock clk [all_outputs]
set_output_delay -min 0.2 -clock clk [all_outputs]
set_driving_cell -lib_cell INVX1_RVT $data_inputs
set_load 0.05 [all_outputs]
# Do not false-path the entire async reset net: deassert needs recovery/removal.
# Finish reset constraints with the real reset synchronizer and release protocol.

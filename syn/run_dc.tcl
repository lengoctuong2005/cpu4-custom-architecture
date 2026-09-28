#=========================================================
# run_dc.tcl  —  Tong hop CPU 4-bit (SAED32nm RVT)
# Chay:  cd syn ; dc_shell -f run_dc.tcl | tee dc.log
#=========================================================
set DESIGN cpu4

set_app_var search_path    ". ../rtl ../cons ../Lib/db"
set_app_var target_library "saed32rvt_tt1p05v25c.db"
set_app_var link_library   "* saed32rvt_tt1p05v25c.db"

define_design_lib WORK -path ./work
file mkdir output
file mkdir reports

analyze -format verilog {
    alu_4bit.v
    register_file.v
    program_counter.v
    control_unit.v
    instruction_memory.v
    data_memory.v
    cpu_top.v
}
elaborate $DESIGN
current_design $DESIGN
link
uniquify

source ../cons/${DESIGN}.sdc
check_design > reports/check_design.rpt

compile_ultra

report_timing -max_paths 10      > reports/timing.rpt
report_area                      > reports/area.rpt
report_power                     > reports/power.rpt
report_qor                       > reports/qor.rpt
report_constraint -all_violators > reports/constraint.rpt

change_names -rules verilog -hierarchy
write -format verilog -hierarchy -output output/design_mapped.v
write_sdc output/${DESIGN}.sdc

exit

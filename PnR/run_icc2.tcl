#=========================================================
# run_icc2.tcl  —  Physical Design CPU 4-bit (SAED32nm)
# Chay:  cd PnR ; icc2_shell -f run_icc2.tcl
#=========================================================
set fillers_ref "*/SHFILL128_RVT */SHFILL64_RVT */SHFILL3_RVT */SHFILL2_RVT */SHFILL1_RVT"
set endcap_left "*/SHFILL2_RVT";  set endcap_right "*/SHFILL2_RVT"
set endcap_top    "*/SHFILL3_RVT */SHFILL2_RVT */SHFILL1_RVT"
set endcap_bottom "*/SHFILL3_RVT */SHFILL2_RVT */SHFILL1_RVT"
set tapcell_ref "*/SHFILL3_RVT"

set_app_var search_path "../Lib/ndm"
lappend search_path "../Lib/tech/milkyway"
lappend search_path "../syn/output"
lappend search_path "../cons"
if {[info exists env(SAED32_HOME)]} {
    lappend search_path "$env(SAED32_HOME)/lib/ndm"
    lappend search_path "$env(SAED32_HOME)/tech/milkyway"
}
set_app_var link_library "../Lib/db/saed32rvt_tt1p05v25c.db"
set tech_file "saed32nm_1p9m_mw.tf"
set ref_lib   "saed32_rvt.ndm"

# Pre-check PDK technology assets
set tech_found 0
foreach sp $search_path {
    if {[file exists [file join $sp $tech_file]]} {
        set tech_found 1
        break
    }
}
if {!$tech_found} {
    puts "\[ERROR\] Technology file '$tech_file' not found in search_path: $search_path"
    puts "\[INFO\] Please set SAED32_HOME environment variable or place PDK files under ../Lib."
    exit 1
}

create_lib -technology $tech_file -ref_libs $ref_lib cpu_top.dlib

# --- Import design ---
read_verilog -top cpu_top design_mapped.v
read_sdc ../syn/output/cpu_top.sdc

# --- RC / layer ---
read_parasitic_tech -layermap ../Lib/tech/milkyway/saed32nm_tf_itf_tluplus.map \
    -tlup ../Lib/tech/star_rcxt/saed32nm_1p9m_Cmax.tluplus -name maxTLU
read_parasitic_tech -layermap ../Lib/tech/milkyway/saed32nm_tf_itf_tluplus.map \
    -tlup ../Lib/tech/star_rcxt/saed32nm_1p9m_Cmin.tluplus -name minTLU
set_attribute [get_layers {M1 M3 M5 M7 M9}] routing_direction horizontal
set_attribute [get_layers {M2 M4 M6 M8}]    routing_direction vertical
set_parasitic_parameters -late_spec minTLU -early_spec maxTLU

# --- Floorplan + placement ---
initialize_floorplan -core_utilization 0.6 -core_offset {5}
create_placement -floorplan
legalize_placement
set_block_pin_constraints -self -allowed_layers {M3 M4 M5 M6} -pin_spacing_distance 2
place_pins -self

# --- Power ---
source -echo ./scripts/power.tcl
check_pg_connectivity -check_std_cell_pins none

# --- Placement toi uu ---
place_opt

# --- CTS ---
set_clock_tree_options -target_skew 0.05
set_driving_cell -lib_cell NBUFFX16_RVT [get_ports clk]
set_clock_uncertainty 0.2 -setup [all_clocks]
set_clock_uncertainty 0.05 -hold [all_clocks]
source -echo ./scripts/ndr.tcl
clock_opt

# --- Routing ---
set_app_options -name route.detail.antenna -value true
route_auto
route_opt

# --- Signoff: filler + DRC/LVS ---
set SH_FILLERS "*/SHFILL128_RVT */SHFILL64_RVT */SHFILL3_RVT */SHFILL2_RVT */SHFILL1_RVT"
create_stdcell_fillers -lib_cells $SH_FILLERS
connect_pg_net
remove_stdcell_fillers_with_violation
check_lvs -nets [get_nets] -checks {short open} -check_child_cells true

# --- Luu & xuat ---
save_block
save_lib -all
set design "cpu_top"
write_gds -long_names -design $design -hierarchy design_lib \
    -layer_map ../Lib/tech/milkyway/saed32nm_1p9m_gdsout_mw.map \
    -lib_cell_view frame -keep_data_type -fill exclude output/${design}.gds
write_parasitics -output ./output/cpu_top.spef -no_name_mapping -compress -hierarchical -format spef
write_verilog output/cpu_top_icc2.v -exclude {all_physical_cells pg_objects filler_cells \
    well_tap_cells end_cap_cells physical_only_cells}

exit

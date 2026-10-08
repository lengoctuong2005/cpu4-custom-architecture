# Board inputs KEY/SW are asynchronous and require synchronizer/RDC review.
# One physical clock; no button/divider is used as a clock.
create_clock -name CLOCK_50 -period 20.0 [get_ports CLOCK_50]
derive_clock_uncertainty
# Do NOT globally false-path KEY[0]: verify reset release recovery/removal.
# I/O LED/7-seg timing is board/application-specific; finish in Quartus TimeQuest.

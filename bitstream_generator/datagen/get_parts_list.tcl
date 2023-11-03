#
#  Just pop open Vivado and source this file in the TCL console, or run it in batch mode.
#
#  Output is written to tmp directory. Move it to this directory when it finishes.
#
#  Takes a while to complete this routine..
#
set outfile [open "/tmp/part_map.csv" w+];
puts $outfile "PART,ARCH,FULLARCH,FAMILY,IDCODE,DEVICE";
foreach p [get_parts] {
    set arch [get_property ARCHITECTURE $p];
    set full [get_property ARCHITECTURE_FULL_NAME $p];
    set family [get_property C_FAMILY $p];
    set idcode [get_property IDCODE $p];
    set device [get_property DEVICE $p];
    puts $outfile "${p},${arch},${full},${family},${idcode},${device}";
}

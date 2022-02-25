#!python
import sys
import re
import os
import time

# NOTE: Only works with ***SuperSlicer***

source_file=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(source_file, "r") as f:
    lines = f.readlines() #count lines

# Process file to .gcode file for post-process script 
if (source_file.endswith('.gcode')):
    dest_file = re.sub('\.gcode$','',source_file)
    try:
        os.rename(source_file, dest_file+".sqv.bak")
    except FileExistsError:
        os.remove(dest_file+".sqv.bak")
        os.rename(source_file, dest_file+".sqv.bak")
    dest_file = re.sub('\.gcode$','',source_file)
    dest_file = dest_file + '.gcode'
else:
    dest_file = source_file
    os.remove(source_file)

# Boolean variables
in_infill = False
in_internal_perimeter = False
in_solid_infill = False
in_top_solid_infill = False
in_internal_bridge = False

# NOTE: External perimeters omitted since print quality is my main concern

# Open the destination file and write
with open(dest_file, "w") as of:
    of.write('; Ensure macros are properly setup in klipper\n')
    of.write('_USE_INFILL_SQV\n')
    of.write('_USE_INTERNAL_PERIMETER_SQV\n')
    of.write('_USE_SOLID_INFILL_SQV\n')
    of.write('_USE_TOP_SOLID_INFILL_SQV\n')
    of.write('_USE_INTERNAL_BRIDGE_SQV\n')
    of.write('_USE_NORMAL_SQV\n')
    for line_Index in range(len(lines)):
        oline = lines[line_Index]
        # print(oline)
        # Parse gcode line
        if oline.startswith(';TYPE:Internal infill'):
            in_infill = True
            of.write(oline)
            of.write('_USE_INFILL_SQV\n')
        elif oline.startswith(';TYPE:Internal perimeter'):
            in_internal_perimeter = True
            of.write(oline)
            of.write('_USE_INTERNAL_PERIMETER_SQV\n')
        elif oline.startswith(';TYPE:Solid infill'):
            in_solid_infill = True
            of.write(oline)
            of.write('_USE_SOLID_INFILL_SQV\n')
        elif oline.startswith(';TYPE:Top solid infill'):
            in_top_solid_infill = True
            of.write(oline)
            of.write('_USE_TOP_SOLID_INFILL_SQV\n')
        elif oline.startswith(';TYPE:Internal bridge infill'):
            in_internal_bridge = True
            of.write(oline)
            of.write('_USE_INTERNAL_BRIDGE_SQV\n')
        elif (oline.startswith(';TYPE:External perimeter') or oline.startswith('; INIT') or oline.startswith(';TYPE:Bridge infill') or oline.startswith(';TYPE:Gap fill') or oline.startswith(';TYPE:Overhang perimeter') or oline.startswith(';TYPE:Thin wall')) and (in_infill or in_internal_perimeter or in_solid_infill or in_top_solid_infill or in_internal_bridge):
            in_infill = False
            in_internal_perimeter = False
            in_solid_infill = False
            in_top_solid_infill = False
            in_internal_bridge = False
            of.write(oline)
            of.write('_USE_NORMAL_SQV\n')
        else:
            of.write(oline)

of.close()
f.close()
# About

Sometimes you just want to make an empty bitstream with encryption/auth/perframe etc but it is annoying to go through the normal Vivado flow, or you might want to script generating a bunch of bitstreams, for reasons. This project is a skeleton for doing just that. 

Supports
- Encryption
- Authentication
- PerframeCRC

You can add other bitstream properties pretty easily by extending the BitstreamGenerator class.

All keys are hardcoded. If you need different keys, just edit the source, or extend the class.

# Install

Requires `dearpygui` to run the gui. 

```
$> pip3 install dearpygui
```

Install package

```
$> cd bitstream_generator
$> python3 setup.py develop --user 
```

NOTE: Both CLI and GUI output bitstreams to `bitstream_generator/template/outputs`, so just install with develop so this is easier to find.

# Usage

IMPORTANT: Source your Vivado settings before running the script eg) `source /tools/Xilinx/Vivado/2023.1/settings.sh`. This path may be different depending on where you decided to put Vivado.

## Command Line Interface

```
$> python3 -m bitstream_generator -h

usage: Bitstream Generator [-h] [-d DEVICE] [--perframe] [--encrypt] [--auth]

Quickly generate bitstreams with difference properties for different parts

options:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
  --perframe
  --encrypt
  --auth

```

Check `bitstream_generator/datagen/part_map.csv` for list of parts.

This tool does not make assumptions about what you want to do, it just a quick script to make some bitstreams. 
- If you attempt to generate a bitstream for a part you do not have a license for, it will fail.
- If you set a property on a part that does not support that property, it will fail.

## GUI

```
$> python3 -m bitstream_generator gui
```

Basic GUI interface for selecting a part and the properties you want for the bitstream. After you click generate you will begin to see the Vivado logs in the terminal.


import subprocess
import os
import sys
import argparse
import csv
import logging

from dataclasses import dataclass

datapath, _ = os.path.split(__file__)

PART_CSV = os.path.join(datapath, "datagen/part_map.csv")
LINK_GEN = os.path.join(datapath, "template/srcs/autogen/link.tcl")
BIT_GEN  = os.path.join(datapath, "template/srcs/autogen/bitgen.tcl")
PROJ_XDC = os.path.join(datapath, "template/srcs/proj.xdc")

RELATIVE_RSA_KEY_PATH = "rsa/golden_key.pem" # Path relative to the Vivado runtime environment, not this script.

@dataclass
class BitstreamSettings:
    perframe: bool
    encrypt: bool
    authenticate: bool

class BitstreamGenerator:
    
    def __init__(self):
        self.part_data = csv.DictReader( open( PART_CSV, "r" ), delimiter="," )
        return
    
    def _create_name(self, part_name, settings: BitstreamSettings) -> str:
        name = part_name
        
        if settings.perframe:
            name += "_perframe"
        if settings.encrypt:
            name += "_enc"
        if settings.authenticate:
            name+= "_rsa"
        return name + ".bit"

    def _gen_link_part(self, part_name : str):
        
        logging.info("AUTOGEN: Link part")
        
        with open(LINK_GEN,"w") as f:
            f.write("link_design -top top -part " + part_name)
    
    def _gen_bitgen(self, part_name : str, settings: BitstreamSettings):
        
        logging.info("AUTOGEN: Bit Gen")
        
        output_file = self._create_name(part_name, settings)
        logging.info("OUTPUT FILE: " + output_file)

        with open(BIT_GEN,"w") as f:
            f.write("write_bitstream -force ../outputs/" + output_file)
    
    def _process_settings(self, settings: BitstreamSettings):
        logging.info("AUTOGEN: Constraints")
        with open(PROJ_XDC,"w") as f:
            if settings is None:
                return
            if settings.perframe:
                logging.info(" -- PERFRAMECRC Enabled")
                f.write('set_property BITSTREAM.GENERAL.PERFRAMECRC "Yes" [current_design];\n')
            if settings.encrypt:
                logging.info(" -- ENCRYPT Enabled")
                f.write('set_property BITSTREAM.ENCRYPTION.ENCRYPT "Yes" [current_design];\n') 
                f.write('set_property BITSTREAM.ENCRYPTION.KEY0 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA [current_design];\n')
                f.write('set_property BITSTREAM.ENCRYPTION.STARTIV0 00000000000000000000000000000000 [current_design];\n')
                f.write('set_property BITSTREAM.ENCRYPTION.STARTCBC 00000000000000000000000000000000 [current_design];\n')
            if settings.authenticate:
                logging.info(" -- AUTHENTICATION Enabled")
                f.write('set_property BITSTREAM.AUTHENTICATION.AUTHENTICATE "Yes" [current_design];\n')
                f.write('set_property BITSTREAM.AUTHENTICATION.RSAPRIVATEKEYFILE ' + RELATIVE_RSA_KEY_PATH + ' [current_design];\n')
        return

    def _launch(self):
        
        logging.info("LAUNCH RUN")
        
        ret_path = os.getcwd()
        
        os.chdir(os.path.join(datapath, "template/srcs"))
        
        result = subprocess.run(["make", "run"])
        
        os.chdir(ret_path)
    
    def generate(self, part_name : str, settings : BitstreamSettings):
        
        logging.info("GENERATE: target -> " + part_name)
        
        part_info = [p for p in self.part_data if p["PART"] == part_name]
        
        if len(part_info) < 1:
            raise ValueError("No record for part " + part_name + " found.")
    
        self._process_settings(settings)
        self._gen_link_part(part_name) 
        self._gen_bitgen(part_name, settings)

        self._launch()

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(prog="Bitstream Generator",
            description="Quickly generate bitstreams with difference properties for different parts",
            epilog="FPGA Assurance for Navy & Government Systems (FANGS) Lab")
    # ARGHS
    parser.add_argument("-d","--device",type=str, default=None)
    parser.add_argument("--perframe", action='store_true')
    parser.add_argument("--encrypt", action='store_true')
    parser.add_argument("--auth", action='store_true')
    args = parser.parse_args()
    
    if args.device is None:
        raise ValueError("Must supply target device with --device")

    settings = BitstreamSettings(args.perframe, args.encrypt, args.auth)

    BG = BitstreamGenerator()

    BG.generate(args.device, settings) 

if __name__ == "__main__":
    main()

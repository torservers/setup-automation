#!/usr/bin/python

import sys

from argparse import ArgumentParser

if __name__ == "__main__":
    aparser = ArgumentParser(description="Set MyFamily value in tor config file")
    aparser.add_argument("--file", "-f", help="file to change")
    aparser.add_argument("fingerprints", help="fingerprints to write")
    
    args = aparser.parse_args()
    
    # read config
    try:
        with open(args.file, "r") as f:
            config_lines = f.readlines()
    except IOError:
        print("[!] couldn't open config file for reading. Check the permissions")
        sys.exit(-1)
        
    myfamily_line_index = None
    for l in config_lines:
        if l.startswith("MyFamily"):
            myfamily_line_index = config_lines.index(l)
            
    new_myfamily_line = "MyFamily %s\n" % (args.fingerprints)
    
    if myfamily_line_index is not None:
        print("[i] found MyFamily line, replacing it with new values")
        config_lines[myfamily_line_index] = new_myfamily_line
    else:
        config_lines.append(new_myfamily_line)

    print config_lines
        
    # write config
    try:
        with open(args.file, "w") as f:
            for l in config_lines:
                f.write(l)
    except IOError:
        print("[!] couldn't open config file for writing. Check the permissions")
        sys.exit(-1)

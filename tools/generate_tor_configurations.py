#!/usr/bin/python

import sys

from argparse import ArgumentParser
from jinja2 import Template

if __name__ == "__main__":
    parser = ArgumentParser(description="Create multiple tor configurations \
             for different IP addresses running on the same host")
    parser.add_argument("--address", "-a", help="IP Address of a process", 
                        action="append", required=True)
    parser.add_argument("--nickname", "-n", help="Nickname of a relay", 
                        action="append", required=True)
    parser.add_argument("--config-template", "-c", help="path to torrc template",
                        required=True)
    
    args = parser.parse_args()
    
    if len(args.nickname) != len(args.address):
        print("[!] You need to specify the same number of IP addresses and nicknames")
        sys.exit(-1)
        
    if len(args.address) > 9:
        print("[!] Since this is a hack, no more than 9 processes are supported right now")
        sys.exit(-1)
        
    try:
        with open(args.config_template) as f:
            t = Template(f.read())
    except IOError:
        print("[!] Cannot read template file")
        sys.exit(-1)

    for conf in zip(range(1, len(args.address)+1), args.address, args.nickname):
        try:
            with open("/tmp/tor%i.cfg" % conf[0], "w") as f:
                f.write(t.render(
                    item=conf[0],
                    ip_address=conf[1],
                    nickname=conf[2],
                ))
        except:
            print("[!] Could not open target file for writing. You may have a permission problem");

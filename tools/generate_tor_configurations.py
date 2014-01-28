#!/usr/bin/python

import sys
from os import mkdir, chown
from pwd import getpwnam
from grp import getgrnam

from argparse import ArgumentParser
from jinja2 import Template

if __name__ == "__main__":
    parser = ArgumentParser(description="Create multiple tor configurations \
             for different IP addresses running on the same host")
    parser.add_argument("--addresses", "-a", help="process IP addresses", 
                        required=True)
    parser.add_argument("--nicknames", "-n", help="process nicknames", 
                        required=True)
    parser.add_argument("--config-template", "-c", help="path to torrc template",
                        required=True)
    
    args = parser.parse_args()
    
    addresses = args.addresses.split(",")
    nicknames = args.nicknames.split(",")
    
    if len(nicknames) != len(addresses):
        print("[!] You need to specify the same number of IP addresses and nicknames")
        sys.exit(-1)
        
    if len(addresses) > 9:
        print("[!] Since this is a hack, no more than 9 processes are supported right now")
        sys.exit(-1)
        
    try:
        with open(args.config_template) as f:
            t = Template(f.read())
    except IOError:
        print("[!] Cannot read template file")
        sys.exit(-1)
        
    tor_uid = getpwnam('debian-tor').pw_uid 
    tor_gid = getgrnam('debian-tor').gr_gid

    for conf in zip(range(1, len(addresses)+1), addresses, nicknames):
        try:
            with open("/etc/tor/tor%i.cfg" % conf[0], "w") as f:
                f.write(t.render(
                    item=conf[0],
                    ip_address=conf[1],
                    nickname=conf[2],
                ))
            print("[i] wrote /etc/tor/tor%i.cfg" % conf[0])
        except:
            print("[!] Could not open target file for writing. You may have a permission problem")

        try:
            mkdir("/var/lib/tor%i" % conf[0], 0770)
        except:
            print("[i] could not create /var/lib/tor%i" % conf[0])
        try:
            chown("/var/lib/tor%i" % conf[0], tor_uid, tor_gid)
        except:
            print("[i] could not modify permissions on /var/lib/tor%i" % conf[0])


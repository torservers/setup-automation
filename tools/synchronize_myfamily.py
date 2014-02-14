#!/usr/bin/python

import sys

from argparse import ArgumentParser
from subprocess import check_output, check_call

def get_fingerprints(user, host, port):
    res = check_output(["/usr/bin/ssh", "%s@%s" % (user, host), "-p %i" % port,
                        "python /opt/torservers/scripts/get_fingerprints.py"])
    fingerprints = []
    for line in res.split("\n"):
        if line != "":
            fingerprints.append(line)
    return fingerprints

def set_myfamily(user, host, port, myfamily_line):
    return check_call(["/usr/bin/ssh", "%s@%s" % (user, host), "-p %i" % port, 
                       "python /opt/torservers/scripts/set_myfamily.py '%s'" %
                       myfamily_line])

if __name__ == "__main__":
    aparser = ArgumentParser(description="synchronize MyFamily fingerprints \
                             across a larger number of Tor relays")
    aparser.add_argument("--inventory", "-i", help="Ansible inventory file")
    aparser.add_argument("--username", "-u", help="SSH username")
    aparser.add_argument("--port", "-p", help="SSH port")

    args = aparser.parse_args()
    
    # read inventory file
    try:
        with open(args.inventory) as f:
            inventory_lines = f.readlines()
    except IOError:
        print("[!] could not open inventory file.")
        sys.exit(-1)
        
    # extract host information
    hosts = []
    for l in inventory_lines:
        if not l.startswith("["):
            hostline_elements = l.split()
            host_dict = {}
            for e in hostline_elements:
                if e.startswith("ansible_ssh_host"):
                    host_dict['address'] = e.split("=")[1]
                elif e.startswith("ansible_ssh_user"):
                    host_dict['user'] = e.split("=")[1]
                elif e.startswith("ansible_ssh_port"):
                    host_dict['port'] = int(e.split("=")[1])
            hosts.append(host_dict)
    print("[i] found %i hosts" % len(hosts))
                    
    fingerprints = []

    for host in hosts:
        if "user" in host.keys():
            username = host['user']
        else:
            username = args.username

        if "port" in host.keys():
            port = host['port']
        else:
            port = int(args.port)
            
        host_fingerprints = get_fingerprints(username, host['address'], port)
        print("[i] host %s has %i fingerprints: %s" % (host, 
              len(host_fingerprints), ", ".join(host_fingerprints)))
        fingerprints.extend(host_fingerprints)

    print("[i] found %i fingerprints total" % len(fingerprints))
        
    myfamily_line = ", ".join([ "$"+x for x in fingerprints])
    
    print("[i] new MyFamily line is: %s" % myfamily_line)
    
    for host in hosts:
        if "user" in host.keys():
            username = host['user']
        else:
            username = args.username

        if "port" in host.keys():
            port = host['port']
        else:
            port = int(args.port)

        set_myfamily(username, host['address'], port, myfamily_line)
        print("[i] set new myfamily line on host %s" % host)

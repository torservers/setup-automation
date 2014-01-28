from os import listdir
from os.path import join

from stem.control import Controller

def main():
    stmt_path = '/var/run/torctl/statements'
    stmt_files = [ x for x in listdir(stmt_path) if 'stmt' in x ]
    for stmt_file in stmt_files:
        with open(join(stmt_path,stmt_file)) as f:
            stmt = f.read()
            address = stmt.split("=")[1]
            port=int(address.split(":")[1])

            with Controller.from_port(port=port) as controller:
                controller.authenticate() 
                fingerprint = controller.get_info("fingerprint")

                print fingerprint
    
if __name__ == "__main__":
    main()

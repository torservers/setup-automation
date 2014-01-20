from stem.control import Controller

def main():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate() 
        fingerprint = controller.get_info("fingerprint")

        print fingerprint
  
if __name__ == "__main__":
    main()

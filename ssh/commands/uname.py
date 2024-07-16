def handle(server, command):
    print("Command: " + command)
    args = command.split(" ")
    args.pop(0)
    print("Args: " + str(args))
    result = b""
    
    # Default values 
    kernel_name = b"Linux"
    nodename = server.hostname.encode('utf-8')
    kernel_release = b"5.4.0-42-generic"
    kernel_version = b"#46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020"
    machine = b"x86_64"
    processor = b"x86_64"
    hardware_platform = b"x86_64"
    operating_system = b"GNU/Linux"
    
    # Handle the arguments.
    for arg in args:
        arg = str(arg).lower()
        if arg == "-a":
            result = b"\r\n" + kernel_name + b" " + nodename + b" " + kernel_release + b" " + kernel_version + b" " + machine + b" " + processor + b" " + hardware_platform + b" " + operating_system
        elif arg == "-m":
            result = b"\r\n" + machine
        elif arg == "-n":
            result = b"\r\n" + nodename
        elif arg == "-o":
            result = b"\r\n" + operating_system
        elif arg == "-p":
            result = b"\r\n" + processor
        elif arg == "-r":
            result = b"\r\n" + kernel_release
        elif arg == "-s":
            result = b"\r\n" + kernel_name
        elif arg == "-v":
            result = b"\r\n" + kernel_version
        else:
            result = b"\r\nuname: invalid option -- '" + arg.encode('utf-8') + b"'\r\nusage: uname [-amnoprsv]\r\n"
        
        break
    
    return result + b"\r\n"

description = "Print system information."

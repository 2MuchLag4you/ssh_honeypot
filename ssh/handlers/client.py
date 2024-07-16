import paramiko
import ssh

def client_handle(client, addr, username: str | None, password: str | None) -> None: 
    """Handle the client connection."""
    client_ip = addr[0]
    # print(client)
    # print(addr)
    print(f"{client_ip} ({username}) connected to server.")
    
    try:
        transport = paramiko.Transport(client)  
        transport.local_version = "SSH-2.0-MySSHServer_1.0"
        
        # Create a new instance of the Server class.
        server = ssh.Server(client_ip=client_ip, input_username=username, input_password=password)
        
        # Add the host key to the server.
        transport.add_server_key(server.host_key)
        transport.start_server(server=server)
        
        # Establish the connection.
        channel = transport.accept(100)
        
        if channel is None:
            print("No channel was opened.")
            return
        
        try:
            # Send a generic welcome banner to the client.
            channel.send("Welcome to the SSH session\r\n\r\n")
            
            ssh.handlers.shell_handle(channel, server=server)
            
        except Exception as error:
            print(error)
            
    except Exception as error:
        print(error)

    finally:
        try:
            transport.close()
        except Exception:
            pass
        
        client.close()
                    
            
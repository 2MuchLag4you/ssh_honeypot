import socket
import threading
import time
from ssh.handlers import client_handle

class HoneypotServer:
    def __init__(self, address:str="0.0.0.0", port:int=8022, username:str|None=None, password:str|None=None, concurrent_connections:int=100, banner:bool=True, delay:int =5):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.concurrent_connections = concurrent_connections
        self.server_socket = None
        self.client_threads = []
        self.client_sockets = []
        self.running = True
        self.banner_enabled = banner
        self.banner_delay = delay

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.address, self.port))
        
        # Can handle 100 concurrent connections.
        self.server_socket.listen(self.concurrent_connections)
        
        print(f"Server is listening on {self.address}:{self.port} with {self.concurrent_connections} concurrent connections.")
        
        try:
            while self.running:
                try:
                    # Accept connection from client and address.
                    client_socket, addr = self.server_socket.accept()
                    self.client_sockets.append(client_socket)
                    
                    if self.banner_enabled:
                        # Introduce a delay before handling the client
                        time.sleep(self.banner_delay)  # Adjust delay as needed
                        
                    # Start a new thread to handle the client connection.
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                    client_thread.start()
                    self.client_threads.append(client_thread)
                except Exception as error:
                    print("!!! Exception - Could not open new client connection !!!")
                    print(error)
        except KeyboardInterrupt:
            print("Server shutting down.")
            self.stop()
        
    def handle_client(self, client_socket: socket.socket, addr):
        try:
            if self.banner_enabled:
                banner_message = b"Welcome to my SSH honeypot server\n"
                client_socket.send(banner_message)
                
            client_handle(client_socket, addr, self.username, self.password)
        finally:
            client_socket.close()
    
    def stop(self):
        self.running = False
        # Close all client sockets
        for client_socket in self.client_sockets:
            try:
                client_socket.close()
            except Exception as e:
                print(f"Error closing client socket: {e}")
        # Close the server socket
        if self.server_socket:
            self.server_socket.close()
        # Wait for all client threads to finish
        for client_thread in self.client_threads:
            client_thread.join()
        print("All connections have been closed.")

def honeypot(address:str="0.0.0.0", port:int=8022, username:str|None=None, password:str|None=None, concurrent_connections:int=100, banner:bool=True, delay:int =5):
    server = HoneypotServer(address, port, username, password, concurrent_connections, banner, delay)
    server.start()

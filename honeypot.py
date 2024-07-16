import socket
import threading
from ssh.handlers import client_handle

class HoneypotServer:
    def __init__(self, address="0.0.0.0", port=8022, username=None, password=None, concurrent_connections=100):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.concurrent_connections = concurrent_connections
        self.server_socket = None
        self.client_threads = []
        self.client_sockets = []
        self.running = True

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
        
    def handle_client(self, client_socket, addr):
        try:
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

def honeypot(address="0.0.0.0", port=8022, username=None, password=None, concurrent_connections=100):
    server = HoneypotServer(address, port, username, password, concurrent_connections)
    server.start()

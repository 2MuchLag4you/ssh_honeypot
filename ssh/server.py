import paramiko
import threading
from datetime import datetime
from logger import creds_logger, funnel_logger


# Define the class that will handle the SSH server.
class Server(paramiko.ServerInterface):
    # Define the constructor for the Server class.
    def __init__(self, client_ip: str, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.command_history = []
        self.client_user = None
        self.input_username = input_username
        self.input_password = input_password
        self.hostname = "honeybox"
        self.connected_time = datetime.now()
        try:
            print("Loading server key.")
            self.host_key = paramiko.RSAKey(filename="server.key")
        except FileNotFoundError:
            print("Creating server key.")
            self.host_key = paramiko.RSAKey.generate(2048)
            self.host_key.write_private_key_file("server.key")
        
        self.__prompt = f"{self.hostname}$ "
        # Define the prompt for the SSH server.

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        
    def get_allowed_auths(self, username: str):
        return "password"
    
    def check_auth_password(self, username: str, password: str):
        funnel_logger.info(f'Client {self.client_ip} attempted connection with ' + f'username: {username}, ' + f'password: {password}')
        creds_logger.info(f'{self.client_ip}, {username}, {password}')
        self.client_user = username
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL
        
    def check_channel_shell_request(self, channel: paramiko.Channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    
    def prompt(self):
        if self.client_user is not None:
            self.__prompt = f"{self.client_user}@{self.hostname}$ "
        else:
            self.__prompt = f"{self.hostname}$ "
        return self.__prompt
    
    def check_channel_exec_request(self, channel: paramiko.Channel, command: bytes):
        command = str(command)
        return True
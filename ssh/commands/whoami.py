def handle(server, command):
    return f"\n{server.client_user}\r\n\r\n".encode('utf-8')

description = "Print the user name."

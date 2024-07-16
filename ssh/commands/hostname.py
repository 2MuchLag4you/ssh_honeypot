def handle(server, command):
    return f"\n{server.hostname}\r\n".encode('utf-8')

description = "Get the hostname of the current machine."
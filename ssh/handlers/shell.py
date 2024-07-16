
from logger import funnel_logger
from ssh.server import Server
from ssh.commands import command_registry
import paramiko

def shell_handle(channel: paramiko.Channel, server: Server) -> None:
    """Handle the shell session."""
    # Send the prompt to the client.
    channel.send(f"{server.prompt()}")
    # Variable to store the command.
    command = b""
    command_history = []
    history_index = -1
    
    while True:
        char = channel.recv(1)
        # If a new character is received, reset the history index
        if char != b'\x1b':
            history_index = -1
            
        ### ? In progress, handling arrow keys for command history
        
        # if char == b'\x1b':
        #     char += channel.recv(2)
        #     print(history_index)
        #     # print(command_history)
        #     if char == b'\x1b[A':  # Arrow up
        #         if command_history:
        #             if history_index == -1:
        #                 history_index = len(command_history) - 1
        #             elif history_index > 0:
        #                 history_index -= 1
        #             command = command_history[history_index]
        #             # Clear the current input line
        #             channel.send(b'\r' + b' ' * (len(server.prompt()) + len(command)) + b'\r')
        #             # Print the prompt and the command
        #             channel.send(f"{server.prompt()}{command.decode('utf-8')}".encode('utf-8'))
        #     elif char == b'\x1b[B':  # Arrow down
        #         if command_history:
        #             if history_index < len(command_history) - 1:
        #                 history_index += 1
        #                 command = command_history[history_index]
        #             else:
        #                 history_index = -1
        #                 command = b''
        #             # Clear the current input line
        #             channel.send(b'\r' + b' ' * (len(server.prompt()) + len(command)) + b'\r')
        #             # Print the prompt and the command
        #             channel.send(f"{server.prompt()}{command.decode('utf-8')}".encode('utf-8'))
        #     elif char == b'\x1b[C': # Arrow right
        #         print('Right')
        #     elif char == b'\x1b[D': # Arrow left
        #         print('Left')                    
                    
        #     continue
        
        ### ? In progress, handling arrow keys for command history
        
        channel.send(char)

        if not char:
            channel.close()
            break

        if char not in {b'\x1b[A', b'\x1b[B'}:
            command += char
            
            
        # print(char)
        # print(command)
        
        # Emulate common shell commands.
        if char == b"\r":
            # Convert bytes to string.
            command_str = command.strip().decode('utf-8')
            # Handle the exit command.
            if command_str:
                command_history.append(command)
            
            print(command_str.split(' ')[0])
            # Split the command by spaces.
            full_command = command_str
            command_str = command_str.split(' ')[0]
            
            
            # Handle the exit command.
            if command_str == 'exit':
                response = b"\n Goodbye!\r\n"
                funnel_logger.info(f'Command {command.strip()}' + "executed by " f'{server.client_user}@{server.client_ip}')
                print(f"Session for {server.client_user}@{server.client_ip} exited.")
                channel.close()
            # Handle the help command.
            elif command_str == 'help':
                response = b"\nAvailable commands:\r\n"
                for cmd, (_, desc) in command_registry.items():
                    response += "{:<8} - {:<10}\r\n".format(cmd, desc).encode('utf-8')
                    # response += f"{cmd} - {desc}\r\n".enchode('utf-8')
                response += b"\r\n"
                funnel_logger.info(f'Command {full_command}' + " executed by " f'{server.client_user}@{server.client_ip}')
            # Handle the dynamically imported commands from the commands/ directory.
            elif command_str in command_registry:
                handle_func, _ = command_registry[command_str]
                response = handle_func(server, full_command)
                funnel_logger.info(f'Command {full_command}' + " executed by " f'{server.client_user}@{server.client_ip}')
            # Handle empty command.
            elif command_str == "":
                response = b"\r\n"
            # Handle command not found. 
            else:
                print (f"Session for {server.client_user}@{server.client_ip} executed unknown command: {full_command}")
                funnel_logger.error(f"Session for {server.client_user}@{server.client_ip} executed unknown command: {full_command}")
                response = b"\nCommand not found.\r\n"
                
            # Send the response to the client.
            channel.send(response)
            # Restore the prompt.
            channel.send(f"{server.prompt()}")
            # Reset the command
            command = b""
        # Handle tab key.
        #? Tab key is represented by the following byte: b"\t"
        elif char == b"\t":
            # print("Tab key pressed.")
            channel.send(b"\t")
        # Handle backspace key.
        #? Backspace key is represented by the following byte: b"\x7f"
        elif char == b"\x7f":
            # Ensure we don't backspace past the prompt.
            if command == b"\x7f":
                command = b""
            # Remove the last two characters from the command.
            else:
                command = command[:-2]
                # print("Backspace key pressed.")
                channel.send(b"\b \b")
        elif char == b"\x1b":
            print("")
        # Handle Ctrl+C key.
        elif char == b"\x03":
            channel.send(b"Ctrl+C key pressed, closing connection.\r\n")
            print(f"Ctrl+C key pressed on the session, closing connection for client {server.client_user}@{server.client_ip}.")
            channel.close()
        else:
            print("Uncatched key pressed.")
            print(char)
            pass
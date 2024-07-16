# ssh_honeypot
A basic SSH honeypot to capture IP Adresses, usernames, passwords, and commands.

## Usage

SSH_HONEYPY requires a bind IP address (`-a`) and network port to listen on (`-p`). Use `0.0.0.0` to listen on all network interfaces. 

```
-a / --address: Bind address. (Default : 0.0.0.0)
-p / --port: Port. (Default: 8022)
-c / --concurrent_connections: Amount of allowed concurrent connections. (Default: 100)
-b / --banner: Flag to enable delayed SSH sessions. (Default: False)
-d / --delay: Amount of delay in seconds (Default: 5)
```

Example: `python3 main.py -a 127.0.0.1 -p 8022`

**Optional Arguments**

A username (`-u`) and password (`-w`) can be specified to authenticate the SSH server. The default configuration will accept all usernames and passwords.

```
-u / --username: Username.
-w / --password: Password.
```

Example: `python3 main.py -a 0.0.0.0 -p 22 -u admin -p admin`
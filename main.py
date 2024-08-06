import argparse
import honeypot
import honeypot.objects
import honeypot.objects.honeypot_settings
import honeypot.logger

global honeypot_settings

honeypot_settings = honeypot.objects.HoneypotSettings(
    address="0.0.0.0",
    port=8022,
    username=None,
    password=None,
    concurrent_connections=100,
    banner=True,
    delay=5,
    hostname="hostnametest",
    log_directory="./log",
    overwrite_arguments=False
)

if __name__ == "__main__":
    # Create parser
    parser = argparse.ArgumentParser() 
    parser.add_argument('-a','--address', type=str, default="0.0.0.0")
    parser.add_argument('-p','--port', type=int, default=8022)
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-w', '--password', type=str)
    parser.add_argument('-c', '--concurrent_connections', type=int, default=100)
    parser.add_argument('-b', '--banner', action='store_true')
    parser.add_argument('-d', '--delay', type=int, default=5)
    
    args = parser.parse_args()
    
    # Configuring the honeypot
    honeypot_settings = honeypot.objects.HoneypotSettings(
        address=args.address,
        port=args.port,
        username=args.username,
        password= args.password,
        concurrent_connections=args.concurrent_connections,
        banner=args.banner,
        delay=args.delay,
        hostname=honeypot_settings.hostname,
        log_directory=honeypot_settings.log_directory
    )
    
    # Start the honeypot
    honeypot.honeypot(honeypot_settings)


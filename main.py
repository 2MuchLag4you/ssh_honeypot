import argparse
import honeypot

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
    
    honeypot.honeypot(args.address, args.port, args.username, args.password, args.concurrent_connections, args.banner, args.delay)


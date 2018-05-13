import argparse

from scripts.server.main_server import Server

args_parser = argparse.ArgumentParser(description="Command line commands for manipulating the chat server")

args_parser.add_argument('-s','--start_server',dest="server",help="start server with --start_server")

args=args_parser.parse_args()

if args.server:
    print("Server Started...")
    Server().start_server()

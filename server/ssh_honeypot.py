# server/ssh_honeypot.py

import logging, threading, socket
from paramiko import RSAKey, Transport, server
from paramiko.common import OPEN_SUCCEEDED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
from dotenv import load_dotenv
import os

load_dotenv()
HOST_KEY_PATH = os.path.join(os.path.dirname(__file__), 'host_rsa_key')
LOG_FILE      = os.path.join(os.getcwd(), 'honeypot.log')

class HoneypotServer(server.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        logging.info(f"AUTH_ATTEMPT {username}/{password}")
        return server.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_request(self, kind, chanid):
        # use the constants imported from paramiko.common
        return OPEN_SUCCEEDED if kind == 'session' else OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

def start_honeypot(host='0.0.0.0', port=2222):
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    host_key = RSAKey(filename=HOST_KEY_PATH)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    print(f"[+] SSH Honeypot listening on {host}:{port}")
    while True:
        client, addr = sock.accept()
        transport = Transport(client)
        transport.add_server_key(host_key)
        server_handler = HoneypotServer()
        try:
            transport.start_server(server=server_handler)
            chan = transport.accept(20)
            if chan is None:
                continue
            server_handler.event.wait(10)
            chan.send(b"Welcome to SSH Honeypot!\n")
            while True:
                data = chan.recv(1024)
                if not data:
                    break
                cmd = data.decode('utf-8', errors='ignore').strip()
                logging.info(f"CMD {addr[0]}:{addr[1]} -> {cmd}")
                chan.send(f"bash: {cmd}: command not found\n".encode())
            chan.close()
        except Exception as e:
            logging.info(f"Unknown exception: {e}")
        finally:
            transport.close()

if __name__ == "__main__":
    start_honeypot()

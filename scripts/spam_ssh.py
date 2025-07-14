#!/usr/bin/env python3
import paramiko
import random
import time
import argparse
from itertools import product

HOST = "127.0.0.1"
PORT = 2222

def load_list(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def try_login(username, password, timeout=5):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, port=PORT,
                       username=username,
                       password=password,
                       timeout=timeout,
                       allow_agent=False,
                       look_for_keys=False)
        # If you actually get a shell, send a dummy command
        chan = client.invoke_shell()
        chan.send("uname -a && whoami\n")
        time.sleep(0.5)
        chan.close()
    except Exception:
        # expected on failure; ignore
        pass
    finally:
        client.close()

def main(userlist, passlist, delay_min, delay_max, forever):
    users = load_list(userlist)
    pwds  = load_list(passlist)

    attempts = list(product(users, pwds))
    random.shuffle(attempts)

    while True:
        for u, p in attempts:
            try_login(u, p)
            # random delay between attempts
            time.sleep(random.uniform(delay_min, delay_max))
        if not forever:
            print("Done one pass through all combos.")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SSH brute-force spammer against your honeypot."
    )
    parser.add_argument("-U", "--users",  default="scripts/userlist.txt",
                        help="Path to newline list of usernames")
    parser.add_argument("-P", "--pwds",   default="scripts/passlist.txt",
                        help="Path to newline list of passwords")
    parser.add_argument("--min-delay",    type=float, default=0.1,
                        help="Min seconds between attempts")
    parser.add_argument("--max-delay",    type=float, default=1.0,
                        help="Max seconds between attempts")
    parser.add_argument("--forever",      action="store_true",
                        help="Loop infinitely over the wordlists")
    args = parser.parse_args()

    main(args.users, args.pwds,
         args.min_delay, args.max_delay,
         args.forever)

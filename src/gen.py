#!/usr/bin/env python3
import json
import os

GEN_DIR = 'gen'
HOST_KEY = 'public-ip'
USER_KEY = 'ssh-user'

nodes = {}
customers = {}

with open('nodes.json', 'r') as cfg:
    nodes = json.load(cfg)

with open('customers.json', 'r') as cfg:
    customers = json.load(cfg)

def gen_sshconfig():
    DEFAULT_USER = 'scionlab'

    with open(os.path.join(GEN_DIR, 'sshconfig'), 'w') as f:
        remotes = {}
        remotes.update(nodes)
        remotes.update(customers)
        for name, data in remotes.items():
            user = data[USER_KEY] if USER_KEY in data else DEFAULT_USER
            f.write(f"Host sbas-{name}\n")
            f.write(f"    HostName {data[HOST_KEY]}\n")
            f.write(f"    User {user}\n\n")

def gen_client_cfgs():
    for name, data in customers.items():
        cfg = data.copy()
        del cfg[HOST_KEY]
        del cfg[USER_KEY]
        with open(os.path.join(GEN_DIR, f"client-{name}.json"), 'w') as f:
            json.dump(cfg, f)

if __name__ == '__main__':
    gen_sshconfig()
    gen_client_cfgs()
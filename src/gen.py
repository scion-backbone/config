#!/usr/bin/env python3
import json
import os

GEN_DIR = 'gen'
HOST_KEY = 'public-ip'
USER_KEY = 'ssh-user'

nodes = {}
clients = {}

with open('nodes.json', 'r') as cfg:
    nodes = json.load(cfg)

with open('clients.json', 'r') as cfg:
    clients = json.load(cfg)

def gen_sshconfig():
    DEFAULT_USER = 'scionlab'

    with open(os.path.join(GEN_DIR, 'sshconfig'), 'w') as f:
        remotes = {}
        remotes.update(nodes)
        remotes.update(clients)
        for name, data in remotes.items():
            user = data[USER_KEY] if USER_KEY in data else DEFAULT_USER
            f.write(f"Host sbas-{name}\n")
            f.write(f"    HostName {data[HOST_KEY]}\n")
            f.write(f"    User {user}\n\n")

def gen_client_cfgs():
    # From the file "customers.json", generate the individual client
    # configuration files
    for name, data in clients.items():
        cfg = data.copy()
        del cfg[HOST_KEY] # only required for SSH
        del cfg[USER_KEY] # only required for SSH

        # Add information about provider nodes
        relevant_fields = ['vpn-key', 'public-ip'] 
        for provider in cfg['providers']:
            node = nodes[provider['id']]
            for field in relevant_fields:
                provider[field] = node[field]

        with open(os.path.join(GEN_DIR, f"client-{name}.json"), 'w') as f:
            json.dump(cfg, f, indent=2)

if __name__ == '__main__':
    gen_sshconfig()
    gen_client_cfgs()
#!/usr/bin/env python3
import json

HOST_KEY = 'public-ip'
USER_KEY = 'ssh-user'
DEFAULT_USER = 'scionlab'

remotes = {}

with open('nodes.json', 'r') as cfg:
    remotes.update(json.load(cfg))

with open('customers.json', 'r') as cfg:
    remotes.update(json.load(cfg))

with open('sshconfig', 'w') as out:
    for name, data in remotes.items():
        user = data[USER_KEY] if USER_KEY in data else DEFAULT_USER
        out.write(f"Host sbas-{name}\n")
        out.write(f"    HostName {data[HOST_KEY]}\n")
        out.write(f"    User {user}\n\n")


#!/usr/bin/env python3
import json 

def get_clients_config():
    # Load the clients configuration file
    with open('./clients.json', 'r') as c:
        return json.load(c)

def get_nodes_config():
    # Load the nodes configuration file
    with open('./nodes.json', 'r') as f:
        return json.load(f)

def check_integrity():
    clients = get_clients_config()
    nodes = get_nodes_config()['nodes']
    exit_status = 0

    def error(msg):
        global exit_status
        print("Integrity check failed:", msg)
        exit_status = 1

    # Check if the providers listed in each client configuration include the
    # correct clients in the connected-clients array
    for name, client in clients.items():
        for provider in client['providers']:
            if provider['id'] not in nodes:
                error(f"Provider {provider['id']} of client {name} does not exist in nodes.json.")
            elif name not in nodes[provider['id']]['connected-clients']:
                error(f"{name} not included in {provider['id']} connected-clients list.")

    # Check if the clients listed in each node configuration include the node
    # as one of its providers            
    for name, node in nodes.items():
        for connected_client in node['connected-clients']:
            client = clients.get(connected_client)
            if not client: # check if connected client of a node does not exist in clients.json
                error(f"{connected_client} configuration does not exist in clients.json.")
            else:
                for provider in client['providers']: 
                    if provider['id'] == name:
                        break
                else:
                    error(f"{name} not included in the providers list of client {connected_client}.")

    exit(exit_status)
    

if __name__ == '__main__':
    check_integrity()


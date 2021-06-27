import json 

def get_clients_config():
    # Load the clients configuration file
    with open('./clients.json', 'r') as c:
        clients_config = json.load(c)
    return clients_config

def get_nodes_config():
    # Load the nodes configuration file
    with open('./nodes.json', 'r') as f:
        nodes_config = json.load(f)
    nodes = nodes_config["nodes"]
    return nodes

def test_config_files():
    clients = get_clients_config()
    nodes = get_nodes_config()
    exit_status = 0

    # Check if the providers listed in each client configuration include the correct clients in the connected_clients array
    for client, client_info in clients.items():
        providers = client_info['providers']
        for provider in providers:
            if (not nodes.get(provider['id'])):
                print(f'''Provider {provider['id']} of client {client} does not exist in nodes.json.''')    
                exit_status = 1
            elif (client not in nodes.get(provider['id'])['connected-clients']):
                print(f'''{client} not included in {provider['id']} connected-clients list.''')
                exit_status = 1
    # Check if the clients listed in each node configuration include the node as one of its providers            
    for name, node in nodes.items():
        connected_clients = node['connected-clients']
        for connected_client in connected_clients:
            client_info = clients.get(connected_client)
            if not client_info: # check if connected client of a node does not exist in clients.json
                print(f'''{connected_client} configuration does not exist in clients.json.''')
                exit_status = 1
            else:
                client_providers = client_info['providers']
                match = False
                for provider in client_providers: 
                    if provider['id'] == name:
                        match = True
                        break
                if not match:
                    print(f'''{name} not included in the providers list of client {connected_client}.''')
                    exit_status = 1
    exit(exit_status)
    
test_config_files()

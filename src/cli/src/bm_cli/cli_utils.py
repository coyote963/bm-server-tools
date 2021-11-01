from collections import defaultdict
import configparser
import json

from tabulate import tabulate
import requests
import toml

def _get_port_list(base_port: int, num_servers: int):
    """Generate a list of ports"""
    return [str(2 * x + base_port) for x in range(num_servers)]


def get_env(base_port: int, num_servers: int):
    """Returns the environment needed to run the docker file"""
    game_ports = _get_port_list(base_port, num_servers)
    rcon_ports = _get_port_list(base_port + 1, num_servers)
    return {
        'GAME_PORTS': ','.join(game_ports),
        'RCON_PORTS': ','.join(rcon_ports)
    }


def get_ports(base_port: int, num_servers: int):
    """Returns the forwarded ports"""
    all_ports = 2 * num_servers
    tcp_ports = {'{}/tcp'.format(i) : i for i in range(base_port, base_port + all_ports)}
    udp_ports = {'{}/udp'.format(i) : i for i in range(base_port, base_port + all_ports)}
    return {
        **tcp_ports,
        **udp_ports,
        '8000/tcp': 8000
    }


def get_all_servers(server_port):
    """Gets all the currently running services and pretty prints them"""
    server_list = requests.get(f'http://127.0.0.1:{server_port}').json()['servers']
    active_servers = [ server for server in server_list if server['game_id'] != None ]
    if (len(active_servers) == 0):
        return "There are no servers running, add one with the add command"
    else:
        header = active_servers[0].keys()
        rows = [x.values() for x in active_servers]
        return tabulate(rows, header)

def server_is_running(server_port=8000):
    """Returns true if the server is running, otherwise false"""
    try:
        response = requests.get(f'http://127.0.0.1:{server_port}')
    except Exception as e:
        return False
    return True


def convert_to_dict(config):
    config_dict = defaultdict(dict)
    for section in config.sections():
        for key, value in config.items(section):
            config_dict[section][key] = value.strip('"')
    return dict(config_dict)


def convert_toml_to_dict(toml_settings_path: str):
    """Converts a toml string to python dictionary"""
    config = configparser.ConfigParser()
    # Override key format. This keeps key case unchanged
    config.optionxform = str
    config.read(toml_settings_path)
    return convert_to_dict(config)


def post_new_server(settings_dict: dict, mode = 'normal'):
    """Posts a new bman server"""
    settings_dict['mode'] = mode
    serialized_settings = json.dumps(settings_dict)
    serialized_settings.replace("'", '"')
    serialized_settings.replace("////", "/")
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(
        'http://127.0.0.1:8000',
        headers=headers,
        data=serialized_settings)
    return response.json()


def delete_server(game_id: int):
    """Deletes a running boring man server"""
    response = requests.delete(
        'http://127.0.0.1:8000/' + str(game_id),
    )
    return response.json()
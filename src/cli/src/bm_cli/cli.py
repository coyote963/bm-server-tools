import fire
import docker

from .cli_utils import (
    get_env,
    get_ports,
    get_all_servers,
    convert_toml_to_dict,
    post_new_server,
    server_is_running,
    delete_server
)
from .presets import preset_settings

def requires_server(func):
    def wrapper(*args, **kwargs):
        
        if server_is_running():
            return func(*args, **kwargs)
        else:
            print("""
            Server is not running. 
            [python cli.py start] to get started
            """)
    return wrapper


class BoringCLI(object):
    """Tools for managing boring man servers."""

    def start(self, num_servers=3, base_port=42069):
        docker_env = get_env(num_servers, base_port)
        client = docker.from_env()
        try:
            container = client.containers.run(
                "coyotebm/bm-server-api:latest", 
                environment=get_env(base_port, num_servers),
                ports=get_ports(base_port, num_servers),
                detach=True
            )
        except docker.errors.APIError:
            print("An error occurred and the server could not start. Is it already running?")
            return
        with open(".container_id", 'w') as container_file:
            container_file.write(container.id)
        print(f'Started Server listening on 8000')


    def stop(self):
        """Kills the currently running server and all boring man servers"""
        with open('.container_id', 'r') as container_file:
            container_id = container_file.readline()
            client = docker.from_env()
            try:
                container = client.containers.get(container_id)
                container.kill()
            except docker.errors.APIError:
                print("Server is not running")

    @requires_server
    def status(self):
        """Gets the current status of the running server"""
        print(get_all_servers(8000))


    @requires_server
    def add_custom(self, settings_file_path: str):
        """Creates a custom server from an ini file"""
        settings = convert_toml_to_dict(settings_file_path)
        response = post_new_server(settings)
        print(
            f'Added a new server. ID: {response["game_id"]}'
        )

    @requires_server
    def remove(self, game_id: int):
        """Stops a boring man server, freeing it's space"""
        # import pdb; pdb.set_trace()
        response = delete_server(int(game_id))
        if 'error' in response:
            print(response['error'])
        if 'status' in response:
            print(f'Remove {response["game_id"]}: {response["status"]}')


    @requires_server
    def add(self, server_preset: str):
        """Adds a preset server"""
        if server_preset in preset_settings:
            response = post_new_server(preset_settings[server_preset])
            print(
                f'Added a new server. ID: {response["game_id"]}'
            )
        else:
            print(f'Not a preset, valid options are {",".join(preset_settings.keys())}')
            

def main():
    fire.Fire(BoringCLI)

if __name__ == '__main__':
    main()
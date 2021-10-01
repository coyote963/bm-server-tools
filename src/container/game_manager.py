import docker

BM_SETTINGS_FILE = '/home/coyote/files'

def currently_running():
    '''Returns a list of the currently running bm-linux containers'''
    client = docker.from_env()
    return [x for x in client.containers.list() if 'bm-linux' in x.name]

def start_new_instance(config_id):
    '''Creates a new bm-linux container with the configuration ID'''
    client = docker.from_env()
    client.containers.run(
        'bm-linux_game:latest',
        ports = {
             '42069/tcp': 42069,
             '42069/udp': 42069
        },
        volumes = {
             BM_SETTINGS_FILE: {
                 'bind': '/files',
                 'mode': 'rw'
             }
        },
        environment = {
             'CONFIG_ID': config_id
        },
        detach = True 
    )


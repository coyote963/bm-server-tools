from flask import Flask, request, render_template, jsonify

from GameState import ServerGameState
from settings_file_utils import (
    convert_to_toml,
    number_of_files,
    write_settings_file,
    enforce_values
)
from subprocess import Popen, PIPE

PORT_MAPPINGS = [
    {
        'game_port': 42069,
        'rcon_port': 42070,
    }, {
        'game_port': 42071,
        'rcon_port': 42072,
    },{
        'game_port': 42073,
        'rcon_port': 42074,
    }
]

app = Flask(__name__)

server_state = ServerGameState(PORT_MAPPINGS)

@app.route('/', methods=['POST'])
def create_server():
    """
    Creates a Boring Man server with the settings provided in the POST form.
    Returns error if there isn't a server slot available
    """
    game_id = number_of_files()
    free_server = server_state.find_free_server()
    settings = enforce_values(request.form.to_dict())
    if free_server is None:
        return jsonify({'error': 'No free server slots'})
    # Enforce the Rcon and Port values depending on the free server
    settings = enforce_values(settings, 
        {
            'Server': {
                'Port': str(free_server.game_port),
                'Name': 'haha server'
            },
            'Rcon': {
                'RconPort': str(free_server.rcon_port),
            }
        }
    )
    write_settings_file(game_id, convert_to_toml(settings))
    free_server.allocate(game_id)
    return jsonify({'game_id': game_id})


@app.route('/', methods=['GET'])
def get_server_list():
    """
    Returns a list of all the servers that have been created
    """
    return jsonify({
        'servers': server_state.get_server_list()
    })

# @app.route('/environ', methods=['GET'])
# def get_environs():
#     import os
#     return jsonify(dict(os.environ))

@app.route('/<game_id>', methods=['GET'])
def get_server_info(game_id):
    """
    Returns information about a single server with the given game_id
    """
    server_state.refresh()
    return jsonify({
        'server': server_state.get_game_info(game_id)
    })

@app.route('/<game_id>', methods=['DELETE'])
def stop_server(game_id):
    """
    Stops the server with the given game_id
    """
    server_state.refresh()
    try:
        server_state.stop_server(game_id)
    except Exception as e:
        return jsonify({
            'error': str(e)
        })
    return jsonify({
        'status': 'success',
        'game_id': game_id
    })

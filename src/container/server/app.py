from subprocess import Popen, PIPE
from enum import Enum
import logging

from flask import Flask, request, render_template, jsonify

from GameState import ServerGameState, ServerMode
from settings_file_utils import (
    convert_to_toml,
    number_of_files,
    write_settings_file,
    enforce_values,
    set_ports,
    get_port_mappings
)


app = Flask(__name__)

server_state = ServerGameState(get_port_mappings())

@app.route('/', methods=['POST'])
def create_server():
    """
    Creates a Boring Man server with the settings provided in the POST form.
    Returns error if there isn't a server slot available
    """
    game_id = number_of_files()
    free_server = server_state.find_free_server()
    settings = enforce_values(request.json)
    if free_server is None:
        return jsonify({'error': 'No free server slots'}, 501)
    # Enforce the Rcon and Port values depending on the free server
    settings = set_ports(
        settings, 
        free_server.rcon_port, 
        free_server.game_port)
    write_settings_file(game_id, convert_to_toml(settings.dict()))
    if 'mode' not in request.json or request.json['mode'] not in ServerMode.__members__:
        return jsonify({'error': 'Missing or invalid server mode'})
    mode = request.json['mode'].lower()

    free_server.allocate(game_id, settings, mode=ServerMode[mode])
    return jsonify({
        'game_id': game_id, 
        'settings': settings.dict(),
        'pid': free_server.pid
    })


@app.route('/', methods=['GET'])
def get_server_list():
    """
    Returns a list of all the servers that have been created
    """
    server_state.refresh()
    return jsonify({
        'servers': server_state.get_server_list()
    })


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
        server_state.stop_server(int(game_id))
    except Exception as e:
        return jsonify({
            'error': str(e)
        })
    return jsonify({
        'status': 'success',
        'game_id': game_id
    })

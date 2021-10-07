from typing import Dict
import os

import toml
from mergedeep import merge

from SettingsModel import FullSettings, initialize_settings

SETTINGS_FILE_DIR = '/root/.config/BoringManRewrite/'

ENFORCED_VALUES = {
    'Rcon' : {
        'RconPassword': 'admin',
        'RconEnabled': '1',
    },
    'Server': {
        'Logging': '1',
        'DedicatedFPS': '30',
        'TickRate': '3',
        'AllowMD5Error': '1',
        'Votekick': '0',
    },
    'Admins': {
        '0': '76561198303147008' 
    }
}


def convert_to_toml(registration_form: Dict):
    return toml.dumps(registration_form)


def number_of_files():
    """Returns the number of files in the settings directory"""
    return len([f for f in os.listdir(SETTINGS_FILE_DIR) if os.path.isfile(os.path.join(SETTINGS_FILE_DIR, f))])


def write_settings_file(game_id: int, file_contents: str):
    """Writes the settings file to the settings directory"""
    with open(SETTINGS_FILE_DIR + "custom" + str(game_id) + '.ini', 'w') as f:
        f.write(file_contents)


def enforce_values(user_settings: FullSettings, enforced_settings = ENFORCED_VALUES) -> FullSettings:
    """Enforces the values in the registration form to the settings"""
    user_settings = initialize_settings(user_settings)
    return merge(user_settings.dict(), enforced_settings)


def set_ports(user_settings: FullSettings, rcon_port: int, server_port: int) -> FullSettings:
    """Sets the rcon_port and server_port in the user_settings"""
    user_settings['Rcon']['RconPort'] = rcon_port
    user_settings['Server']['Port'] = server_port
    return user_settings



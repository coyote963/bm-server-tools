import os

import toml
from mergedeep import merge

SETTINGS_FILE_DIR = '/home/coyote/files'

section_values = {
    'Server': [
        'Password',
        'MOTD',
        'Name',
        'MaxPlayers',
        'EnableSpec',
        'StrictSpec',
        'WarmUp',
        'GameMode',
        'Fiesta',
    ],
    'ServerMutators': [
        'AllWater',
        'Hazards',
    ]
}

forced_values = {
    'Server': {
        'DedicatedFPS': '30',
    },
    'Rcon': {
        'RconPort': '42070',
        'RconPassword': 'admin'
    }
}

def split_into_sections(reg_form):
    sectioned_config = {}
    for section, _ in section_values.items():
        sectioned_config[section] = {}
        for setting in section_values[section]:
            if setting in reg_form and reg_form[setting] != "":
                sectioned_config[section][setting] = reg_form[setting]
    return sectioned_config

def set_forced_values(config):
    return merge(config, forced_values)


def number_of_files_in_folder():
    allfiles = next(os.walk(SETTINGS_FILE_DIR))[2]
    return len(allfiles)


def create_new_settings_file(settings_string, settings_index):
    with open(f'{SETTINGS_FILE_DIR}/custom_{settings_index}.ini', 'w') as settings_file:
        settings_file.write(settings_string)


def create_ini(reg_form):
    x = split_into_sections(reg_form.to_dict())
    set_forced_values(x)
    config_id = number_of_files_in_folder()
    create_new_settings_file(
        toml.dumps(x),
        config_id)
    print(toml.dumps(x))
    return config_id 

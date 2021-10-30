# bm-server-tools
Provides useful wrapper for bman servers. The core of everything is the boring man linux docker image. Inside the image runs a flask server that can handle a user configured number of boring man servers. The bman linux image also runs VNC for remote management of servers. As well as tools to automatically check the health of the boring man servers and the ability to automatically stop unhealthy servers. Various tools for interfacing with the docker image are also available. 

## Installation
### Getting the docker image

Each tool has its own requirements and are kept separate for the sake of modularity. Only the TUI does not require docker to be installed. The others can be installed by use of the `requirements.txt` file. The most up to date docker image is `coyotebm/bm-server-api:dev`.

### CLI

Command line tools for provisioning servers. A sample of the commands:

1. `start` Starts the Boring Man Wrapper API
2. `stop` Stops Boring Man Wrapper API and all servers running therein
3. `add` Adds a server from a preset. Presets are configurable and defined in `presets.py`
4. `add-custom` Adds a server from a settings file path
5. `remove` Kills a server and frees its resources
6. `status` Displays server information in tabular form

#### Installation

1. Install docker, the way to do so varies between operating systems. 
2. Install the `requirements.txt`
3. Ensure the current user is in the docker group
4. `python cli.py start` to start the service


### TUI 

The TUI is a standalone program that creates a live dashboard of a boring man server. This is useful for viewing the current status of a match on the fly. Install the requirements file and run `python tui.py` to launch it.

## Usage 

The docker image will by default not launch any game servers. To get started make a POST request to the API running locally on 7778, with the keys being the boring man server setting name and the value being its value.

Making GET requests shows every running server
 
## Directory structure

```
src/
    container/ - Everything that runs inside a docker container
        server/ - Flask server files
            GameState - Base class for storing the current state of the servers
            SettingsModel - Class representing a Boring Man settings file
            app.py - Entry point of the flask app
            healthcheck.py - Tools for verifying the server is still running
            settings_file_utils - Utilities for manipulating settings files
        run.sh - Run the flask server locally
        ...
    tui/ - Standalone TUI rcon interface
        tui.py - TUI code
        game.py - RCOn connection
``` 

## Screenshots

Picture of the TUI capturing the Live Results of a match
![TUI screenshot](screenshots/tui.png?raw=true "Boring Man TUI")

![TUI screenshot](screenshots/schema.PNG?raw=true "Boring Man TUI")

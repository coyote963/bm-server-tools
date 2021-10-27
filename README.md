# bm-server-tools
Provides useful wrapper for bman servers. The core of everything is the boring man linux docker image. Inside the image runs a flask server that can handle a user configured number of boring man servers. The bman linux image also runs VNC for remote management of servers. As well as tools to automatically check the health of the boring man servers and the ability to automatically stop unhealthy servers. Various tools for interfacing with the docker image are also available. 

## Installation
### Getting the docker image

On distros that use apt as their package manager, run install_apt.sh, which will install the necessary dependencies. Build the docker image locally or just pull it from the docker hub.

If you just want to run the docker image just run `docker run -d -p <port-range>:<port-range> -p 6080:80 -p 7778:7778 bm-linux`


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

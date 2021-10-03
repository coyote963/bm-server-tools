# bm-server-tools
Provides useful wrapper for bman servers. The core of everything is the boring man linux docker image. Inside the image runs a flask server that can handle a user configured number of boring man servers. The bman linux image also runs VNC for remote management of servers. As well as tools to automatically check the health of the boring man servers and the ability to automatically stop unhealthy servers. Various tools for interfacing with the docker image are also available. 

## Installation
### Getting the docker image

On distros that use apt as their package manager, run install_apt.sh, which will install the necessary dependencies. Build the docker image locally or just pull it from the docker hub.

If you just want to run the docker image just run `docker run -d -p <port-range>:<port-range> -p 6080:80 -p 7778:7778 bm-linux`


### CLI 

Other interfacing tools like the CLI will need the docker container running or else they won't work. To install the CLI run `install.sh` in the /src/cli folder

## Usage 

The docker image will by default not launch any game servers. To get started make a POST request to the API running locally on 7778, with the keys being the boring man server setting name and the value being its value.

Making GET requests shows every running server
 
## Directory structure

```
src/
    container/ - Everything that runs inside a docker container
        app.py - Flask server
        Dockerfile - Used for building the bm-linux docker image
        GameState.py - Classes for organizing server state
        healthcheck.py - Intended to be run periodically on a server to check its status
        requirements.txt - Python dependencies
        run.sh - Entrypoint of the Docker image
        settings_file_utils.py - Utilities for manipulation of boring man settings files
        SettingsModel - Pydantic models for server settings
``` 
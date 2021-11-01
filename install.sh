#!/bin/bash

BASEPATH=$HOME


install_cli() {
  if [ ! -d ".cli_env" ]
  then
    echo "Installing cli dependencies"
    python3 -m venv .cli_env
    source .cli_env/bin/activate 
    pip3 install -r src/cli/requirements.txt
    source .cli_env/bin/deactivate
  else
    echo "CLI is already installed"
  fi
}

install_tui() {
  if [ ! -d ".tui_env" ]
  then
    echo "Installing TUI dependencies"
    python3 -m venv .tui_env
    source .tui_env/bin/activate 
    pip3 install -r src/tui/requirements.txt
    source .tui_env/bin/deactivate
  else
    echo "TUI is already installed"
  fi
}

install_docker() {
  curl -fsSL get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
}


if [ $1 == "nothing" ]; then
  echo "Done"
  exit
fi

if [ $1 == "cli"]; then
  install_cli
  exit
fi

if [ $1 == "tui"]; then
  install_tui
  exit 
fi

if [ $1 == "docker" ]; then
  install_docker
  exit
fi

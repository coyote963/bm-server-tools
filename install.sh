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

echo "Do you wish to install docker? [1-2]"
select yn in "Yes" "No"; do
  case $yn in
  Yes)
    install_docker
    break
    ;;
  No) break ;;
  esac
  echo "Not a valid choice [1, 2]"
done

echo "Which component do you want to install? [1-4]"
select opt in "CLI" "TUI" "ALL" "NONE"; do
  case $opt in
  CLI)
    install_cli
    break
    ;;
  TUI)
    install_tui
    break
    ;;
  ALL)
    install_cli
    install_tui
    break
    ;;
  NONE) break ;;
  esac
  echo "Not a valid choice [1, 2, 3, 4]"
done


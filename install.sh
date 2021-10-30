#!/bin/bash

BASEPATH=$HOME
CONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

install_miniconda() {
  curl -k $CONDA_URL >${BASEPATH}/conda_install.sh
  bash ${BASEPATH}/conda_install.sh -b -p ${BASEPATH}/Miniconda3
  rm -f ${BASEPATH}/conda_install.sh
  $BASEPATH/miniconda3/bin/conda update -y -n base -c defaults conda
}

install_tui() {
  $BASEPATH/miniconda3/bin/conda create -y -n bm-tui python=3.7
  source $BASEPATH/miniconda3/bin/activate bm-tui
  conda install --file ./src/tui/requirements.txt
}

install_cli() {
  $BASEPATH/miniconda3/bin/conda create -y -n bm-cli python=3.7
  source $BASEPATH/miniconda3/bin/activate bm-cli
  conda install --file ./src/cli/requirements.txt
}

if [[! -d "$BASEPATH/miniconda3" ]]; then
  install_miniconda
fi

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

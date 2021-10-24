
echo "(Re)install docker? Choose yes if unsure. (y/n):"



install_docker() {
  sudo apt-get remove docker docker-engine docker.io containerd-runc
  sudo apt-get update
  sudo apt-get install \
      ca-certificates \
      curl \
      gnupg \
      lsb-release
  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io
}

install_dependencies() {
  echo "Installing dependencies"
}


while true; do
  read -p "Do you wish to install this docker? Choose yes if unsure (y/n): " yn
  case $yn in
    [Yy]* ) install_docker; break;;
    [Nn]* ) break;;
    * ) echo "Please answer y or n.";;
  esac
done

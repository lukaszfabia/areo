#!/bin/bash

# Remember to run in before we run project

if [ "$(id -u)" -ne 0 ]; then
  echo "Add user to sudoers here: /etc/sudoers or run: sudo -i and then usermod -aG wheel <user> and uncomment line with wheel"
  exit 1
fi

sudo apt update

sudo apt install tmux docker docker-compose

sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl status docker

sudo usermode -aG docker $USER

result=$(groups $USER | grep "docker")

if [[ -n "$result" ]]; then
  echo -e "Successfully added $USER to docker.\n Rebooting..."
  sudo reboot
else
  echo "Failed to add $USER to docker. Try do it manually."
fi

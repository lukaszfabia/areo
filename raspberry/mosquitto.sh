#!/bin/bash

export DISPLAY=:0.0

sudo apt update
sudo apt install mosquitto mosquitto-clients

# sprawdznie statusu komara
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service
sudo systemctl status mosquitto.service

sudo bash -c 'echo "allow_anonymous true" >> /etc/mosquitto/mosquitto.conf'
sudo bash -c 'echo "listener 1883 0.0.0.0" >> /etc/mosquitto/mosquitto.conf'
sudo systemctl restart mosquitto.service

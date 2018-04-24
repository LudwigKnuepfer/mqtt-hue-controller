# mqtt-hue-controller

This is  a python script that subscribes to MQTT and controls a Philipps Hue Bridge depending on what is published

# Installation

Assuming you're on a raspberry pi running the latest (as of this time) raspbian distribution (Debian 9.4):
```sh
sudo mkdir /etc/mqtt_hue_controller
sudo cp config.ini /etc/mqtt_hue_controller/
sudo vim /etc/mqtt_hue_controller/config.ini # adjust to your needs
sudo cp mqtt-hue-controller.py /usr/local/bin/mqtt_hue_controller
sudo cp mqtt-hue-controller.service /lib/systemd/system/
sudo systemctl enable mqtt-hue-controller.service
sudo systemctl start mqtt-hue-controller.service
```

# Installing Prerequisits

```sh
sudo pip3 install paho-mqtt
sudo pip3 install phue
```

# Caveats

There is no support for an automatic registration procedure nor bridge discovery at this point.
You could use phue to do register and copy out the id from the config file phue creates.

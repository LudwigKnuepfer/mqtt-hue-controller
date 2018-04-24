#!/usr/bin/env python3

import os
import sys
import time

import configparser

import paho.mqtt.client as mqtt

from phue import Bridge

CONFIG = None
BRIDGE = None

def LOG(msg):
    print(msg)

def handle_config_entry(entry):
    if 'light' in entry:
        if 'bri' in entry:
            BRIDGE.set_light(entry['light'], 'bri', int(entry['bri']))
        if 'on' in entry:
            BRIDGE.set_light(entry['light'], 'on', entry.getboolean('on'))
        LOG("set %s" % entry['light'])

def mqtt_on_message(client, userdata, msg):
    global CONFIG

    topic = msg.topic
    payload = msg.payload.decode()
    LOG("mqtt got message: %s: %s" % (topic, payload))

    if payload in CONFIG:
        handle_config_entry(CONFIG[payload])
    else:
        LOG("no action associated with this payload")

def mqtt_on_connect(client, userdata, flags, rc):
    global CONFIG
    if rc == 0:
        LOG("mqtt connected")

        for topic in CONFIG['MQTT']['event_topics'].split():
            client.subscribe(topic, qos=0)

        client.publish(
                CONFIG['MQTT']['status_topic'], "hue-controller up and running", qos=0, retain=True)
    else:
        LOG("mqtt connection failed")
        sys.exit(1)

def mqtt_init():
    global CONFIG
    protocol = mqtt.MQTTv311
    if 'protocol' in CONFIG['MQTT']:
        pass

    client_id = CONFIG['MQTT'].get('client_id', 'hue-controller')

    client = mqtt.Client(
            client_id=client_id, clean_session=False, protocol=protocol)

    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message

    return client

def bridge_init():
    global CONFIG
    global BRIDGE

    BRIDGE = Bridge(ip=CONFIG['Hue']['host'], username=CONFIG['Hue']['key'])
    BRIDGE.connect()

def main():
    global CONFIG
    config = configparser.ConfigParser()
    config.read('/etc/mqtt_hue_controller/config.ini')
    CONFIG = config

    client = mqtt_init()
    try:
        client.connect(
                CONFIG['MQTT']['host'],
                int(CONFIG['MQTT']['port']),
                60)
    except socket.error as err:
        LOG(err)
        sys.exit(1)

    bridge_init()

    client.loop_start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        LOG("KeyboardInterrupt")
    finally:
        client.publish(
                CONFIG['MQTT']['status_topic'], "hue-controller dead", qos=0, retain=True)
        time.sleep(0.1)
        client.disconnect()

    sys.exit(0)

if __name__ == "__main__":
    main()

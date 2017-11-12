'''
Created on 7. nov. 2017

@author: Andersen
'''

import paho.mqtt.client as mqtt
import os
import time
from urllib.parse import urlparse
from paho.mqtt import publish
from local.topic import gettopic, gettimediff
import threading

class Client(object):
    '''
    classdocs
    '''


    def __init__(self, cid, on_message, url):
        '''
        Constructor
        '''
        self.mqttc = mqtt.Client()
        
        url_str = os.environ.get(url, 'mqtt://localhost:1883')
        url = urlparse(url_str)
        #self.mqttc.username_pw_set(url.username, url.password)
        self.hostname = url.hostname
        self.port = url.port
        self.id = cid
        
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_message = on_message
        #self.mqttc.on_log = self.on_log
        
    def connect(self):
        self.mqttc.connect(self.hostname, self.port)
    
    def disconnect(self):
        self.mqttc.disconnect()
    
    def subscribe(self, topic, qos=0):
        self.mqttc.subscribe(topic, qos)
        
    def publish(self, topic, message, qos=0):
        self.mqttc.publish(topic, message, qos)
        
    def produce(self, msgnr, ival, topic, qos, psize):
        
        self.t = threading.Thread(target=self.producefunc, args=(msgnr, ival, topic, qos, psize))
        self.t.start() 
    
    def producefunc(self, msgnr, ival, topic, qos, psize):
        self.mqttc.loop_start()
        for i in range(msgnr):
            self.publish(topic, gettopic(i, psize), qos)
            time.sleep(ival)
        self.mqttc.loop_stop()
        self.disconnect()
    
    def consume(self, ival, topic, qos):
        self.t = threading.Thread(target=self.consumefunc, args=(ival, topic, qos))
        self.t.start();
    
    def consumefunc(self, ival, topic, qos):
        self.mqttc.subscribe(topic, qos)
        self.mqttc.loop_start()
        
        while True:
            time.sleep(ival)
        
        self.mqttc.loop_stop()
        self.disconnect()
    '''
    Callbacks
    '''
    def on_disconnect(self, client, userdata, rc):
        print(self.id + 'disconnected with the result code ' + mqtt.connack_string(rc))
        self.mqttc.loop_stop()
        
    def on_connect(self, client, userdata, flags, rc):
        print(self.id + ' Connected with the result code '+mqtt.connack_string(rc))
        self.mqttc.loop_start()
    
    def on_log(self, client, obj, level, string):
        print(string)
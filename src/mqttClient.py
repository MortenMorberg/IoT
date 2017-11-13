'''
Created on 7. nov. 2017

@author: Andersen
'''

import paho.mqtt.client as mqtt
from IClient import IClient
import os
import time
from urllib.parse import urlparse
from paho.mqtt import publish
from topic import gettopic, gettimediff
import threading

class mqttClient(IClient):
    '''
    classdocs
    '''

    def __init__(self, cid, url):
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
        #self.mqttc.on_log = self.on_log
        
    def connect(self):
        self.mqttc.connect(self.hostname, self.port)
    
    def disconnect(self):
        self.mqttc.disconnect()
    
	# self, topic={'topic':'', 'qos':''} kwargs = {'timeout':'', 'cb':''}
    def subscribe(self, topic, kwargs):
        self.mqttc.on_message = topic['cb']
        self.t = threading.Thread(target=self.subscribefunc, args=(topic, kwargs))
        self.t.start();
	
	# self, topic={'topic':'', 'psize':'', 'qos':''} kwargs = {'nr':'', 'ival':''}
    def publish(self, topic, kwargs):
        self.t = threading.Thread(target=self.publishfunc, args=(topic, kwargs))
        self.t.start() 
    
	# self, topic={'topic':'', 'psize':'', 'qos':''} kwargs = {'nr':'', 'ival':''}
    def publishfunc(self, topic, kwargs):
        self.mqttc.loop_start()
        for i in range(kwargs['nr']):
            self.mqttc.publish(topic['topic'], gettopic(i, topic['psize']), topic['qos'])
            time.sleep(kwargs['ival'])
        self.mqttc.loop_stop()
        self.disconnect()
    
	# self, topic={'topic':'', 'qos':''} kwargs = {'timeout':'', 'cb':''}
    def subscribefunc(self, topic, kwargs):
        self.mqttc.subscribe(topic['topic'], topic['qos'])
        self.mqttc.loop_start()
        
        time.sleep(kwargs['timeout'])
        
        self.mqttc.loop_stop()
        self.disconnect()
        
    def waitForClient(self):
        self.t.join()
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
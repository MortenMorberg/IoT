import numpy as np
from amqpClient import amqpClient
from mqttClient import mqttClient
import matplotlib.pyplot as plt
from csv_helper import write_to_csv
#import resource

import time
from topic import *

timevals = []

def callback(ch, method, properties, body):
    topic = body.decode('utf-8')
    timediff = gettimediff(topic, time.time())
    timevals.append(timediff)
    print('MsgID: {0} Time difference between sent and received: {1}' \
                                    .format(getMsgId(topic), timediff))
                                   
def on_message(client, userdata, msg):
    timediff = gettimediff(msg.payload, time.time())
    timevals.append(timediff)
    print("Topic: "+msg.topic+" DeviceId: "+str(getDeviceId(msg.payload))+" MsgId: "+ str(getMsgId(msg.payload))+" Time: "+str(timediff))

def var_sub_test(broker, url, nr_pub, nr_con ):
    if( broker == 'mqtt' or broker == 'amqp' ):
        p_clients = []
        s_clients = []
        for c in range(0, nr_pub + nr_con):
            client = None
            topic = None
            kwargs = None

            if( broker == 'mqtt' ):
                client = mqttClient(c, url)
                topic = {'topic': 'x', 'psize': 1, 'qos':0 }
                kwargs_p = {'nr':1, 'ival':1}
                msg_s = {'topic':'x', 'qos':0, 'cb':on_message}
                kwargs_s = {'timeout' : 10}
            else:
                client = amqpClient(c, url)
                topic = [ {'exchange': 'x', 'routing_key': '', 'psize': 1 } ]
                kwargs_p = {'nr': 1, 'ival': 1}
                msg_s = {'exchange': 'x', 'cb': callback, 'no_ack': True}
                kwargs_s = {'timeout' : 10}

            if( c < nr_pub ):
                p_clients.append(client)
            else:
                s_clients.append(client)
            client.connect()

        for s in s_clients:
            s.subscribe(msg_s, kwargs_s)
        if(broker  == 'amqp'):
            for s in s_clients:
                s.start_subscribe_timeout(kwargs_s) 
        time.sleep(1)
        for p in p_clients:
            p.publish(topic, kwargs_p)

        ## wait until they are terminated, make sure to disconnect so that connections at the host are freed
        for s in s_clients:
            s.waitForClient()

        for p in p_clients:
            p.waitForClient()

    return np.median(timevals), np.mean(timevals), np.var(timevals), len(timevals)

if __name__=="__main__":

    # protocol name
    proto = 'amqp'
    
    # url
    url = 'amqp://iotgroup4:iot4@2.104.13.126:5672'
    
    time_med, time_mean, time_var, msg_nr = var_sub_test(proto, url, 1, 300)
    
    print(msg_nr)
'''
if __name__=="__main__":
    #resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

    #minimum number of subscribers
    sub_min = 1
    
    #maximum number of subscribers
    sub_max = 10
    
    # number of intervals
    sub_nr = 2
    
    #repetition number
    rep_nr = 1
    
    # protocol name
    proto = 'mqtt'
    
    # url
    url = 'amqp://iotgroup4:iot4@2.104.13.126:5672'
    
    sub_ival = int((sub_max-sub_min)/(sub_nr-1))
    sub_vars = []
    sub_med = []
    sub_mean = []
    sub_xval = range(sub_min, sub_max+1, sub_ival)
    
    med_mat = []
    mean_mat = []
    var_mat = []
    for i in range(0,rep_nr):
        med_vec  = []
        mean_vec = []
        var_vec  = []
        for j in sub_xval:
            print(j)
            timevals = []
            time_med, time_mean, time_var = var_sub_test(proto, url, 1, j)
            med_vec.append(time_med)
            mean_vec.append(time_mean)
            var_vec.append(time_var)
        med_mat.append(med_vec)
        mean_mat.append(mean_vec)
        var_mat.append(var_vec)
        
    for i in range(0,len(sub_xval)):
        med = np.median([row[i] for row in med_mat])
        mean = np.median([row[i] for row in mean_mat])
        var = np.median([row[i] for row in var_mat])
        sub_med.append(med)
        sub_mean.append(mean)
        sub_vars.append(var)
    
    write_to_csv(sub_xval, sub_med,  '../csv/' + proto + '_var_sub_test_med',  proto + '_var_sub_test_med')
    write_to_csv(sub_xval, sub_mean, '../csv/' + proto + '_var_sub_test_mean', proto + '_var_sub_test_mean')
    write_to_csv(sub_xval, sub_vars,  '../csv/' + proto + '_var_sub_test_var',  proto + '_var_sub_test_var')
     '''       
import numpy as np
from amqpClient import amqpClient
from mqttClient import mqttClient
import matplotlib.pyplot as plt
from csv_helper import write_to_csv

import time
from topic import *

timevals = []

def callback(ch, method, properties, body):
    topic = body.decode('utf-8')
    timediff = gettimediff(topic, time.time())
    timevals.append(timediff)
    print('\nMsgID: {0} \nTime difference between sent and received: {1}\n' \
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
                kwargs_s = {'timeout' : 30}
            else:
                client = amqpClient(c, url)
                topic = [ {'exchange': 'x', 'routing_key': '', 'psize': 1 } ]
                kwargs_p = {'nr': 1, 'ival': 1}
                msg_s = {'exchange': 'x', 'cb': callback, 'no_ack': True}
                kwargs_s = {'timeout' : 30}

            if( c < nr_pub ):
                p_clients.append(client)
            else:
                s_clients.append(client)
            client.connect()

        for s in s_clients:
            s.subscribe(msg_s, kwargs_s)
        time.sleep(1)
        for p in p_clients:
            p.publish(topic, kwargs_p)

        ## wait until they are terminated, make sure to disconnect so that connections at the host are freed
        for s in s_clients:
            s.waitForClient()

        for p in p_clients:
            p.waitForClient()

    return np.median(timevals), np.mean(timevals), np.var(timevals)


if __name__=="__main__":
        
    pub_min = 1
    pub_max = 10
    pub_nr = 2
    rep_nr = 2
    proto = 'mqtt'
    url = 'amqp://iotgroup4:iot4@2.104.13.126:5672'
    
    pub_ival = int((pub_max-pub_min)/(pub_nr-1))
    pub_vars = []
    pub_med = []
    pub_mean = []
    pub_xval = range(pub_min, pub_max+1, pub_ival)
    
    med_mat = []
    mean_mat = []
    var_mat = []
    for i in range(0,rep_nr):
        med_vec  = []
        mean_vec = []
        var_vec  = []
        for j in pub_xval:
            print(j)
            timevals = []
            time_med, time_mean, time_var = var_sub_test(proto, url, 1, j)
            med_vec.append(time_med)
            mean_vec.append(time_mean)
            var_vec.append(time_var)
        med_mat.append(med_vec)
        print(med_mat)
        mean_mat.append(mean_vec)
        print(mean_mat)
        var_mat.append(var_vec)
        print(var_mat)
    
    for i in range(0,rep_nr):
        med = np.median([row[i] for row in med_mat])
        mean = np.median([row[i] for row in mean_mat])
        var = np.median([row[i] for row in var_mat])
        pub_med.append(med)
        pub_mean.append(mean)
        pub_vars.append(var)
    
    write_to_csv(pub_xval, pub_med,  '../csv/' + proto + '_var_sub_test_med',  proto + '_var_sub_test_med')
    write_to_csv(pub_xval, pub_mean, '../csv/' + proto + '_var_sub_test_mean', proto + '_var_sub_test_mean')
    write_to_csv(pub_xval, pub_vars,  '../csv/' + proto + '_var_sub_test_var',  proto + '_var_sub_test_var')
            
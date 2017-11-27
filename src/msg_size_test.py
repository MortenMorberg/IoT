import numpy as np
from amqpClient import amqpClient
from mqttClient import mqttClient
import matplotlib.pyplot as plt

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


def msg_size_test(broker, url, psize):
    if( broker == 'mqtt' or broker == 'amqp' ):
        p_client = None
        s_client = None
        if( broker == 'mqtt' ):
            p_client = mqttClient(1, url)
            s_client = mqttClient(2, url)
            topic = {'topic': 'x', 'psize': psize, 'qos':0 }
            kwargs_p = {'nr':10, 'ival':1}
            msg_s = {'topic':'x', 'qos':0, 'cb':on_message}
            kwargs_s = {'timeout' : 20}
        else:
            p_client = amqpClient(c, url)
            s_client = amqpClient(c, url)
            topic = [ {'exchange': 'x', 'routing_key': '', 'psize': 1 } ]
            kwargs_p = {'nr': 1, 'ival': 2}
            msg_s = {'exchange': 'x', 'cb': callback, 'no_ack': True}
            kwargs_s = {'timeout' : 30}
            
        p_client.connect()
        s_client.connect()

        s_client.subscribe(msg_s, kwargs_s)
        time.sleep(1)
        p_client.publish(topic, kwargs_p)

        ## wait until they are terminated, make sure to disconnect so that connections at the host are freed
        s_client.waitForClient()
        p_client.waitForClient()
        
    return np.median(timevals), np.mean(timevals), np.var(timevals)


if __name__=="__main__":
    times = []
    psize = []
    for i in range(0, 1000001, 100000):
        timevals = []
        time_med, time_mean, time_var = msg_size_test('mqtt', 'amqp://iotgroup4:iot4@192.168.0.3:5672', i)
        times.append(time_med)
        psize.append(i)

    plt.plot(psize, times)
    plt.title('Consumer, median time')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Time (median)')
    plt.show()
    plt.savefig('pubVScon')

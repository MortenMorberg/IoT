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
    #print("Topic: "+msg.topic+" DeviceId: "+str(getDeviceId(msg.payload))+" MsgId: "+ str(getMsgId(msg.payload))+" Time: "+str(timediff))

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
                kwargs_p = {'nr': 1, 'ival': 2}
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
    var = []
    pubs = []
    idx = 401
    for i in range(1, idx, 50):
        vars = []
        print(i)
        for j in range(1, 10):
            time_med, time_mean, time_var = var_sub_test('mqtt', 'amqp://iotgroup4:iot4@192.168.0.3:5672', 1, i)
            vars.append(time_var)
        var.append(np.median(vars))
        pubs.append(i)
    plt.plot(pubs, var)
    plt.title('Consumer variance')
    plt.ylabel('Latency variance')
    plt.xlabel('Consumers')
    plt.show()
    plt.savefig('pubVScon')
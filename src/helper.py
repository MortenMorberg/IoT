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

def pub_sub_test(broker, url, nr_pub, nr_con ):
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
                kwargs_p = {'nr':10, 'ival':0.1}
                msg_s = {'topic':'x', 'qos':0, 'cb':on_message}
                kwargs_s = {'timeout' : 30}
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

        for p in p_clients:
            p.publish(topic, kwargs_p)

        ## wait until they are terminated, make sure to disconnect so that connections at the host are freed
        for s in s_clients:
            s.waitForClient()
            s.disconnect()

        for p in p_clients:
            p.waitForClient()
            p.disconnect()

    return np.median(timevals), nr_pub-nr_con


if __name__=="__main__":
    times = []
    ratios = []
    idx = 100
    for i in range(1, idx):
        timeval, ratioval = pub_sub_test('amqp', 'amqp://iotgroup4:iot4@192.168.0.7:5672', i, idx - i)
        times.append(timeval)
        ratios.append(ratioval)

    plt.plot(ratios, times)
    plt.title('Pub vs con, median time')
    plt.xlabel('Publishers/Consumers (ratio)')
    plt.ylabel('Time (median)')
    plt.show()
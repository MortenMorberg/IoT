import sys
from amqpClient import amqpClient
from mqttClient import mqttClient

import time
from topic import *

def callback(ch, method, properties, body):
    topic = body.decode('utf-8')
    print('\nMsgID: {0} \nTime difference between sent and received: {1}\n' \
                                    .format(getMsgId(topic), gettimediff(topic, time.time())))

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

        for s in s_clients:
            s.waitForClient()

        for p in p_clients:
            p.waitForClient()
        
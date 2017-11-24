import numpy as np
import sys
from amqpClient import amqpClient
from mqttClient import mqttClient
import matplotlib.pyplot as plt

import time
from topic import *

timevals = []
recv_msgs = 0

def callback_pub_sub_test(ch, method, properties, body):
    topic = body.decode('utf-8')
    timediff = gettimediff(topic, time.time())
    timevals.append(timediff)
    print('MsgID: {0} Time difference: {1}' \
                                    .format(getMsgId(topic), timediff))

def callback_msg_interval(ch, method, properties, body):
    topic = body.decode('utf-8')
    timediff = gettimediff(topic, time.time())
    timevals.append(timediff)
    global recv_msgs
    recv_msgs += 1

    print('\nMsgID: {0} \nTime difference between sent and received: {1}\n' \
                                    .format(getMsgId(topic), timediff))

def pub_sub_run(broker, url, nr_pub, nr_con, call_back, interval=1 ):
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
                kwargs_p = {'nr':10, 'ival': interval}
                msg_s = {'topic':'x', 'qos':0, 'cb':call_back}
                kwargs_s = {'timeout' : 30}
            else:
                client = amqpClient(c, 'amqp://{0}'.format(url))
                topic = [ {'exchange': 'x', 'routing_key': '', 'psize': 1 } ]
                kwargs_p = {'nr': 1, 'ival': interval}
                msg_s = {'exchange': 'x', 'cb': call_back, 'no_ack': True}
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

    return np.median(timevals), nr_pub-nr_con

def pub_sub_test():
    times = []
    ratios = []
    idx = 10
    for i in range(1, idx):
        timevals = []
        timeval, ratioval = pub_sub_run('amqp', 'iotgroup4:iot4@2.104.13.126:5672', i, idx - i, callback_pub_sub_test)
        times.append(timeval)
        ratios.append(ratioval)

    plt.plot(ratios, times)
    plt.title('Pub vs con, median time')
    plt.xlabel('Publishers/Consumers (ratio)')
    plt.ylabel('Time (median)')
    plt.show()

def msg_interval_test():
    print('here')
    y_packetloss = []
    x_msg_s = []
    broker = 'amqp'
    url = 'iotgroup4:iot4@localhost:5672'
    interval = 0.1
    idx = 20
    for i in range(10, idx, 10):
        global recv_msgs
        recv_msgs = 0
        timevals = []
        if( broker == 'mqtt' or broker == 'amqp' ):
            p_clients = []
            s_client = None

            for i in range(idx + 1):
                client = None
                topic = None
                kwargs = None

                if( broker == 'mqtt' ):
                    client = mqttClient(i, url)
                    topic = {'topic': 'x', 'psize': 1, 'qos':0 }
                    kwargs_p = {'nr':10, 'ival': interval}
                    msg_s = {'topic':'x', 'qos':0, 'cb': callback_msg_interval}
                    kwargs_s = {'timeout' : 30}
                else:
                    client = amqpClient(i, 'amqp://{0}'.format(url))
                    topic = [ {'exchange': 'x', 'routing_key': '', 'psize': 1 } ]
                    kwargs_p = {'nr': 10, 'ival': interval}
                    msg_s = {'exchange': 'x', 'cb': callback_msg_interval, 'no_ack': True}
                    kwargs_s = {'timeout' : 30}

                if( i < idx ):
                    p_clients.append(client)
                else:
                    s_client = client
                client.connect()

            s_client.subscribe(msg_s, kwargs_s)

            time.sleep(1)

            for p in p_clients:
                p.publish(topic, kwargs_p)

            ## wait until they are terminated, make sure to disconnect so that connections at the host are freed
            s_client.waitForClient()

            for p in p_clients:
                p.waitForClient()

            sent_msgs = 10 * idx
            x_msg_s.append(idx * interval)
            y_packetloss.append(sent_msgs - recv_msgs)
            print(sent_msgs)
            print(recv_msgs)

    plt.plot(x_msg_s, y_packetloss)
    plt.title('Packet loss test')
    plt.xlabel('Messages/s')
    plt.ylabel('Packets lost')
    plt.show()

if __name__=="__main__":
    case = None
    if( len(sys.argv) < 2 ):
        print('No inline args! Specify case')
        sys.exit()
    
    case = sys.argv[1]

    print(case)
    if( case  == 'pub-sub-test'):
        print('Running pub-sub-test')
        pub_sub_test()

    elif( case == 'msg-interval-test' ):
        print('Running msg-interval-test')
        msg_interval_test()
    else:
        print('Exit')
        sys.exit()
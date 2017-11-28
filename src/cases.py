import numpy as np
import sys
from amqpClient import amqpClient
from mqttClient import mqttClient
import matplotlib.pyplot as plt
from csv_helper import read_from_csv, write_to_csv

import time
from topic import *

timevals = []
recv_msgs = 0

def callback_pub_sub_test(ch, method, properties, body):
    global timevals
    topic = body.decode('utf-8')
    timediff = gettimediff(topic, time.time())
    timevals.append(timediff)
    #print('MsgID: {0} Time difference: {1}' .format(getMsgId(topic), timediff))

def callback_msg_interval(ch, method, properties, body):
    global recv_msgs, timevals
    topic = body.decode('utf-8')
    timediff = gettimediff(topic, time.time())
    timevals.append(timediff)
    recv_msgs += 1
    #print('MsgID: {0} Time difference: {1}' .format(getMsgId(topic), timediff))

def pub_sub_run(broker, url, nr_pub, nr_con, call_back, interval=1 ):
    if( broker == 'mqtt' or broker == 'amqp' ):
        p_clients = []
        s_clients = []
        pubs = 0
        subs = 0
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
                msg_s = {'exchange': 'x', 'cb': call_back, 'no_ack': True, 'auto_delete': True}
                kwargs_s = {'timeout' : 30}

            if( c < nr_pub ):
                p_clients.append(client)
                pubs += 1
            else:
                s_clients.append(client)
                subs += 1
            client.connect()
            
        print('Publishers: {0} Subscribers: {1}' .format( pubs, subs ))

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

def pub_sub_test(broker, url, fileName, iterations=1, stepsize=1, showplot=False):
    times = []
    ratios = []
    for i in range(1, iterations):
        timeval, ratioval = pub_sub_run(broker, url, i, iterations - i, callback_pub_sub_test, interval=stepsize)
        times.append(timeval)
        ratios.append(ratioval)

    write_to_csv(ratios, times, '../csv/{0}'.format(fileName))

    if( showplot ):
        x, y = read_from_csv('../csv/{0}'.format(fileName))
        plt.plot(x, y)
        plt.title('Pub vs con, median time')
        plt.xlabel('Publishers/Consumers (ratio)')
        plt.ylabel('Time (median)')
        plt.show()

def msg_interval_test(broker, url, fileName, iterations=1, stepsize=1, interval=0.01, showplot=False):
    y_packetloss = []
    x_msg_s = []
    
    y_times = []

    interval = 0.1
    for i in range(10, iterations + 1, stepsize):
        global recv_msgs, timevals
        recv_msgs = 0
        timevals = []
        p_clients = []
        s_client = None
        
        if( broker == 'mqtt' or broker == 'amqp' ):
            client = None
            topic = None
            kwargs = None

            subs = 0
            pubs = 0
            for j in range(i + 1):
                if( broker == 'mqtt' ):
                    client = mqttClient(j, url)
                    topic = {'topic': 'x', 'psize': 1, 'qos':0 }
                    kwargs_p = {'nr':10, 'ival': interval}
                    msg_s = {'topic':'x', 'qos':0, 'cb': callback_msg_interval}
                    kwargs_s = {'timeout' : 30}
                else:
                    client = amqpClient(j, 'amqp://{0}'.format(url))
                    topic = [ {'exchange': 'x', 'routing_key': '', 'psize': 1 } ]
                    kwargs_p = {'nr': 10, 'ival': interval}
                    msg_s = {'exchange': 'x', 'cb': callback_msg_interval, 'no_ack': True, 'auto_delete': True}
                    kwargs_s = {'timeout' : 30}
                
                if( j < i ):
                    p_clients.append(client)    
                    pubs += 1
                else:
                    s_client = client
                    subs += 1
                client.connect()

            print('Publishers: {0} Subscribers: {1}' .format( pubs, subs ))
            s_client.subscribe(msg_s, kwargs_s)

            time.sleep(1)

            for p in p_clients:
                p.publish(topic, kwargs_p)

            ## wait until they are terminated, make sure to disconnect so that connections at the host are freed
            s_client.waitForClient()

            for p in p_clients:
                p.waitForClient()

            sent_msgs = 10 * i

            x_msg_s.append(i * interval)
            y_packetloss.append(sent_msgs - recv_msgs)

            y_times.append(np.median(timevals))

    write_to_csv(x_msg_s, y_packetloss, '../csv/{0}'.format(fileName[0]), 'test')
    write_to_csv(x_msg_s, y_times, '../csv/{0}'.format(fileName[1]), 'test2')

    if( showplot ):
        x_1, y_1 = read_from_csv('../csv/{0}'.format(fileName[0]))
        plt.plot(x_1, y_1)
        plt.title('Packet loss test')
        plt.xlabel('Messages/s')
        plt.ylabel('Packets lost')
        plt.show()

        x_2, y_2 = read_from_csv('../csv/{0}'.format(fileName[1]))
        plt.plot(x_2, y_2)
        plt.title('Packet loss test')
        plt.xlabel('Messages/s')
        plt.ylabel('Median receive times')
        plt.show()


if __name__=="__main__":
    case = None
    if( len(sys.argv) < 2 ):
        print('No inline args! Specify case')
        sys.exit()
    
    case = sys.argv[1]
    if( case  == 'pub-sub-test'):
        print('Running pub-sub-test')
        pub_sub_test(broker='amqp', url='iotgroup4:iot4@2.104.13.126:5672', iterations=50, stepsize=1, fileName='pubSubRatioTest', showplot=True)

    elif( case == 'msg-interval-test' ):
        print('Running msg-interval-test')
        msg_interval_test(broker='amqp', url='iotgroup4:iot4@2.104.13.126:5672', iterations=20, stepsize=10, interval=0.1, fileName=['msgIntervalTest', 'msgTimeTest'], showplot=True)

    elif( case == 'all'):
        msg_interval_test(broker='amqp', url='iotgroup4:iot4@2.104.13.126:5672', iterations=50, stepsize=10, interval=0.1, fileName='msgIntervalLongTest')
        pub_sub_test(broker='amqp', url='iotgroup4:iot4@2.104.13.126:5672', iterations=50, stepsize=1, fileName='pubSubRatioLongTest')

    else:
        print('Exit')
        sys.exit()

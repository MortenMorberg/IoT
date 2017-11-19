import sys
from amqpClient import amqpClient
from mqttClient import mqttClient

import datetime
import time

def get_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def callback(ch, method, properties, body):
    print('Message received: {0} \nMessage sent: {1}\n\n' .format(get_timestamp(), body.decode('utf-8')))

if __name__=="__main__":
    arg = sys.argv[1:][0]  #mqtt or amqp
    nbr_publishers = int(sys.argv[2:][0]) #publishers
    nbr_consumers = int(sys.argv[2:][1]) #consumers
    url = 'amqp://bbjpgbhk:g460d0kQW8VRZA7KlLQ6uC4-Mxd_yG3e@golden-kangaroo.rmq.cloudamqp.com/bbjpgbhk'

    print(arg)

    if( arg == [] and nbr_publishers+nbr_consumers < 0):
        print('No inline args! Use -mqtt or -amqp and nbr of consumers and publishers')
        sys.exit()
    if( arg == '-mqtt'):
        print('Using mqtt')
    elif( arg == '-amqp' ):
        print('Using amqp')
    else:
        sys.exit()

    if( arg == '-mqtt' or arg == '-amqp' ):
        p_clients = []
        s_clients = []
        for c in range(0, nbr_publishers + nbr_consumers):
            client = None
            topic = None
            kwargs = None

            if( arg == '-mqtt' ):
                client = mqttClient(c, url)
            else:
                client = amqpClient(c, url)
                topic = [ {'exchange': 'x', 'routing_key': '', 'body': '3' } ]
                kwargs_p = {'nr': 3, 'ival': 10}
                msg_s = {'exchange': 'x', 'cb': callback, 'no_ack': True}
                kwargs_s = {'timeout' : 30}

            if( c < nbr_publishers ):
                p_clients.append(client)
            else:
                s_clients.append(client)
            client.connect()

        for p in p_clients:
            p.publish(topic, kwargs_p)

        for s in s_clients:
            s.subscribe(msg_s, kwargs_s)

        while(True): #waiting for last msg
            time.sleep(1)
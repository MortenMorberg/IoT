import sys
from amqpClient import amqpClient
from mqttClient import mqttClient

if __name__=="__main__":
    arg = sys.argv[1:]  #mqtt or amqp
    nbr_publishers = sys.argv[2:] #publishers
    nbr_consumers = sys.argv[3:] #consumers

    print(sys.argv)
    
    url = 'amqp://bbjpgbhk:g46d0kQW8VRZA7KlLQ6uC4-Mxd_yG3e@golden-kangaroo.rmq.cloudamqp.com/bbjpgbhk'
    
    if( arg == [] ):
        print('No inline args! Use -mqtt or -amqp')
        sys.exit())
    
    if( arg == ['-mqtt'] ):
        print('Using mqtt')

    if( arg == ['-amqp'] ):
        print('Using amqp')

    if( arg == ['-mqtt'] or arg == ['amqp'] ):
        p_clients = []
        s_clients = []
        for c in range(0, nbr_publishers + nbr_consumers):
            client = None
            if( arg == ['-mqtt'] ):
                client = mqttClient(p, url)
            else:
                client = amqpClient(p, url)
            
            if( c < nbr_publishers ):
                p_clients.append(client)
            else:
                s_clients.append(client)
            client.connect()

        for p in p_clients:
            p.publish()

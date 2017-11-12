from IClient import IClient
from threading import Thread
import time
import pika

class amqpClient(IClient):

    def __init__(self, amqp_url):
        self.connection = None
        self.pChannel = None
        self.pThread = None
        self.sChannel = None
        self.sQueuename = None
        self.params = None
        self.url = amqp_url

    def connect(self):
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(parameters=self.params)

    def publishThread(self, pubmsg, kwargs):
        # TODO: should it be more randomly determined?
        for i in range( len(pubmsg) ): # for every message to be published
            self.pChannel.exchange_declare(exchange=pubmsg[i]['exchange'], exchange_type='fanout')
            for j in range( kwargs['nbr'][i] ): # for the number of times a msg should be published
                self.pChannel.basic_publish( **pubmsg[i] )
                print('sending msg: {0}'.format(i+j+1))
                time.sleep( kwargs['time'] )
        print('publishThread ended')

    def publish(self, pubmsg, kwargs):
        status = True
        if ( self.pThread == None ) or ( not self.pThread.is_alive() ): 
            if self.pChannel == None :
                self.pChannel = self.connection.channel() # start a channel
            self.pThread = Thread( target=self.publishThread, kwargs={'kwargs' : kwargs, 'pubmsg' : pubmsg} )
            self.pThread.start()
        else:
            status = False

        return status

    def __subscribeThread(self, **kwargs):
        pass

    def subscribe(self, kwargs):
        #self.channel.basic_consume(consumer_callback=calback,queue=queue,no_ack=True, exclusive=False,consumer_tag=None)  
        self.sChannel = self.connection.channel() # start a channel
        self.sChannel.exchange_declare(exchange=kwargs['exchange'], exchange_type='fanout')

        result = self.sChannel.queue_declare(exclusive=True)
        queueName = result.method.queue

        self.sChannel.queue_bind(exchange=kwargs['exchange'],queue=queueName)
        self.sChannel.basic_consume(consumer_callback=kwargs['callback'], queue=queueName, no_ack=kwargs['no_ack'])

        self.sThread = Thread( target=self.sChannel.start_consuming )
        self.sThread.start()

    def disconnect(self):
        self.connection.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

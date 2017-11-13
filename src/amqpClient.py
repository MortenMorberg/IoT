from IClient import IClient
from threading import Thread
from topic import *
import time
import pika

class amqpClient(IClient):

    def __init__(self, id,  amqp_url):
        self.connection = None
        self.pChannel = None
        self.pThread = None
        self.sChannel = None
        self.sQueuename = None
        self.params = None
        self.url = amqp_url
        self.id = id
        self.qos = None

    def connect(self):
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(parameters=self.params)

    def publishThread(self, pubmsg, kwargs):
        # TODO: should it be more randomly determined?
        for i in range( len(pubmsg) ): # for every message to be published
            self.pChannel.exchange_declare(exchange=pubmsg[i]['exchange'], exchange_type='fanout')
            psize = pubmsg[i].pop('psize', 10) #TODO: 10 has been chosen for default size in publish if no psize is given
            for j in range( kwargs['nr'][i] ): # for the number of times a msg should be published
                pubmsg[i]['payload'] = gettopic(self.id, j, psize) # added new json payload!
                self.pChannel.basic_publish( **pubmsg[i] )
                print('sending msg: {0}'.format(i+j+1))
                time.sleep( kwargs['ival'] )
        print('publishThread ended')

    def publish(self, pubmsg, kwargs):
        status = True
        if ( self.pThread == None ) or ( not self.pThread.is_alive() ): 
            if self.pChannel == None :
                self.pChannel = self.connection.channel() # start a channel
            qos = pubmsg[0].pop('qos',{'pre_c' : 0, 'pre_s' : 0})
            self.pChannel.basic_qos(prefetch_size=qos['pre_s'], prefetch_count=qos['pre_c'])
            self.pThread = Thread( target=self.publishThread, kwargs={'kwargs' : kwargs, 'pubmsg' : pubmsg} )
            self.pThread.start()
        else:
            status = False

        return status

    def subscribe(self, submsg, kwargs):
        #self.channel.basic_consume(consumer_callback=calback,queue=queue,no_ack=True, exclusive=False,consumer_tag=None)  
        self.sChannel = self.connection.channel() # start a channel
        qos = submsg.pop('qos',{'pre_c' : 0, 'pre_s' : 0, 'no_ack' : False})
        self.sChannel.basic_qos(prefetch_size=qos['pre_s'], prefetch_count=qos['pre_c'])

        self.sChannel.exchange_declare(exchange=submsg['exchange'], exchange_type='fanout')

        result = self.sChannel.queue_declare(exclusive=True)
        queueName = result.method.queue

        self.sChannel.queue_bind(exchange=submsg['exchange'],queue=queueName)
        self.sChannel.basic_consume(consumer_callback=submsg['cb'], queue=queueName, no_ack=submsg['no_ack'])
        self.connection.add_timeout(deadline=kwargs.get('timeout', 30), callback_method=self.sChannel.stop_consuming ) #TODO: defaults to 30s
        self.sThread = Thread( target=self.sChannel.start_consuming )
        self.sThread.start()

    def disconnect(self):
        self.connection.close()
        
    def waitForClient(self):
        if self.pThread != None:
            self.pThread.join()
        if self.sThread != None:
            self.sThread.join()
        

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

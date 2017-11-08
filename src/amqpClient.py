from IClient import IClient
from threading import Thread
import pika

class amqpClient(IClient):

    def __init__(self, amqp_url):
        self.connection = None
        self.pChannel = None
        self.pThead = None
        self.sChannel = None
        self.sQueuename = None
        self.params = None
        self.url = amqp_url

    def connect(self):
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(parameters=self.params)

    def publishThread(self, **kwargs):
        self.pChannel.basic_publish( **kwargs )

    def publish(self, **kwargs):
        self.pChannel = self.connection.channel() # start a channel
        self.pThread = Thread( target=self.publishThread, kwargs=kwargs )
        self.pThread.start()

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

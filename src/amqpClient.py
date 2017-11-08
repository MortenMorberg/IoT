from IClient import IClient
from threading import Thread
import pika

class amqpClient(IClient):

    def __init__(self, amqp_url):
        self.connection = None
        self.pChannel = None
        self.pThead = None
        self.sChannel = None
        self.sThread = None
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

    def subscribeThread(self, **kwargs):
        pass
        #self.pChannel.basic_publish( **kwargs )

    def subscribe(self, callback, queue):
        #self.channel.basic_consume(consumer_callback=calback,queue=queue,no_ack=True, exclusive=False,consumer_tag=None)  
        self.sChannel = self.connect.channel() # start a channel
        self.sThread = Thread( target=self.subscribeThread, kwargs={'topics' : topics} )
        self.sThread.start()

    def disconnect(self):
        self.connection.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

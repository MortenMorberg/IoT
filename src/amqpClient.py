from IClient import IClient
import pika

class amqpClient(IClient):

    def __init__(self, amqp_url):
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url

    def connect(self):
        self.params = pika.URLParameters(url)
        self.params.socket_timeout = 5
        self.connect = pika.BlockingConnection(parameters=self.params)
        self.channel = self.connect.channel() # start a channel

    def publish(self, **kwargs):
        self.channel.basic_publish( **kwargs )

    def subscribe(self, callback, queue):
        self.channel.basic_consume(consumer_callback=calback,queue=queue,no_ack=True, exclusive=False,consumer_tag=None)  
    def disconnect(self):
        pass

    def on_message(self, channel, method, properties, body):
        print(method.delivery_tag)
        print(body)
        print(channel.basic_ack(delivery_tag=method.delivery_tag))

    def __exit__(self, exc_type, exc_value, traceback):
        self.connect.close()

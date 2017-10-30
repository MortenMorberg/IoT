import pika

class amqp_client:

    def __init__(self, url):
        self.params = pika.URLParameters(url)
        self.params.socket_timeout = 5

    def connect(self):
        self.connect = pika.BlockingConnection(parameters=self.params)
        self.channel = self.connect.channel() # start a channel

    def publish(self, **kwargs):
        self.channel.basic_publish( **kwargs )

    def subscribe(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.connect.close()

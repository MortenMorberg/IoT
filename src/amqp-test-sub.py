from amqpClient import amqpClient
from threading import Thread
import pika
import time

# http://192.168.43.104:15672/ --> username: guest password: group4

def callback(ch, method, properties, body):
    print(body.decode('utf-8'))

if __name__ == "__main__":

    url = 'amqp://bbjpgbhk:g460d0kQW8VRZA7KlLQ6uC4-Mxd_yG3e@golden-kangaroo.rmq.cloudamqp.com/bbjpgbhk'
    #url =  'amqp://iotgroup4:iot4@192.168.43.104:5672'
    
    amqp = amqpClient( url )

    amqp.connect()
    amqp.subscribe({'exchange': 'x', 'cb': callback, 'no_ack': True}, {'timeout' : 30})
    
    print("going to while loop")
    while(True):
        time.sleep(1)
    #    print('in script')


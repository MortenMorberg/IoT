from amqpClient import amqpClient
import pika

# http://192.168.43.104:15672/ --> username: guest password: group4

if __name__ == "__main__":

    #url = 'amqp://bbjpgbhk:g460d0kQW8VRZA7KlLQ6uC4-Mxd_yG3e@golden-kangaroo.rmq.cloudamqp.com/bbjpgbhk'
    url =  'amqp://iotgroup4:iot4@192.168.43.104:5672'
    amqp = amqpClient( url )

    amqp.connect()
    topic = {'exchange': 'temp', 'routing_key': '', 'body': 'test' }
    amqp.publish( **topic )
    
    amqp.subscribe('temp')

    print("going to while loop")
    while(True):
        pass


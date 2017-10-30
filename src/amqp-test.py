from amqp_client import amqp_client
import pika

if __name__ == "__main__":

    url = 'amqp://bbjpgbhk:g460d0kQW8VRZA7KlLQ6uC4-Mxd_yG3e@golden-kangaroo.rmq.cloudamqp.com/bbjpgbhk'
    #url =  'amqp://iotgroup4:group4@192.168.43.104:5672'
    amqp = amqp_client( url )

    amqp.connect()
    topic = {'exchange': 'temp', 'routing_key': '', 'body': 'test' }
    amqp.publish( **topic )

    while(True):
        pass


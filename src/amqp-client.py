#!/usr/bin/env python

import pika

if __name__ == "__main__":
    # configuration
    url = 'amqp://bbjpgbhk:g460d0kQW8VRZA7KlLQ6uC4-Mxd_yG3e@golden-kangaroo.rmq.cloudamqp.com/bbjpgbhk'
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    # blocking connection
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel() # start a channel


    channel.basic_publish(exchange='', routing_key='', body='')


    while(True):
        pass

    connection.close()

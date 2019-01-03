#!/usr/bin/env python
import pika

# basic queue receiver example
credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('queenbee.local',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# declare our queue - this name needs to match value in send.py
channel.queue_declare(queue='hello')

# callback for received message
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# Register listener
# no_ack parameter turns off message acknowledgement
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

# loop until canceled
channel.start_consuming()

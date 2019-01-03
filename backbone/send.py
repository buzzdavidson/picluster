#!/usr/bin/env python
import pika

# simple queue sender example; paired with receive.py

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('queenbee.local',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# declare our queue - this needs to match value in receive.py
channel.queue_declare(queue='hello')

# publish our message using the default exchange.
# in this case, the routing key will determine the queue to receive the message.
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

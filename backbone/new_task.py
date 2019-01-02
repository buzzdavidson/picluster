#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('queenbee.local',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      )
)
print(" [x] Sent 'Hello World!'")
connection.close()

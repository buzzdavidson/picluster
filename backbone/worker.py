#!/usr/bin/env python
import pika
import time

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('queenbee.local',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# this queue is declared as durable
channel.queue_declare(queue='task_queue', durable=True)
# Ensure that workers are only executed if they are not busy
channel.basic_qos(prefetch_count=1)

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # note: either need no_ack in consume method or manually call basic_ack
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
channel.basic_consume(callback,
                      queue='task_queue',
#                      no_ack=True
)

channel.start_consuming()

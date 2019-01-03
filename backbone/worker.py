#!/usr/bin/env python
import pika
import time

# example demonstrating multiple workers consuming from a single queue.
# run multiple instances of this application and submit tasks with new_task,py
credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('queenbee.local',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# Declare the queue and make it durable
channel.queue_declare(queue='task_queue', durable=True)

# Ensure that workers are only executed if they are not busy
channel.basic_qos(prefetch_count=1)

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # Messages will not be removed from queue until acknowledged.
    # if the basic_consume method includes no_ack, this happens automatically.
    # in this case, we're directly calling basic_ack to notify that work has
    # been successfully completed.
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
channel.basic_consume(callback,
                      queue='task_queue',
)

channel.start_consuming()

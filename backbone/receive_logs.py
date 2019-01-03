import pika

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('queenbee.local',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# note: this is an unnamed queue, so it will have a random name
# note: the exclusive flag ensures that the temporary queue is deleted
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

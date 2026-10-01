import pika

# establishing a connection with rabbitmq server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#before sending we need to make sure the recipient queue exists
channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

channel.basic_publish(exchange='',
                      routing_key='hello', #queue name
                      body='Hello world!')
print(" [x] Sent 'Hello World!' ")

connection.close()
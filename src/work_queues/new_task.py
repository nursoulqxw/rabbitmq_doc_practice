import pika, sys

# establishing a connection with rabbitmq server
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

#before sending we need to make sure the recipient queue exists
channel.queue_declare(queue='task_queue', durable=True, arguments={'x-queue-type': 'quorum'})

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue', #queue name
    body=message,
    properties = pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent # make message persistent (survive RabbitMQ node restarts)
    ))
print(f" [x] Sent {message}")
connection.close()
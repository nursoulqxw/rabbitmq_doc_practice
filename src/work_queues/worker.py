import pika, os, sys, time

# message acknowledgement is used to ensure that messages are not lost if the worker dies while processing a message. By default, RabbitMQ will consider a message acknowledged as soon as it has been delivered to a consumer. If the consumer dies before acknowledging the message, RabbitMQ will requeue the message and deliver it to another consumer.

# def main():

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# we need to make sure that the queue will survive a RabbitMQ node restart. In order to do so, we need to declare it as durable
channel.queue_declare(queue='task_queue', durable=True, arguments={'x-queue-type': 'quorum'}) 
# receiving the message from the queue
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag) # manual message acknowledgment

channel.basic_qos(prefetch_count=1) # this tells RabbitMQ not to give more than one message to a worker at a time. Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one. Instead, it will dispatch it to the next worker that is not still busy.
# telling the rabbitmq that this particular callback function should receive messages from our task_queue
channel.basic_consume(queue='task_queue',
                    on_message_callback=callback)
# print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
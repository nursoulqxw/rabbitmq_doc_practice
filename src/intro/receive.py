import pika, os, sys

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

    # receiving the message from the queue
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # telling the rabbitmq that this particular callback function should receive messages from our 'hello' queue
    channel.basic_consume(queue='hello',
                        on_message_callback=callback,
                        auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
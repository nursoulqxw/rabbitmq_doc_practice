import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Cәлем Қазақ халқым! алты жетіііі"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(f" [x] Sent {message}")
connection.close()
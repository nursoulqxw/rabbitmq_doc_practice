channel.basic_publish(exchange='', #<- default exchange, which is a direct exchange that routes messages to queues based on the routing key. In this case, the routing key is set to 'hello', which means that the message will be sent to the queue named 'hello'.
                      routing_key='hello',
                      body=message)
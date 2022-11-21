import pika
import time
import json

conn_params = pika.ConnectionParameters('localhost', 5672)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='first-queue')


def publish(body):
    channel.basic_publish(exchange='', routing_key='first-queue', body=json.dumps(body))
    # print(f"Date sent: {json.dumps(body)}")


# for i in range(10):
#     a = [1, 2, 3, 4, 5]
#     publish(a)
#     time.sleep(1)


# for i in range(100):
#     channel.basic_publish(exchange='',
#                           routing_key='first-queue',
#                           body='Hi consumer!')
#     print("Greeting sent")
#     time.sleep(2)


# connection.close()

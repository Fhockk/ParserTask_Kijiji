import pika
import json

conn_params = pika.ConnectionParameters('localhost', 5672)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='second-queue')


def publish(body):
    channel.basic_publish(exchange='', routing_key='second-queue', body=json.dumps(body))
    # print(f"Date sent: {json.dumps(body)}")

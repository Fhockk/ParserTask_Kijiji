import pika
import time
import json

conn_params = pika.ConnectionParameters(host='rabbitmq', port=5672)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='first-queue')


def publish(body):
    channel.basic_publish(exchange='', routing_key='first-queue', body=json.dumps(body))
    # print(f"Date sent: {json.dumps(body)}")




import pika
import traceback, sys
import json
from parse_link import ParseLinks
from send_tobd import publish

conn_params = pika.ConnectionParameters(host='localhost', port=5672)
# conn_params = pika.ConnectionParameters(host='localhost', port=5672, heartbeat=5)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='first-queue')
count = []
print('Waiting for messages. Exit: Ctrl - C')
parser = ParseLinks()


def callback(ch, method, properties, body):
    count.append(1)
    kkk = json.loads(body)
    parser.main(kkk)
    # print(count)
    # print(kkk)


channel.basic_consume(on_message_callback=callback, queue='first-queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)



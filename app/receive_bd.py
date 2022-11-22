import pika
import traceback, sys
import json
from psycopg2 import extensions
import psycopg2
from psycopg2.errors import UniqueViolation

from db_config import create_database, create_tables, create_conn

conn_params = pika.ConnectionParameters(host='rabbitmq', port=5672)
# conn_params = pika.ConnectionParameters(host='localhost', port=5672, heartbeat=5)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

# count = []

create_database()
create_tables()

channel.queue_declare(queue='second-queue')
print('Waiting for messages. Exit: Ctrl - C')

conn = create_conn()

with conn:
    def callback(ch, method, properties, body):
        # count.append(1)
        kkk = json.loads(body)
        # print(type(kkk[21]))
        table = 'ad_list'
        table2 = 'ad_author'
        sql_ins_data = f"""
                                INSERT INTO {table}
                               (ad_id,
                                title,
                                locationn,
                                item_posted,
                                price,
                                utilities,
                                author_id,
                                hydro,
                                heat,
                                water,
                                parking,
                                agr_type,
                                moveindate,
                                pet,
                                sizee,
                                furnished,
                                dishwasher,
                                fridge,
                                air_cond,
                                balcony,
                                smoking,
                                gym,
                                pool,
                                concierge,
                                security,
                                bicycle_park,
                                storage_space,
                                elevator,
                                barrier,
                                vis_aid,
                                acc_wash,
                                acc_wheelch,
                                description
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                """
        sql_ins_data2 = f"""
                                INSERT INTO {table2}
                               (
                               author_id,
                               author_name,
                               role
                               ) 
                               VALUES (%s, %s, %s);
        """

        for el in kkk:
            author_data = []
            author_data.append(el.get('author_id'))
            author_data.append(el.pop('author_name'))
            author_data.append(el.pop('role'))
            author_tuple = tuple(author_data)
            # print(author_tuple)

            el_tuple = tuple(el.values())
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql_ins_data2, author_tuple)
                    cursor.execute(sql_ins_data, el_tuple)
                    conn.commit()
                except UniqueViolation:
                    conn.rollback()
                    continue

    channel.basic_consume(on_message_callback=callback, queue='second-queue')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)




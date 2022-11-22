import psycopg2
from psycopg2 import Error, extensions


def create_conn():
    conn = psycopg2.connect(database='testdata',
                            user='postgres',
                            password='postgres',
                            host='db',
                            port='5432'
                            )
    print("CONNECTED TO DB ")
    return conn


def create_database():
    try:
        username = 'postgres'
        db_name = 'testdata'
        connection = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )

        autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        connection.set_isolation_level(autocommit)

        cursor = connection.cursor()

        sql_create_db = f"""
                                CREATE DATABASE {db_name}
                                WITH OWNER = {username}
                                ENCODING = 'UTF8';
                                """

        try:
            cursor.execute(sql_create_db)
        except (Exception, Error) as error:
            print(error)
    except (Exception, Error) as error:
        print(error)


def create_tables():
    table_name1 = 'ad_list'
    table_name2 = 'ad_author'

    sql_create_table1 = f"""
                    CREATE TABLE IF NOT EXISTS {table_name1} (
                    id_row SERIAL PRIMARY KEY,
                    ad_id INTEGER,
                    title VARCHAR(512),
                    locationn VARCHAR(255),
                    item_posted DATE,
                    price INTEGER,
                    utilities VARCHAR(64),
                    author_id INTEGER REFERENCES {table_name2} (author_id),
                    hydro BOOLEAN,
                    heat BOOLEAN,
                    water BOOLEAN,
                    parking BOOLEAN,
                    agr_type VARCHAR(127),
                    moveindate DATE,
                    pet BOOLEAN,
                    sizee REAL,
                    furnished BOOLEAN,
                    dishwasher BOOLEAN,
                    fridge BOOLEAN,
                    air_cond BOOLEAN,
                    balcony BOOLEAN,
                    smoking BOOLEAN,
                    gym BOOLEAN,
                    pool BOOLEAN, 
                    concierge BOOLEAN, 
                    security BOOLEAN,
                    bicycle_park BOOLEAN,
                    storage_space BOOLEAN,
                    elevator BOOLEAN,
                    barrier BOOLEAN,
                    vis_aid BOOLEAN,
                    acc_wash BOOLEAN,
                    acc_wheelch BOOLEAN,
                    description TEXT,
                    UNIQUE(ad_id)
                    );
                    """
    sql_create_table2 = f"""
                    CREATE TABLE IF NOT EXISTS {table_name2} (
                    id_row SERIAL PRIMARY KEY,
                    author_id INTEGER,
                    author_name VARCHAR(128),
                    role VARCHAR(20),
                    UNIQUE(author_id)
                    );
    """
    conn = create_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_create_table2)
            cursor.execute(sql_create_table1)
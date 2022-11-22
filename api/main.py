from fastapi import FastAPI, Request
import psycopg2

engine = psycopg2.connect(database='testdata',
                          user='postgres',
                          password='postgres',
                          host='db',
                          port='5432'
                          )

app = FastAPI()


def ad_validate(data):
    ad = {
        'id': data[0],
        'ad_id': data[1],
        'title': data[2],
        'locationn': data[3],
        'item_posted': data[4],
        'price': data[5],
        'utilities': data[6],
        'author_id': data[7],
        'hydro': data[8],
        'heat': data[9],
        'water': data[10],
        'parking': data[11],
        'agr_type': data[12],
        'moveindate': data[13],
        'pet': data[14],
        'sizee': data[15],
        'furnished': data[16],
        'dishwasher': data[17],
        'fridge': data[18],
        'air_cond': data[19],
        'balcony': data[20],
        'smoking': data[21],
        'gym': data[22],
        'pool': data[23],
        'concierge': data[24],
        'security': data[25],
        'bicycle_park': data[26],
        'storage_space': data[27],
        'elevator': data[28],
        'barrier': data[29],
        'vis_aid': data[30],
        'acc_wash': data[31],
        'acc_wheelch': data[32],
        'description': data[33]
    }
    return ad


@app.get('/')
def get_root():
    return {"Hello world"}


@app.get('/ad/{id_row}')
def get_ad(id_row):
    table = 'ad_list'
    sql = f"""
        SELECT * FROM {table}
        WHERE id_row={id_row}
    """
    with engine.cursor() as cursor:
        cursor.execute(sql)
        records = cursor.fetchall()
        return ad_validate(records[0])


# Price: as range(from minimal to maximal)
@app.get('/sort_by_price')
def get_sort_by_price():
    table = 'ad_list'
    sql = f"""
        SELECT * FROM {table}
        ORDER BY price ASC;
    """
    with engine.cursor() as cursor:
        cursor.execute(sql)
        records = cursor.fetchall()
        result = []
        for item in records:
            result.append(ad_validate(item))
        return result


# Date: as range (from earliest to latest)
@app.get('/sort_by_date')
def get_sort_by_date():
    table = 'ad_list'
    sql = f"""
        SELECT * FROM {table}
        WHERE item_posted IS NOT NULL
        ORDER BY item_posted DESC;
    """
    with engine.cursor() as cursor:
        cursor.execute(sql)
        records = cursor.fetchall()
        result = []
        for item in records:
            result.append(ad_validate(item))
        return result


# points from The Unit and Overview (name=True/False)
@app.get('/sort/')
def get_sort_by_data(request: Request):
    table = 'ad_list'
    params = request.query_params
    result = dict(params)
    print(result)
    if result:
        if len(result) == 1:
            for key, value in result.items():
                sql = f"""
                    SELECT * FROM {table}
                    WHERE {key} = {value}
                """
                with engine.cursor() as cursor:
                    cursor.execute(sql)
                    records = cursor.fetchall()
                    result = []
                    for item in records:
                        result.append(ad_validate(item))
                    return result
        else:
            sql = f"SELECT * FROM {table} WHERE"
            for key, value in result.items():
                sql_ad = f" {key} = {value} AND"
                sql += sql_ad
            sql = sql[:-4] + ';'
            with engine.cursor() as cursor:
                cursor.execute(sql)
                records = cursor.fetchall()
                result = []
                for item in records:
                    result.append(ad_validate(item))
                return result
    return params

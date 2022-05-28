from psycopg2 import connect, Error
import csv
import pandas as pd
from pandas.io.excel import ExcelWriter


def my_connect():
    _username = 'postgres'
    _password = '123'
    _host = 'localhost'
    _database = 'ad_forum'
    _port = '5432'
    tables = ['auth_user', 'ad_forum_director', 'ad_forum_post', 'ad_forum_news', 'ad_forum_review']

    try:
        cnx = connect(
            host=_host,
            user=_username,
            password=_password,
            database=_database,
            port=_port
        )
        cursor = cnx.cursor()
        for table in tables:
            cursor.execute(f'SELECT * FROM {table}')
            with open(f'{table}.csv', 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)

            with ExcelWriter(f'{table}.xlsx') as ew:
                pd.read_csv(f'{table}.csv', encoding='windows-1251').to_excel(ew, sheet_name=f'{table}.csv')

    except Error as e:
        print(e)

    return cnx


my_connect()

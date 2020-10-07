import csv
import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print('CONNECTION:', connection)

cursor = connection.cursor()
print('CURSOR:', cursor)

query = '''
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    survived bool,
    pclass int,
    name varchar,
    sex varchar,
    age float,
    sib_spouse_count int,
    parent_child_count int,
    fare float8
);
'''

cursor.execute(query)

def write_rows():
    with open(f'{os.getcwd()}/titanic.csv') as titanic:
        csvReader = csv.reader(titanic)
        next(csvReader)
        counter = 1
        for row in csvReader:
            if "'" in row[2]:
                name = row[2].replace("'", '')

            else:
                name = row[2]
            data = (counter, row[0], int(row[1]), name, row[3], float(row[4]), 
            int(row[5]), int(row[6]), float(row[7]))
            
            insert_query = f'''
            INSERT INTO passengers VALUES {data};
            '''
            print(insert_query)
            cursor.execute(insert_query)
            counter += 1


write_rows()
connection.commit()
connection.close()

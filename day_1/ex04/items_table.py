import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql


def item_create_script(table_name):
    create_script = sql.SQL('''CREATE TABLE {} (
                        product_id   INTEGER,
                        category_id   NUMERIC,
                        category_code   TEXT NULL,
                        brand        varchar(254) NULL
                    )''').format(sql.Identifier(table_name))
    return create_script


def connection():
    load_dotenv()
    hostname = "localhost"
    database = os.getenv('POSTGRES_DB')
    username = os.getenv('POSTGRES_USER')
    pwd = os.getenv('POSTGRES_PASSWORD')
    port_id = os.getenv('PORT_ID')
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    return conn


def store_in_database(filename, conn, cur):
    assert os.path.exists(filename), "The file doesnt exist"
    assert filename.endswith('.csv'), "File isnt csv file"
    table_name = 'items'
    cur.execute(sql.SQL('DROP TABLE IF EXISTS {}').format
                (sql.Identifier(table_name)))
    cur.execute(create_script(table_name))

    with open(filename, 'r') as f:
        next(f)  # skip header
        cur.copy_expert(
            sql.SQL("COPY {} FROM STDIN WITH CSV HEADER").format
            (sql.Identifier(table_name)), f
        )


def main():
    conn = None
    cur = None
    try:
        conn = connection()
        cur = conn.cursor()
        store_in_database("../subject/item/item.csv", conn, cur)
    except Exception as e:
        print("Error:", e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.commit()
            conn.close()


if __name__ == "__main__":
    main()
else:
    print("incorrect main import")

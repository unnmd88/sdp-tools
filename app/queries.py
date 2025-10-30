from contextlib import contextmanager

import psycopg2


@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        dbname='tdb', user='admin1', password='1122', host='localhost', port='5432'
    )
    try:
        yield conn
    finally:
        conn.close()


def get_all(tablename):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(f'SELECT * FROM {tablename}')
        results = cur.fetchall()
        print(results)


def drop_tables():
    stmt = """
            DO $$ 
            DECLARE 
                r RECORD;
            BEGIN 
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP; 
            END $$;
            """
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(stmt)
        conn.commit()


def create_tlo_table():
    stmt = """
            CREATE TABLE TLO (
            pk_tlo_id     SERIAL PRIMARY KEY,
            name          varchar(40) UNIQUE,
            district      varchar(40) NOT NULL DEFAULT '',
            fk_tlo        int REFERENCES REGIONS(pk_regions_id)
            );
            """
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(stmt)
        conn.commit()


def create_regions_table():
    stmt = """
            CREATE TABLE REGIONS (
            pk_regions_id     SERIAL PRIMARY KEY,
            city              varchar(40) UNIQUE,
            region            int UNIQUE
            );
            """
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(stmt)
        conn.commit()


def insert_data_tlo():
    with get_db_connection() as conn, conn.cursor() as cur:
        with open('data_tlo') as file:
            for l in file:
                cur.execute(f'INSERT INTO TLO (name, district, fk_tlo) VALUES {l}')
        conn.commit()


def insert_data_regions():
    with get_db_connection() as conn, conn.cursor() as cur:
        with open('data_regions') as file:
            for l in file:
                cur.execute(f'INSERT INTO regions (city, region) VALUES {l}')
        conn.commit()


def join1():
    with get_db_connection() as conn, conn.cursor() as cur:
        with open('data_regions') as file:
            for l in file:
                cur.execute(f'INSERT INTO regions (city, region) VALUES {l}')
        conn.commit()


if __name__ == '__main__':
    drop_tables()

    """ Mutable section """
    create_regions_table()
    insert_data_regions()
    create_tlo_table()
    insert_data_tlo()

    get_all('tlo')
    get_all('regions')

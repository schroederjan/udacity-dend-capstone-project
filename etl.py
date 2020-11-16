import configparser
import psycopg2
from sql_queries import insert_table_queries

def insert_tables(cur, conn):
    """uses database connection and loads data into dimension/fact tables"""
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """reads connection data from .cfg file and connects with psycopg2"""
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['TIMESCALEDB'].values()))
    cur = conn.cursor()
    
    #insert precreated tables
    insert_tables(cur, conn)
    
    #copy/insert from staging csv
    file = open('data/staging_data/taxi_df.csv')
    cur.copy_from(file, 'rides', sep=',')        
    
    file = open('data/staging_data/bridge_df.csv')
    cur.copy_from(file, 'weather', sep=',')       
    
    file = open('data/staging_data/zones_df.csv')
    cur.copy_from(file, 'zones', sep=',')           
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
import configparser
import psycopg2
from sql_queries import insert_table_queries, insert_analytics_table_queries

def insert_tables(cur, conn):
    """uses database connection and loads data into dimension/fact tables"""
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def insert_analytics_tables(cur, conn):
    """uses database connection and loads data into dimension/fact tables"""
    for query in insert_analytics_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """reads connection data from .cfg file and connects with psycopg2"""
    try:
        # connect to the timescaleDB server
        print('Connecting to the timescaleDB server...')
        config = configparser.ConfigParser()
        config.read('dwh.cfg')
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['TIMESCALEDB'].values()))
        cur = conn.cursor()        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  
    
    """inserts data into tables"""
    try:
        #insert precreated tables
        print("Inserting precreated data into the database tables...")
        insert_tables(cur, conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)   
    
    """inserts data into tables"""
    try:
        #copy/insert from staging csv
        print("Copy/Inserting staged data into the database tables...")
        
        file = open('data/staging_data/taxi_df.csv')
        cur.copy_from(file, 'rides', sep=',')        
        
        file = open('data/staging_data/bridge_df.csv')
        cur.copy_from(file, 'weather', sep=',')       
        
        file = open('data/staging_data/zones_df.csv')
        cur.copy_from(file, 'zones', sep=',')         
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)  
    
    
    """insert data for analytics table"""
    try:
        #need to be after inserting all the other tables
        print("Inserting data for analytics tables...")
        insert_analytics_tables(cur, conn)       
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)       

    print("Committing changes...")
    conn.commit()
    print("Closing connection...")
    conn.close()

if __name__ == "__main__":
    main()
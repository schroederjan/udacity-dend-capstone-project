import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP EXTENSIONS

timescaledb_extension_drop = "DROP EXTENSION IF EXISTS timescaledb"

# CREATE EXTENSIONS

timescaledb_extension_create = "CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE"

# DROP TABLES

rides_table_drop = "DROP TABLE IF EXISTS rides"
payment_types_table_drop = "DROP TABLE IF EXISTS payment_types"
rates_table_drop = "DROP TABLE IF EXISTS rates"
weather_table_drop = "DROP TABLE IF EXISTS weather"
zones_table_drop = "DROP TABLE IF EXISTS zones"
taxi_hour_table_drop = "DROP TABLE IF EXISTS taxi_hour CASCADE"

# CREATE TABLES

rides_table_create= ("""
CREATE TABLE rides
(
    vendor_id INTEGER,
    pickup_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    dropoff_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    passenger_count NUMERIC,
    trip_distance NUMERIC,
    pickup_id  INTEGER,
    rate_code  INTEGER,
    dropoff_id INTEGER,
    payment_type INTEGER,
    fare_amount NUMERIC,
    extra NUMERIC,
    mta_tax NUMERIC,
    tip_amount NUMERIC,
    tolls_amount NUMERIC,
    improvement_surcharge NUMERIC,
    total_amount NUMERIC
);
SELECT create_hypertable('rides', 'pickup_datetime', 'payment_type', 2, create_default_indexes=>FALSE);
CREATE INDEX ON rides (vendor_id, pickup_datetime desc);
CREATE INDEX ON rides (pickup_datetime desc, vendor_id);
CREATE INDEX ON rides (rate_code, pickup_datetime DESC);
CREATE INDEX ON rides (passenger_count, pickup_datetime desc);
""")

taxi_hour_table_create = ("""
CREATE TABLE taxi_hour
(
one_hour TIMESTAMP WITHOUT TIME ZONE NOT NULL,
count_rides NUMERIC
);
SELECT create_hypertable('taxi_hour', 'one_hour');
""")

payment_types_table_create = ("""
CREATE TABLE payment_types
(
    payment_type INTEGER,
    description TEXT
);
""")

rates_table_create = ("""
CREATE TABLE rates
(
    rate_code   INTEGER,
    description TEXT
);
""")

weather_table_create = ("""
CREATE TABLE weather
(
    datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    pedestrians INTEGER,
    weather TEXT,
    temperature NUMERIC,
    rain NUMERIC,
    events TEXT
);
""")

zones_table_create = ("""
CREATE TABLE zones
(
    location_id INTEGER,
    borough TEXT,
    zone TEXT,
    service_zone TEXT
);
""")

# INSERT TABLES

payment_type_table_insert = (""" INSERT INTO payment_types(payment_type, description) VALUES
(1, 'credit card'),
(2, 'cash'),
(3, 'no charge'),
(4, 'dispute'),
(5, 'unknown'),
(6, 'voided trip')
""")

rates_table_insert = (""" INSERT INTO rates(rate_code, description) VALUES
(1, 'standard rate'),
(2, 'JFK'),
(3, 'Newark'),
(4, 'Nassau or Westchester'),
(5, 'negotiated fare'),
(6, 'group ride')
""")

#INSERT TABLE (ANALYTICS)

taxi_hour_insert_table = (""" 
INSERT INTO taxi_hour
SELECT time_bucket_gapfill('1 hour', pickup_datetime, '2018-01-01 00:00:00','2018-01-31 23:59:59') AS one_hour, COUNT(*) AS count_rides
    FROM rides
    WHERE  pickup_datetime < '2018-02-01' AND pickup_datetime > '2018-01-01'
    GROUP BY one_hour
    ORDER BY one_hour
;
""")

# QUERY LISTS

drop_extensions_queries = [timescaledb_extension_drop]
create_extensions_queries = [timescaledb_extension_create]

drop_table_queries = [rides_table_drop, payment_types_table_drop, rates_table_drop, weather_table_drop, zones_table_drop, taxi_hour_table_drop]
create_table_queries = [rides_table_create, payment_types_table_create, rates_table_create, weather_table_create, zones_table_create, taxi_hour_table_create]

insert_table_queries = [payment_type_table_insert, rates_table_insert]
insert_analytics_table_queries = [taxi_hour_insert_table]


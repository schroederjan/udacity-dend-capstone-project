
#PACKAGES
import pandas as pd

#FUNCTIONS
def prepare_taxi_data():
    
    # TLC Data = taxi_data
    taxi_data = pd.read_csv("data/out_2018_01.csv", 
                            parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"])
    #drop duplicates in the df
    taxi_dup = taxi_data.drop_duplicates()
    #drop na's in the df
    taxi_clean = taxi_dup.dropna(how = "all")
    #change the column names for better management
    taxi_clean.columns = ["vendor_id",
                          "pickup_datetime",
                          "dropoff_datetime",
                          "passenger_count",                      
                          "trip_distance",
                          "rate_code",
                          "store",
                          "pickup_id",
                          "dropoff_id",
                          "payment_type",
                          "fare_amount",
                          "extra",
                          "mta_tax",
                          "tip_amount",
                          "tolls_amount",
                          "improvement_surcharge",
                          "total_amount"]
    #remove one column without need
    taxi_df = taxi_clean.loc[ : , taxi_clean.columns != 'store']  
    
    #transform the df types accordingly
    taxi_df['vendor_id'] = taxi_df['vendor_id'].apply(int)
    taxi_df['rate_code'] = taxi_df['rate_code'].apply(int)
    taxi_df['payment_type'] = taxi_df['payment_type'].apply(int)
    taxi_df['pickup_id'] = taxi_df['pickup_id'].apply(int)
    taxi_df['dropoff_id'] = taxi_df['dropoff_id'].apply(int)    
    
    #save to staging files
    tmp_df = "data/staging_data/taxi_df.csv"
    taxi_df.to_csv(tmp_df, header=False, index = False)     

prepare_taxi_data()

def prepare_taxi_zone_data():
    
    # Taxi Zone Data = taxi_zone_data
    taxi_zone_data = pd.read_csv("data/taxi_zone_data.csv")    
    #drop duplicates in the df
    taxi_zone_data_dup = taxi_zone_data.drop_duplicates()    
    #drop na's in the df
    taxi_zones_clean = taxi_zone_data_dup.dropna(how = "all")    
    #change the column names for better management
    taxi_zones_clean.columns = ["location_id",
                                "borough",
                                "zone",
                                "service_zone"]
    zones_df = taxi_zones_clean
    
    #save to staging files
    tmp_df = "data/staging_data/zones_df.csv"
    zones_df.to_csv(tmp_df, header=False, index = False)     

prepare_taxi_zone_data()    

def prepare_bridge_data():
    
    bridge_data = pd.read_json("data/bridge_data.json")
    #first cut down on interesting columns
    bridge_selection = bridge_data[["hour_beginning", "Pedestrians", "weather_summary", "temperature", "precipitation", "events"]]
    #drop duplicates in the df
    bridge_dup = bridge_selection.drop_duplicates()
    #drop na's in the df
    bridge_clean = bridge_dup.dropna(how = "all")    
    #change the column names for better management
    bridge_clean.columns = ["datetime",
                            "pedestrians",
                            "weather",
                            "temperature",
                            "rain",
                            "events"]
    bridge_df = bridge_clean
    #transform the df types accordingly
    bridge_df["datetime"] = pd.to_datetime(bridge_df["datetime"])
    bridge_df["temperature"] = pd.to_numeric(bridge_df["temperature"])
    bridge_df["rain"] = pd.to_numeric(bridge_df["rain"]) 
    
    #fill NaN for NUMERIC values
    bridge_df["temperature"] = bridge_df["temperature"].fillna(0)
    bridge_df["rain"] = bridge_df["rain"].fillna(0)
    bridge_df["pedestrians"] = bridge_df["pedestrians"].fillna(0)    
    
    #save to staging files
    tmp_df = "data/staging_data/bridge_df.csv"
    bridge_df.to_csv(tmp_df, header=False, index = False)     

prepare_bridge_data()   
    
        

    
    





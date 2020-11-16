
def download_data_csv(year):
    
    import csv
    import requests    
    
    url = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_" + str(year) + "-"
    
    for x in range(1, 13):
        #try:
            
        #download file
        month = str(x).zfill(2)
        link = url + month + ".csv"
        print("Requesting URL:")
        print(link)            
        response = requests.get(link)      
        
        #writing file
        filename = "out_" + str(year) + "_" + str(month) + ".csv"
        print("Writing File...")
        print(filename)
        
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for line in response.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))        
             
        #except:
            
           # print("Link not found. Not downloaded the following link.")
            #print(url, str(x).zfill(2), ".csv", sep="")     

#calling the function
download_data_csv(2018)






    


    
    
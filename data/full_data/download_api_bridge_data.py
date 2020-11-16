
def import_data_api():
    
    import json
    from sodapy import Socrata    
    
    #client connect
    url = "data.cityofnewyork.us"
    code = "6fi9-q3ta"
    client = Socrata(url, None)
    
    #get data
    print("Requesting Data...")
    data_raw = client.get(code)
    client.close()
    
    #write data
    print("Writing File...")
    print("data.json")
    with open('data.json', 'w') as outfile:
        json.dump(data_raw, outfile)    
        
    print("Done.")

import_data_api()


    

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv

from datetime import datetime
import pandas as pd

import json
import os
import json
import io

load_dotenv()
    
path = os.getenv("FILE_PATH")

api_key = os.getenv("API_KEY")

sandbox_api_url = os.getenv("SANDBOX_API_URL")

parameters = {
    'start':'1',
    'limit':'5000',
    'market_cap_min':'500000',
    'convert':'USD',
    'sort_dir':'desc',
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try: 
    response = session.get(sandbox_api_url, params=parameters)
        
    json_data = json.loads(response.text)
    
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    str_current_datetime = str(current_datetime)
    
    file_name = "CMC_" + str_current_datetime + ".csv";
    
    file_path = path + file_name
    
    raw_df = pd.DataFrame(json_data["data"])
    
    price_lst = []
    
    market_cap_lst = []
    
    for data in raw_df["quote"]:
        
        _data = data["USD"]
        
        price_lst.append(_data["price"])
        
        market_cap_lst.append(_data["market_cap"])
         
    clean_df = pd.DataFrame(columns=['Id','Name','Symbol','Slug','Last Updated','Price','Market Cap'])
    
    clean_df['Id'] = raw_df["id"]
    clean_df['Name'] = raw_df["name"]
    clean_df['Symbol'] = raw_df['symbol']
    clean_df['Slug'] = raw_df['slug']
    clean_df['Last Updated'] = raw_df['last_updated']
    clean_df['Price'] = price_lst
    clean_df['Market Cap'] = market_cap_lst
    
    with io.StringIO() as csv_buffer:
        
        clean_df.to_csv(file_path, index=False);
                      
except (ConnectionError, Timeout, TooManyRedirects) as error:
    print(error)
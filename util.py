import pandas as pd
from datetime import timedelta
import json
import requests
import time
import json
from geoip2 import database
# change this
reader = database.Reader('./geoip/GeoLite2-City_20190611/GeoLite2-City.mmdb')

HOSTNAME = "100.88.37.43"
PORT = 9200
ADDR = f"http://{HOSTNAME}:{PORT}"

headers = {'Content-type': 'application/json'}

def bulk_send_dataframe(df, index):
    """
    index: elastic search index that you want to send to
    Example: 
    index="netflow":
    or index="features"
    Returns
        json message
    """
    
    action = { "index" : { "_index" : index}}
    action = json.dumps(action)
    # convert dataframe to list of dict
    to_send = [row.to_dict() for i, row in df.iterrows()]
    data_to_post = f"{action}\n" + f"\n{action}\n".join(json.dumps(d) for d in to_send)+ "\n"
    r = requests.post(url=f"{ADDR}/_bulk?pretty", data=data_to_post, headers=headers)
    return r.json()
    
def geo_helper(ip):
    """
    Extract the following from ip (String)
    - Latitude
    - Longitude
    - Country
    Returns
        ["{Latitude},{Longitude}", Country] or [None, None]
    """
    try:
        response = reader.city(ip)
        lat = response.location.latitude
        lon = response.location.longitude
        geostring = f"{round(lat,2)},{round(lon,2)}"
        country = response.country.names["en"]
        return [geostring, country]
    except:
        return [None, None]
    
def add_geoinformation(df, dest_col, src_col=None):
    """
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
    
    Read from df[dest_col] (and df[src_col] if given src_col)
    for each ip in each col:
    Apply geo_helper on each ip to create 2 new columns: 
    df["dest_location"] and df["dest_country"] (and src_location and src_country if given src_col)
    Returns:
        Dataframe with additional columns
    """
    dest_addr = df[dest_col]
    if src_col is not None:
        src_addr = df[src_col]
        addr = pd.concat([src_addr, dest_addr])
    else:
        addr = dest_addr
        
    geo_map = {ip: geo_helper(ip) for ip in addr.unique()}
    
    if src_col is not None:
        src_result = list(zip(*src_addr.map(geo_map)))
        df["src_location"], df["src_country"] = src_result
    
    dest_result = list(zip(*dest_addr.map(geo_map)))
    df["dest_location"], df["dest_country"] = dest_result
        
    return df

def add_geoinformation_and_send_dataframe(df, index):
    if index=="netflow":
        src_col="IPV4_SRC_ADDR"
    if index=="features":
        src_col=None
    df = add_geoinformation(df, dest_col='IPV4_DST_ADDR', src_col=src_col)
    response_message = bulk_send_dataframe(df, index)
    return response_message

# Setup for Elasticsearch

## Setup of Mapping/ Schema
Check [Mapping Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html) for more information

Mappings for `netflow` index
```
PUT netflow
{
 'mappings': {
    'properties': {
        'Attack': {'type': 'float'},
        'DEST_CUSTOMER': {'type': 'long'},
        'DST_AS': {'type': 'long'},
        'EXPORTER_IPV4_ADDRESS': {'type': 'ip'},
        'FIRST_SWITCHED': {'type': 'long'},
        'INPUT_SNMP': {'type': 'long'},
        'IN_BYTES': {'type': 'long'},
        'IN_PKTS_COUNT': {'type': 'long'},
        'IPV4_DST_ADDR': {'type': 'ip'},
        'IPV4_DST_MASK': {'type': 'long'},
        'IPV4_SRC_ADDR': {'type': 'ip'},
        'IPV4_SRC_MASK': {'type': 'long'},
        'L4_DST_PORT': {'type': 'long'},
        'L4_SRC_PORT': {'type': 'long'},
        'LAST_SWITCHED': {'type': 'long'},
        'OUTPUT_SNMP': {'type': 'long'},
        'OUT_BYTES': {'type': 'long'},
        'OUT_PKTS_COUNT': {'type': 'long'},
        'PACKET_SIZE': {'type': 'float'},
        'PROTOCOL': {'type': 'long'},
        'SRC_AS': {'type': 'long'},
        'SRC_CUSTOMER': {'type': 'long'},
        'TCP_FLAGS': {'type': 'long'},
        'dest_country': {'type': 'text'},
        'dest_location': {'type': 'geo_point'},
        'record_time': {'format': 'yyyy-MM-dd HH:mm:ss',
                        'type': 'date'},
        'src_country': {'type': 'text'},
        'src_location': {'type': 'geo_point'}
        }
    }
}
```

Mappings for `features` index or other example data
```
PUT features
{
 'mappings': {
    'properties': {
        '0_300_PKTS_RATIO': {'type': 'float'},
         '1200_PKTS_RATIO': {'type': 'float'},
         '301_600_PKTS_RATIO': {'type': 'float'},
         '601_900_PKTS_RATIO': {'type': 'float'},
         '901_1200_PKTS_RATIO': {'type': 'float'},
         'ACK_PKTS_RATIO': {'type': 'float'},
         'DST_AS': {'type': 'long'},
         'ICMP_PKTS_RATIO': {'type': 'float'},
         'IN_PKTS_COUNT': {'type': 'long'},
         'IPV4_DST_ADDR': {'type': 'ip'},
         'L4_DST_PORT': {'type': 'long'},
         'L4_SRC_PORT': {'type': 'long'},
         'PKTS_PER_DST': {'type': 'float'},
         'RST_PKTS_RATIO': {'type': 'float'},
         'SRC_AS': {'type': 'long'},
         'SYN_PKTS_RATIO': {'type': 'float'},
         'TCP_PKTS_RATIO': {'type': 'float'},
         'UDP_PKTS_RATIO': {'type': 'float'},
         'dest_country': 'type': 'text'},
         'dest_location': {'type': 'geo_point'},
         'nDST_IP': {'type': 'long'},
         'nSRC_IP': {'type': 'long'},
         'nSrcAS_nDstAS_Ratio': {'type': 'float'},
         'nSrcs_nDsts_Ratio': {'type': 'float'},
         'record_time': {'format': 'yyyy-MM-dd HH:mm:ss',
                         'type': 'date'}
        }
    }
}
```
To send using `requests` in Python:
```python
import requests
headers = {'Content-type': 'application/json'}
ADDR = f"http://{HOSTNAME}:{PORT}"
r = requests.put(url=ADDR, json=msg, headers=headers)
# where ADDR is 'http://<YOUR HOST NAME>:9200/<INDEX>//'
# msg is the dictionary of mappings and properties
```

We will be using the same `ADDR` and `headers` for the subsequent API calls.

## Push Data to Elasticsearch

```
netflow = pd.read_csv("./path/to/netflow.csv")
features = pd.read_csv("./path/to/features.csv")
```

Bulk Push data using the Bulk API [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

Example

```
POST _bulk
{ "index" : { "_index" : "test", "_id" : "1" } }
{ "field1" : "value1" }
```
For the case of bulk sending `netflow` data, 
```
POST _bulk
{"index": {"_index": "netflow"}}
{"Attack": 0.1, "DEST_CUSTOMER": 763, "DST_AS": 29684, "EXPORTER_IPV4_ADDRESS": "9.11.178.7", "FIRST_SWITCHED": 1543622413, "INPUT_SNMP": 12, "IN_BYTES": 144, "IN_PKTS_COUNT": 3, "IPV4_DST_ADDR": "9.11.190.81", "IPV4_DST_MASK": 29, "IPV4_SRC_ADDR": "0.115.66.205", "IPV4_SRC_MASK": 0, "L4_DST_PORT": 41098, "L4_SRC_PORT": 33358, "LAST_SWITCHED": 1543622422, "OUTPUT_SNMP": 9, "OUT_BYTES": 0, "OUT_PKTS_COUNT": 0, "PACKET_SIZE": 48.0, "PROTOCOL": 17, "SRC_AS": 39386, "SRC_CUSTOMER": -1, "TCP_FLAGS": 0, "dest_country": "United States", "dest_location": "37.75,-97.82", "record_time": "2018-12-01 00:00:00", "src_country": NaN, "src_location": NaN}
{"index": {"_index": "netflow"}}
{"Attack": 0.627, "DEST_CUSTOMER": 1305, "DST_AS": 29684, "EXPORTER_IPV4_ADDRESS": "9.11.178.7", "FIRST_SWITCHED": 1543622382, "INPUT_SNMP": 12, "IN_BYTES": 123, "IN_PKTS_COUNT": 1, "IPV4_DST_ADDR": "9.11.190.81", "IPV4_DST_MASK": 29, "IPV4_SRC_ADDR": "1.174.56.5", "IPV4_SRC_MASK": 0, "L4_DST_PORT": 771, "L4_SRC_PORT": 0, "LAST_SWITCHED": 1543622382, "OUTPUT_SNMP": 9, "OUT_BYTES": 0, "OUT_PKTS_COUNT": 0, "PACKET_SIZE": 123.0, "PROTOCOL": 1, "SRC_AS": 39386, "SRC_CUSTOMER": -1, "TCP_FLAGS": 0, "dest_country": "United States", "dest_location": "37.75,-97.82", "record_time": "2018-12-01 00:00:00", "src_country": "Taiwan", "src_location": "23.5,121.0"}
...
```
The each line in the data here is seperated by a newline `\n`. We sent this data in the same way we have been sending our json. Here, we declare it as the variable `data_to_post`

```python
# let df be the netflow dataframe
# index be a a string "netflow"

action = { "index" : { "_index" : index}}
action = json.dumps(action)
# convert dataframe to list of dict
to_send = [row.to_dict() for i, row in df.iterrows()]
data_to_post = f"{action}\n" + f"\n{action}\n".join(json.dumps(d) for d in to_send)+ "\n"
r = requests.post(url=f"{ADDR}/_bulk?pretty", data=data_to_post, headers=headers)
```

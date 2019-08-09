# Setting up ElasticSearch and Kibana

## Elasticsearch Installation (centOS)

Download and install the RPM manually for

### ES rpm

Install the latest version following instructions from [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/)

Example
```bash
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.0-x86_64.rpm
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.0-x86_64.rpm.sha512
sudo rpm --install elasticsearch-7.3.0-x86_64.rpm
```

### Running as a service (systemd)
NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
```bash
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service
 ```
### You can start elasticsearch service by executing
```bash
 sudo systemctl start elasticsearch.service
```
Created elasticsearch keystore in /etc/elasticsearch

To check if successful installed and running
```bash
curl -X GET "localhost:9200/"
```

### Access from browser
```bash
cd /etc/elasticsearch
vim elasticsearch.yml
```

Change and add settings under `network` to the following
```
transport.host: localhost
transport.tcp.port: 9300
http.port: 9200
network.host: 0.0.0.0
```
Then restart elasticsearch

```bash
 sudo systemctl restart elasticsearch.service
```

To check if successful configured and running
```bash
curl -X GET "<YOUR NETWORK HOST>:9200/"
```
And access it from your browser. You should get a json message with the relevant information

## Kibana installation (centOS)

### Kibana rpm

Install the latest version following instructions from [here](https://www.elastic.co/guide/en/kibana/current/rpm.html)

```bash
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.3.0-x86_64.rpm
sudo rpm --install kibana-7.3.0-x86_64.rpm
```

### Running as a service (systemd)
```bash
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
```
By default, kibana will be hosted on port `5601`. Check `localhost:5601` to see if properly installed. 
To access from designated ip, make the following changes

### Access from browser
```bash
cd /etc/kibana
vim kibana.yml
```

Change/ or add `server.host`
```
server.host: 0.0.0.0
```
Then restart kibana and check if it is running.

```bash
 sudo systemctl restart kibana.service
```

Access from browser: `<YOUR NETWORK HOST>:5601/`
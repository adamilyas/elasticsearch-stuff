# Setting up ElasticSearch and Kibana

We aim to setup elasticsearch 7.3 (ES) and kibana 7.3 on centOS machine using RPM package manager by

* Downloading and installing ES rpm
* Edit ES yml file
* Enable and run ES service via systemd
* Downloading and installing kibana rpm
* Edit kibana yml file
* Enable and run kibana service via systemd

## Elasticsearch Installation (centOS)

Download and install the RPM manually for

### Installing Elasticsearch rpm

Install the latest version following instructions from [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/)

```bash
$ rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
$ wget https://artifacts.elastic.co/downloads/elasticsearch/\
elasticsearch-7.3.0-x86_64.rpm
$ wget https://artifacts.elastic.co/downloads/elasticsearch/\
elasticsearch-7.3.0-x86_64.rpm.sha512
$ sudo rpm --install elasticsearch-7.3.0-x86_64.rpm
```

### Allow access from via network address
```bash
$ cd /etc/elasticsearch
$ vim elasticsearch.yml
```
Change and add settings under `network` to the following
```
transport.host: localhost
transport.tcp.port: 9300
http.port: 9200
network.host: 0.0.0.0
```

### Running as a service (systemd)
NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable elasticsearch.service
$ sudo systemctl start elasticsearch.service
```
To check if successful installed and running
```bash
$ curl -X GET "<YOUR NETWORK HOST>:9200/"
```
Also, try access it from your browser. You should get a json message with the relevant information

## Kibana installation (centOS)

### Installing Kibana rpm

Install the latest version following instructions from [here](https://www.elastic.co/guide/en/kibana/current/rpm.html)

```bash
$ wget https://artifacts.elastic.co/downloads/kibana/kibana-7.3.0-x86_64.rpm
$ sudo rpm --install kibana-7.3.0-x86_64.rpm
```
By default, kibana will be hosted on port `5601`.
To access from designated network ip, make the following changes

### To allow access from network host ip
```bash
$ cd /etc/kibana
$ vim kibana.yml
```
Change/ or add `server.host`
```
server.host: 0.0.0.0
```

### Running as a service (systemd)
```bash
$ sudo /bin/systemctl daemon-reload
$ sudo /bin/systemctl enable kibana.service
$ sudo systemctl start kibana.service
```
Access from browser: `<YOUR NETWORK HOST>:5601/`

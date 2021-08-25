# PerformanceDataConsumer
Service receives binary encoded Performance Data Stream Units (PDSUs), decodes PDSUs and forwards decoded data to monitoring solution.

The Performance Data Stream Units are described using ASN.1.
Transfer syntax for Performance Data Stream Units is derived from their ASN.1 definitions by use of Packed Encoding
Rules (PER).

## Usage
Before start make sure that required ports are not already in use:
```
ss -tulpn | grep ':8083\>\|:8086\>\|:8090\>\|:3000\>\|:8186\>\|:8187\>\|:50007\>' && echo 'Ports already used' || echo 'Ports free'
```
Clone repository and set owner of grafana's data:
```
git clone https://github.com/SkoltechSummerCamp/PerformanceDataConsumer.git
cd PerformanceDataConsumer
sudo chown -R 104:104 monitoring/data/grafana
```
Start performance data consumer and monitoring system:
```
docker-compose -f docker-compose.yml -p monitoring up -d --force-recreate
```

Grafana will be located at ```http://localhost:3000```

Stop performance data consumer and monitoring system:
```
docker-compose -p monitoring down
```
Send data from json file ```PDC_CLIENT_DATA_PATH```:
```
python3 client_file_metrics.py
```
Send computer metrics:
```
python3 client_computer_metrics.py
```
To send computer metrics to preset dashboards, set environmet variable ```PDC_STREAM_ID``` to ```0```:
```
export PDC_STREAM_ID=0
```
Or you can edit dashboards: change streamId comparison in query: ```"streamId"=<'your streamId'>```

You can add your own dashboard in directory ```./monitoring/data/grafana/dashboards```

## Environment variables
```DOCKER_HUB_USERNAME``` - username for performancedataconsumer container. Should be the same as in github secrets.

```PDC_SCHEMA_PATH``` - path to asn.1 schema that would be used to decode serialized data and encode data in test clients; not recommended to change it: library asn1tools can convert some asn.1 types to python types that is not serializable to json, so it requires to change ```server.py``` (f.e. UTCTime converts to datetime.datetime); test clients works with schemas/PerformanceDataStreamUnits.asn schema.

```PDC_ASN_TYPE_NAME``` - name of schema type; must be the same as in chosen asn.1 schema.

```PDC_CODEC_TYPE``` - type of codec that would be used to decode serialized data and encode data in test clients.

```PDC_TELEGRAF_HOST``` - telegraf hostname.

```PDC_TELEGRAF_PORT``` - telegraf port; if you change this parameter - change telegraf port also in docker-compose.

```PDC_TELEGRAF_ENDPOINT``` - telegraf endpoint.

Address that performancedataconsumer would use to send data: ```{PDC_TELEGRAF_HOST}:{PDC_TELEGRAF_PORT}{PDC_TELEGRAF_ENDPOINT}``` (f.e. ```127.0.0.1:8187/telegraf```).

```PDC_HOST``` - performancedataconsumer hostname.

```PDC_PORT``` - performancedataconsumer port.

```PDC_CLIENT_DATA_PATH``` - path to json file that can be used to test performancedataconsumer with ```client_file_metrics.py```.

```PDC_STREAM_ID``` - ```streamId``` parameter that would be used in ```client_computer_metrics.py```. ```-1``` sets random ```streamId```.

```PDC_BUFFER_SIZE``` - size of buffer that receive data from connected sockets.

Deafult values of variables with prefix PDC defined in settings.ini.
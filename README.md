# PerformanceDataConsumer
Service receives binary encoded Performance Data Stream Units (PDSUs), decodes PDSUs and forwards decoded data to monitoring solution.

The Performance Data Stream Units are described using ASN.1.
Transfer syntax for Performance Data Stream Units is derived from their ASN.1 definitions by use of Packed Encoding
Rules (PER).

## Usage
Initially set grafana's directory user:
```
sudo chown -R 104:104 monitoring/data/grafana
```
Start server:
```
docker-compose -f docker-compose.yml -p monitoring up -d --force-recreate
```
Before start make sure that ports 8083, 8086, 8090, 3000, 8186, 8187, 50007 are not already in use

Grafana will be located at ```http://localhost:3000```

Stop server:
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
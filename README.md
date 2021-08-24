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
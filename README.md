# PerformanceDataConsumer
Service receives binary encoded Performance Data Stream Units (PDSUs), decodes PDSUs and forwards decoded data to monitoring solution.

The Performance Data Stream Units are described using ASN.1.
Transfer syntax for Performance Data Stream Units is derived from their ASN.1 definitions by use of Packed Encoding
Rules (PER).

## Usage
Start server:
```
docker-compose -f docker-compose.yml -p monitoring up -d --force-recreate
```
Send data from json file ```PDC_CLIENT_DATA_PATH```:
```
python3 client_file_metrics.py
```
Send computer metrics:
```
python3 client_computer_metrics.py
```
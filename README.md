# PerformanceDataConsumer
Service receives binary encoded Performance Data Stream Units (PDSUs), decodes PDSUs and forwards decoded data to monitoring solution.

The Performance Data Stream Units are described using ASN.1.
Transfer syntax for Performance Data Stream Units is derived from their ASN.1 definitions by use of Packed Encoding
Rules (PER).

## Usage
Start server:
```
docker build . -t server
docker run -p 50007:50007 server
```
To start server in demo mode add ```--env PDC_DEMO_MODE=true``` to ```docker run``` keys.

Send data from json file ```PDC_CLIENT_DATA_PATH```:
```
python3 client.py
```
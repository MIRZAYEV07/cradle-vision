   ## Rest API for converting RTSP (Real-Time Streaming Protocol) URL into HLS (HTTP Live Streaming) format
Rest Api built with FastAPI . The main functionalities are to create a FastAPI endpoint to accept an RTSP URL ,
 Implement a mechanism to convert the RTSP stream into HLS format.


----






## API Usage
```
Convert RTSP to HLS
```
Endpoint: `/convert`

Method:`POST`

Request Body:
 

```json
{
  "rtsp_url": "rtsp://your-rtsp-url"
}
```
----

Response: http 200
```json
{
  "hls_url": "/hls/{log_id}/index.m3u8"
}
```

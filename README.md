   ## Rest API for converting RTSP (Real-Time Streaming Protocol) URL into HLS (HTTP Live Streaming) format
Rest Api built with FastAPI . The main functionalities are to create a FastAPI endpoint to accept an RTSP URL ,
 Implement a mechanism to convert the RTSP stream into HLS format.


----
## Used `ffmpeg-python ` python library for converting RTSP (Real-Time Streaming Protocol) URL into HLS (HTTP Live Streaming) format 
`ffmpeg-python ` is a wrapper around the FFmpeg library for Python. It allows you to use FFmpeg functionality directly within your Python code. FFmpeg is a powerful multimedia processing tool that can handle audio, video, and other multimedia tasks.





## API Usage
```
Convert RTSP to HLS
```
Endpoint: `/convertings`

Method:`POST`

Request Body:
 

```json
{
  "id": 5 ,
  "rtsp_url": "rtsp://your-rtsp-url",
  "title": "securty-camera-1",
  "description": "aslalsklaklaksal",
  "created_at": "2024-01-20T12:00:00",
  "updated_at": "2024-01-20T12:00:00",
}
```
----

Response: http 200
```json
{
  "hls_url": "/hls/{log_id}/index.m3u8"
}
```

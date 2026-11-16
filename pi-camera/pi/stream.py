# the camera server, runs on the pi
# open http://miko.local:8000 on any laptop on the same network
#   /           page with the live picture
#   /stream     the live picture on its own, for an <img> tag
#   /photo.jpg  one frame at stream size, fast
#   /still.jpg  one photo at the sensor's full size, slower, for measuring and ML
#   /info       what the camera is set to, as json

import io
import threading
from datetime import datetime

from flask import Flask, Response, jsonify
from picamera2 import Picamera2

STREAM_SIZE = (1640, 1232)  # full view, binned 2x2. drop to (820, 616) if the stream lags
STILL_SIZE = (3280, 2464)   # every pixel the v2 sensor has
PORT = 8000

camera = Picamera2()
stream_config = camera.create_video_configuration(main={"size": STREAM_SIZE})
still_config = camera.create_still_configuration(main={"size": STILL_SIZE})
camera.configure(stream_config)
camera.start()

# flask runs every request in its own thread, the camera can only do one capture at a time
camera_lock = threading.Lock()

app = Flask(__name__)


@app.after_request
def allow_other_pages(response):
    # lets the web app (another address/port) fetch photos with javascript
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def take_jpeg():
    buffer = io.BytesIO()
    with camera_lock:
        camera.capture_file(buffer, format="jpeg")
    return buffer.getvalue()


def take_full_jpeg():
    buffer = io.BytesIO()
    with camera_lock:
        # switches to the big mode for one photo, then back to streaming
        camera.switch_mode_and_capture_file(still_config, buffer, format="jpeg")
    return buffer.getvalue()


def frames():
    while True:
        jpeg = take_jpeg()
        # multipart = the browser swaps in each new jpeg, which looks like video
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"


@app.route("/")
def page():
    return (
        "<html><head><title>Miko camera</title></head>"
        "<body style='margin:0;background:#111;text-align:center'>"
        "<img src='/stream' style='max-width:100%;max-height:100vh'>"
        "</body></html>"
    )


@app.route("/stream")
def stream():
    return Response(frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/photo.jpg")
def photo():
    return Response(take_jpeg(), mimetype="image/jpeg")


@app.route("/still.jpg")
def still():
    return Response(take_full_jpeg(), mimetype="image/jpeg")


@app.route("/info")
def info():
    return jsonify(
        camera=camera.camera_properties.get("Model"),
        stream_size=list(STREAM_SIZE),
        still_size=list(STILL_SIZE),
        time=datetime.now().isoformat(timespec="seconds"),
    )


if __name__ == "__main__":
    # 0.0.0.0 so other computers can reach it, not only the pi itself
    app.run(host="0.0.0.0", port=PORT, threaded=True)

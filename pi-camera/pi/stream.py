# the camera server, runs on the pi
# open http://miko.local:8000 on any laptop on the same network
#   /                  page with the live picture, the focus bar and the lock button
#   /stream            the live picture on its own, for an <img> tag
#   /photo.jpg         one frame at stream size, fast
#   /still.jpg         one photo at the sensor's full size, slower, for measuring and ML
#   /sharpness         how sharp the picture is right now, as json
#   /sharpness/reset   POST, forget the sharpest picture so far (new sample or new spot)
#   /lock  /unlock     POST, freeze or free the exposure and white balance
#   /info              what the camera is set to and if the pi is ok, as json

import io
import json
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from flask import Flask, Response, jsonify
from picamera2 import Picamera2

STREAM_SIZE = (1640, 1232)  # full view, binned 2x2. drop to (820, 616) if the stream lags
STILL_SIZE = (3280, 2464)   # every pixel the v2 sensor has
PORT = 8000

# libcamera only knows the sensor (imx219), not that ours has no infrared filter.
# the noir file has the white balance and colours for that. a normal v2 camera = "imx219.json"
TUNING_FILE = "imx219_noir.json"

SHARP_ENOUGH = 0.95  # score above this counts as "sharp"
TREND_STEP = 0.05    # bar moved less than 5 % in a second = "steady"

TARGET_LEVEL = 220     # brightest bit of the empty background after locking, out of 255: bright, not clipped
MAX_EXPOSURE = 33000   # microseconds, one stream frame at 30 fps. darker than that = more gain instead
MAX_GAIN = 8.0

# the lock is saved here, so photos look the same after a restart too
LOCK_FILE = Path(__file__).parent / "lock.json"

camera = Picamera2(tuning=Picamera2.load_tuning_file(TUNING_FILE))
stream_config = camera.create_video_configuration(main={"size": STREAM_SIZE})
still_config = camera.create_still_configuration(main={"size": STILL_SIZE})
# picamera2 cleans the stream faster and rougher than the stills by default.
# same cleaning and sharpening for both, so the bar judges the picture the photo will have
stream_config["controls"]["NoiseReductionMode"] = still_config["controls"]["NoiseReductionMode"]
for config in (stream_config, still_config):
    config["controls"]["Sharpness"] = 1.0  # the default, written down so it can't change under us

# flask runs every request in its own thread, the camera can only do one capture at a time
camera_lock = threading.Lock()

# filled in by the focus thread, read by the requests
focus = {"raw": 0.0, "best": 0.0, "worst": float("inf"), "score": 0.0, "trend": "steady", "hint": "starting",
         "passed_peak": False, "time": 0.0}
last_metadata = {}
locked_controls = {}  # empty = camera picks exposure and colour by itself


def use_lock(values):
    """Fix exposure and white balance to these values, in the stream and in the stills."""
    locked_controls.clear()
    locked_controls.update(
        AeEnable=False,
        AwbEnable=False,
        ExposureTime=int(values["ExposureTime"]),
        AnalogueGain=float(values["AnalogueGain"]),
        ColourGains=tuple(values["ColourGains"]),  # json turns the pair into a list, picamera wants a tuple
    )
    for config in (stream_config, still_config):
        config["controls"].update(locked_controls)


# a lock from last time? start with it, so today's photos match yesterday's
if LOCK_FILE.exists():
    use_lock(json.loads(LOCK_FILE.read_text()))

camera.configure(stream_config)
camera.start()

app = Flask(__name__)


@app.after_request
def allow_other_pages(response):
    # lets the web app (another address/port) fetch photos with javascript
    response.headers["Access-Control-Allow-Origin"] = "*"
    # without this javascript can't read our own X- headers on still.jpg
    response.headers["Access-Control-Expose-Headers"] = "*"
    return response


# ---------- sharpness ----------

def sharpness_of(grey):
    """How much the brightness jumps between neighbour pixels. sharp edges = big jumps = big number."""
    # average each 2x2 block into one pixel: 1640 wide -> 820, about 0.43 um per pixel at 40x.
    # full stream pixels (0.21 um) are finer than the lens can show, so the jumps there are
    # mostly noise. openflexure found the same: clean peak at 832x624, false peaks at full size
    h, w = grey.shape
    small = grey[: h // 2 * 2, : w // 2 * 2].astype(np.float32)
    small = small.reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))
    # whole picture, not just the middle: a thin sample can have nothing in the middle
    # laplacian by hand: 4 x the pixel minus its 4 neighbours, 0 on a flat area
    edges = (4 * small[1:-1, 1:-1]
             - small[:-2, 1:-1] - small[2:, 1:-1]
             - small[1:-1, :-2] - small[1:-1, 2:])
    # a twice as bright picture has twice as big jumps (4x the variance), without being sharper.
    # dividing by brightness squared takes that out. x1000 only so the numbers are easy to read
    brightness = max(float(small.mean()), 1.0)
    return float(edges.var()) / brightness ** 2 * 1000


def hint_for(score, trend, passed_peak):
    # what the page says to the student, same text for the web app
    if score >= SHARP_ENOUGH and passed_peak:
        return "sharp, take the photo"
    if trend == "sharper":
        return "getting sharper, keep turning"
    if trend == "blurrier":
        return "getting blurrier, turn back"
    if not passed_peak:
        # 1.0 only means "best so far" until you've turned past the sharpest point once
        return "turn the focus wheel slowly to find the sharpest point"
    return "turn back slowly to the sharpest point"


def watch_focus():
    # runs forever next to the server, about 5 times a second
    global last_metadata
    recent = []   # last 3 raw values, for the average
    history = []  # last 5 averages = about one second, for the trend
    while True:
        try:
            with camera_lock:
                request = camera.capture_request()
                frame = request.make_array("main")
                last_metadata = request.get_metadata()
                request.release()
        except Exception:
            # camera busy switching modes or gone, try again in a bit
            time.sleep(0.5)
            continue

        # green channel = most of the brightness, and the sensor has twice as many green pixels
        grey = frame[:, :, 1]
        recent = (recent + [sharpness_of(grey)])[-3:]  # average of 3, one noisy frame can't jump the bar
        raw = sum(recent) / len(recent)

        focus["best"] = max(focus["best"], raw)
        focus["worst"] = min(focus["worst"], raw)
        # noise gives every picture the same base number, also a blurry one. with few cells in view
        # that base is most of the number, and raw / best would stay above 0.9 all the time.
        # so the bar runs from the blurriest picture seen (0) to the sharpest (1)
        spread = focus["best"] - focus["worst"]
        seen_change = spread >= 0.02 * focus["best"]
        score = (raw - focus["worst"]) / spread if seen_change else 0.0  # 0 = nothing to compare yet
        if seen_change and score < 0.8:
            # fell well below the best, so the best really was a peak
            focus["passed_peak"] = True

        # compare with about a second ago, turning slowly changes too little per frame.
        # measured on the bar (part of the spread), not on raw: raw is mostly noise with few cells
        history = (history + [raw])[-5:]
        change = (raw - history[0]) / spread if seen_change else 0.0
        if len(history) < 5 or abs(change) < TREND_STEP:
            trend = "steady"
        else:
            trend = "sharper" if change > 0 else "blurrier"

        focus.update(raw=round(raw, 2), score=round(score, 3), trend=trend,
                     hint=hint_for(score, trend, focus["passed_peak"]), time=time.time())
        time.sleep(0.2)


# ---------- photos ----------

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
        if locked_controls:
            # switching modes can drop the settings, put them back
            camera.set_controls(locked_controls)
    return buffer.getvalue()


def frames():
    while True:
        jpeg = take_jpeg()
        # multipart = the browser swaps in each new jpeg, which looks like video
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n"


def camera_settings():
    return {
        "locked": bool(locked_controls),
        "exposure_us": last_metadata.get("ExposureTime"),
        "analogue_gain": last_metadata.get("AnalogueGain"),
        "colour_gains": last_metadata.get("ColourGains"),
    }


# ---------- pi health ----------

def pi_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000  # file is in thousandths of a degree
    except OSError:
        return None


def pi_throttled():
    # vcgencmd says throttled=0x0 when power and heat are fine, anything else = the pi slowed down
    try:
        answer = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True, text=True, timeout=2)
        return answer.stdout.strip().split("=")[1] != "0x0"
    except (OSError, IndexError, subprocess.TimeoutExpired):
        return None


# ---------- addresses ----------

PAGE = """<html><head><title>Miko camera</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { margin: 0; background: #111; color: #eee; font-family: sans-serif; text-align: center; }
  img { max-width: 100%; max-height: 80vh; }
  #bar { width: 80%; max-width: 600px; height: 24px; margin: 8px auto; background: #333; border-radius: 12px; overflow: hidden; }
  #fill { height: 100%; width: 0; background: #c33; transition: width 0.2s; }
  button { font-size: 16px; margin: 4px; padding: 6px 14px; }
</style></head>
<body>
  <img src="/stream">
  <div id="bar"><div id="fill"></div></div>
  <div id="hint">starting</div>
  <button onclick="post('/sharpness/reset')">New sample</button>
  <button id="lock" onclick="toggleLock()">Lock light</button>
  <div style="font-size: 13px; color: #999">Lock the light first, on an empty part of the slide. Then focus.</div>
<script>
  let locked = false;

  function post(path) { return fetch(path, { method: "POST" }); }

  async function toggleLock() {
    await post(locked ? "/unlock" : "/lock");
    locked = !locked;
    document.getElementById("lock").textContent = locked ? "Unlock light" : "Lock light";
  }

  async function update() {
    const answer = await fetch("/sharpness").then(r => r.json());
    const fill = document.getElementById("fill");
    fill.style.width = (answer.score * 100) + "%";
    // red when blurry, green when sharp
    const sharp = answer.score >= 0.95 && answer.passed_peak;
    fill.style.background = sharp ? "#3c3" : answer.score >= 0.7 ? "#cc3" : "#c33";
    document.getElementById("hint").textContent = answer.hint;
  }
  setInterval(update, 300);
  // someone else may have locked it already, start the button the right way round
  fetch("/info").then(r => r.json()).then(answer => {
    locked = answer.locked;
    document.getElementById("lock").textContent = locked ? "Unlock light" : "Lock light";
  });
</script>
</body></html>"""


@app.route("/")
def page():
    return PAGE


@app.route("/stream")
def stream():
    return Response(frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/photo.jpg")
def photo():
    return Response(take_jpeg(), mimetype="image/jpeg")


@app.route("/still.jpg")
def still():
    sharpness_now = focus["score"]  # read before, the still itself pauses the focus thread
    jpeg = take_full_jpeg()
    settings = camera_settings()
    # the photo's facts ride along as headers, so the back-end gets them in the same request
    headers = {
        "X-Sharpness": str(sharpness_now),
        "X-Locked": str(settings["locked"]).lower(),
        "X-Exposure-Us": str(settings["exposure_us"]),
        "X-Analogue-Gain": str(settings["analogue_gain"]),
        "X-Colour-Gains": str(settings["colour_gains"]),
        "X-Taken-At": datetime.now().isoformat(timespec="seconds"),
    }
    return Response(jpeg, mimetype="image/jpeg", headers=headers)


@app.route("/sharpness")
def sharpness():
    return jsonify(score=focus["score"], best=round(focus["best"], 2), raw=focus["raw"],
                   trend=focus["trend"], passed_peak=focus["passed_peak"], hint=focus["hint"])


@app.route("/sharpness/reset", methods=["POST"])
def sharpness_reset():
    focus["best"] = 0.0
    focus["worst"] = float("inf")
    focus["passed_peak"] = False
    return jsonify(ok=True)


def frame_with(controls):
    """Set these controls and return a frame taken with them."""
    camera.set_controls(controls)
    for _ in range(4):
        # new settings take a few frames to reach the sensor, throw those away
        camera.capture_request().release()
    return camera.capture_array("main")


def expose_on_background():
    """Find the exposure that makes the empty background TARGET_LEVEL bright, with as little gain as possible."""
    # auto white balance on an empty slide = the lamp's own colour, so keep those colour gains
    settled = camera.capture_metadata()
    colour_gains = settled["ColourGains"]
    exposure, gain = settled["ExposureTime"], 1.0
    for _ in range(10):
        frame = frame_with({"AeEnable": False, "AwbEnable": False, "ColourGains": colour_gains,
                            "ExposureTime": int(exposure), "AnalogueGain": gain})
        # 99.9 % instead of the very brightest pixel, so one hot pixel can't decide it
        level = float(np.percentile(frame[:, :, :3], 99.9))
        if abs(level - TARGET_LEVEL) < 0.05 * TARGET_LEVEL:
            break
        # screen brightness grows slower than exposure (gamma), so step by the square of the gap.
        # clamped, so a black or white frame can't make it jump wildly
        step = min(max((TARGET_LEVEL / max(level, 1.0)) ** 2, 0.25), 4.0)
        light = exposure * gain * step
        # longer exposure first (no noise), only past one frame time turn up the gain
        exposure = min(light, MAX_EXPOSURE)
        gain = min(max(light / MAX_EXPOSURE, 1.0), MAX_GAIN)
    return {"ExposureTime": int(exposure), "AnalogueGain": gain, "ColourGains": colour_gains}


@app.route("/lock", methods=["POST"])
def lock():
    # do it on an EMPTY bright part of the slide: then the light is set by the lamp, not by
    # how many cells happen to be in view, and every sample gets the same settings
    with camera_lock:
        values = expose_on_background()
        use_lock(values)
        camera.set_controls(locked_controls)
    LOCK_FILE.write_text(json.dumps(values))
    return jsonify(camera_settings())


@app.route("/unlock", methods=["POST"])
def unlock():
    # new lens or new light: let the camera find its settings again
    with camera_lock:
        locked_controls.clear()
        for config in (stream_config, still_config):
            for name in ("ExposureTime", "AnalogueGain", "ColourGains"):
                config["controls"].pop(name, None)
            config["controls"].update(AeEnable=True, AwbEnable=True)
        camera.set_controls({"AeEnable": True, "AwbEnable": True})
    LOCK_FILE.unlink(missing_ok=True)
    return jsonify(camera_settings())


@app.route("/info")
def info():
    # ok = the focus thread got a frame in the last 3 seconds, so the camera really works
    camera_ok = time.time() - focus["time"] < 3
    return jsonify(
        ok=camera_ok,
        camera=camera.camera_properties.get("Model"),
        stream_size=list(STREAM_SIZE),
        still_size=list(STILL_SIZE),
        temperature_c=pi_temperature(),
        throttled=pi_throttled(),
        time=datetime.now().isoformat(timespec="seconds"),
        **camera_settings(),
    )


if __name__ == "__main__":
    # daemon = stops together with the server
    threading.Thread(target=watch_focus, daemon=True).start()
    # 0.0.0.0 so other computers can reach it, not only the pi itself
    app.run(host="0.0.0.0", port=PORT, threaded=True)

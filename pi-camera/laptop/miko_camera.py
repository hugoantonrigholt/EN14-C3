# gets photos from miko's camera, runs on any laptop on the same network as the pi
# use it two ways:
#   python miko_camera.py          saves one photo in photos/
#   python miko_camera.py --full   same, at full sensor size
#   python miko_camera.py --focus  prints the sharpness 5 times a second, ctrl+c stops
#   from miko_camera import get_photo   then get_photo() gives you the jpeg bytes
# only uses the standard library, so nothing to pip install
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

PI_ADDRESS = "miko.local"
PORT = 8000


def ask(path, address=PI_ADDRESS, post=False, timeout=15):
    """Send one request to the pi and return the answer's bytes and headers."""
    url = f"http://{address}:{PORT}/{path}"
    request = urllib.request.Request(url, method="POST" if post else "GET")
    with urllib.request.urlopen(request, timeout=timeout) as answer:
        return answer.read(), answer.headers


def get_photo(full=False, address=PI_ADDRESS):
    """Return one photo from the pi as jpeg bytes. full=True gives 3280 x 2464 instead of 1640 x 1232."""
    jpeg, _ = ask("still.jpg" if full else "photo.jpg", address)
    return jpeg


def get_photo_with_facts(address=PI_ADDRESS):
    """Return a full photo and its facts: sharpness, locked, exposure, gains, time."""
    jpeg, headers = ask("still.jpg", address)
    facts = {
        "sharpness": float(headers["X-Sharpness"]),
        "locked": headers["X-Locked"] == "true",
        "exposure_us": headers["X-Exposure-Us"],
        "analogue_gain": headers["X-Analogue-Gain"],
        "colour_gains": headers["X-Colour-Gains"],
        "taken_at": headers["X-Taken-At"],
    }
    return jpeg, facts


def get_sharpness(address=PI_ADDRESS):
    """Return the sharpness as a dict: score 0 to 1, trend, hint, ..."""
    body, _ = ask("sharpness", address, timeout=2)
    return json.loads(body)


def reset_sharpness(address=PI_ADDRESS):
    """Forget the sharpest picture so far, after a new sample or a new spot on the slide."""
    ask("sharpness/reset", address, post=True)


def lock(address=PI_ADDRESS):
    """Freeze exposure and white balance, so every photo after this looks the same."""
    body, _ = ask("lock", address, post=True)
    return json.loads(body)


def unlock(address=PI_ADDRESS):
    """Let the camera pick exposure and white balance again, after a new lens or light."""
    body, _ = ask("unlock", address, post=True)
    return json.loads(body)


def get_info(address=PI_ADDRESS):
    """Return the camera and pi status, ok is False when the camera stopped giving frames."""
    body, _ = ask("info", address, timeout=2)
    return json.loads(body)


def save_photo(folder="photos", full=False, address=PI_ADDRESS):
    """Save one photo with the time in its name and return where it went."""
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    file_name = folder / f"miko_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    file_name.write_bytes(get_photo(full, address))
    return file_name


def print_focus():
    # handy while turning the wheel without a browser
    while True:
        answer = get_sharpness()
        bar = "#" * int(answer["score"] * 30)
        print(f"{bar:<30} {answer['score']:.2f}  {answer['hint']}")
        time.sleep(0.2)


if __name__ == "__main__":
    if "--focus" in sys.argv:
        print_focus()
    else:
        print(f"Saved {save_photo(full='--full' in sys.argv)}")

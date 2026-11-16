# gets photos from miko's camera, runs on any laptop on the same network as the pi
# use it two ways:
#   python miko_camera.py          saves one photo in photos/
#   python miko_camera.py --full   same, at full sensor size
#   from miko_camera import get_photo   then get_photo() gives you the jpeg bytes
# only uses the standard library, so nothing to pip install
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

PI_ADDRESS = "miko.local"
PORT = 8000


def get_photo(full=False, address=PI_ADDRESS):
    """Return one photo from the pi as jpeg bytes. full=True gives 3280 x 2464 instead of 1640 x 1232."""
    name = "still.jpg" if full else "photo.jpg"
    url = f"http://{address}:{PORT}/{name}"
    with urllib.request.urlopen(url, timeout=15) as answer:
        return answer.read()


def save_photo(folder="photos", full=False, address=PI_ADDRESS):
    """Save one photo with the time in its name and return where it went."""
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    file_name = folder / f"miko_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    file_name.write_bytes(get_photo(full, address))
    return file_name


if __name__ == "__main__":
    print(f"Saved {save_photo(full='--full' in sys.argv)}")

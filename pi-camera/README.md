# Miko camera

The Raspberry Pi inside Miko runs a small web server that gives out the camera's picture. Every other part of the project (the ML service, the back-end, the web app) gets its photos from this server over the network, so nobody needs to touch the Pi to use the camera.

To set up a Pi from scratch, follow [SETUP.md](SETUP.md).

## What is in this folder

| File | Runs on | What it does |
|---|---|---|
| `pi/stream.py` | Pi | The camera server: live picture and photos on port 8000 |
| `pi/miko-camera.service` | Pi | Starts the server by itself when the Pi boots |
| `pi/preview.py` | Pi | Shows the camera on a monitor plugged into the Pi (only for testing) |
| `laptop/miko_camera.py` | Laptop | Gets a photo from the Pi, in Python, with nothing to install |

## How to reach the camera

Your laptop has to be on the same network as the Pi (for now, the phone hotspot). The Pi's address is `miko.local`.

| Address | What you get | Use it for |
|---|---|---|
| `http://miko.local:8000/` | The live picture with a focus bar, a hint and the lock button | Looking, focusing the microscope |
| `http://miko.local:8000/stream` | The live picture on its own | An `<img>` tag in the web app |
| `http://miko.local:8000/photo.jpg` | One photo, 1640 x 1232, fast | Quick checks, live counting |
| `http://miko.local:8000/still.jpg` | One photo, 3280 x 2464, takes about a second. Its facts come along as headers (below) | Photos that are saved, labelled or counted |
| `http://miko.local:8000/sharpness` | How sharp the picture is now, as JSON (below) | The sharpness bar on the Scan page, asked 2 to 5 times a second |
| `POST /sharpness/reset` | Forgets the sharpest picture so far | A new sample, or a new spot on the slide |
| `POST /lock` | Keeps the white balance the camera found, sets the exposure so the brightest part of the background is 220 of 255 with the lowest gain, saves it on the Pi, and returns it. Takes 1 to 3 seconds | Once, on an empty part of the slide, before focusing |
| `POST /unlock` | Lets the camera choose them again and forgets the saved lock | A new lens or new light |
| `http://miko.local:8000/info` | Camera model, sizes, `ok`, Pi temperature, `throttled`, `locked`, exposure and gains, as JSON | Checking the camera works. `ok` is false when no frame came in for 3 seconds |

Both photo sizes show the whole field of view: the stream combines each 2 x 2 block of pixels into one, the still keeps every pixel. For counting cells, use the still.

## The sharpness

The server works out the sharpness about 5 times a second from the whole stream picture, with each 2 x 2 block averaged into one pixel (820 x 616, about 0.43 µm per pixel at 40x): the bigger the jumps in brightness between neighbouring pixels, the sharper. Full stream pixels are finer than the 40x can show, so their jumps are mostly noise; OpenFlexure found the same and measures at 832 x 624 (Knapper et al., 2021). The whole picture is used because a thin sample can have nothing in the middle. Brighter pictures have bigger jumps without being sharper, so the number is divided by the brightness squared.

That number (`raw`) depends on the sample, and noise gives every picture the same base amount, even a blurry one. So the `score` runs from the blurriest picture since the last reset (0) to the sharpest (1): **1.0 means as sharp as it has been**. It stays 0 until the picture has changed at least 2 %. A score is only called sharp once the student has turned past the sharpest point (`passed_peak`), because before that every new best scores 1.0. With only a few cells in view, the bar hardly moves far from focus and comes alive close to it: the trend and the hint still lead the way.

```json
{"score": 0.97, "best": 1.74, "raw": 1.69, "trend": "steady", "passed_peak": true, "hint": "sharp, take the photo"}
```

`trend` is `sharper`, `blurrier` or `steady` compared with about a second ago: steady means the bar moved less than 5 %. `hint` is the sentence the page shows, so the web app can show the same text.

## A photo's facts

`still.jpg` sends these headers with the picture, so the back-end gets them in the same request. The lens and the micrometres per pixel are not here: the back-end knows which lens is on.

| Header | Example |
|---|---|
| `X-Sharpness` | `0.97` (the score just before the photo) |
| `X-Locked` | `true` |
| `X-Exposure-Us` | `12000` |
| `X-Analogue-Gain` | `1.0` |
| `X-Colour-Gains` | `(1.6, 1.9)` |
| `X-Taken-At` | `2026-11-30T14:05:12` |

## Per part of the project

**ML service (Python).** Copy `laptop/miko_camera.py` next to your code:

```python
from miko_camera import get_photo, save_photo

jpeg_bytes = get_photo(full=True)   # the photo as bytes, ready for your model
path = save_photo("photos", full=True)   # or saved as a file, if your code reads files
```

To turn the bytes into an image, use whichever library your model already uses, for example Pillow: `Image.open(io.BytesIO(jpeg_bytes))`. From the command line, `python miko_camera.py --full` saves one photo in `photos/`, and `python miko_camera.py --focus` prints the sharpness bar while you turn the wheel.

The file also has `get_photo_with_facts()`, `get_sharpness()`, `reset_sharpness()`, `lock()`, `unlock()` and `get_info()`.

**Back-end (C#).** A photo is one GET request that returns a JPEG, with its facts in the headers:

```csharp
using var http = new HttpClient { Timeout = TimeSpan.FromSeconds(15) };
using var answer = await http.GetAsync("http://miko.local:8000/still.jpg");
byte[] photo = await answer.Content.ReadAsByteArrayAsync();
string sharpness = answer.Headers.GetValues("X-Sharpness").First();
```

From there it can be saved with its sample and passed to the ML service. For `/sharpness` and `/info`, use a short timeout (about 2 seconds), so the Scan page shows "No microscope" instead of waiting when the Pi is off.

**Web app.** The live picture is one tag:

```html
<img src="http://miko.local:8000/stream" alt="Live picture from Miko">
```

The server allows other pages to fetch its photos with JavaScript (`fetch("http://miko.local:8000/still.jpg")`), so the web app can run on a different address.

## Known limits

- Only one capture runs at a time. Taking a `still.jpg` pauses the stream and the sharpness for about a second.
- The lock is for everyone using the server, not per user. It is saved in `pi/lock.json` on the Pi, so it is still there after a restart, and photos from different days match. Lock on an empty bright part of the slide: then the settings come from the lamp, not from how many cells are in view. Unlock when the lens or the light changes.
- The stream and the full photos get the same noise reduction and sharpening, so the focus bar judges the same picture the photo will have.
- The bar can't tell dust from cells. Dust or scratches on the other side of the glass give a second sharp point, about a third of a turn of the focus wheel away. Landed on specks instead of cells? Click New sample and keep turning.
- `miko.local` only works on the same network as the Pi. It does not work on eduroam.
- The camera is the NoIR version, so colours look pink in daylight. Under Miko's LED they look normal. The server loads the NoIR tuning file (`imx219_noir.json`), which has the white balance and colours for a sensor without an infrared filter. With a normal Camera V2, set `TUNING_FILE = "imx219.json"` in `pi/stream.py`.
- No password protects the server. Anyone on the same network can see the camera. That is fine on a phone hotspot, not on a public network.

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
| `http://miko.local:8000/` | A page with the live picture | Looking, focusing the microscope |
| `http://miko.local:8000/stream` | The live picture on its own | An `<img>` tag in the web app |
| `http://miko.local:8000/photo.jpg` | One photo, 1640 x 1232, fast | Quick checks, live counting |
| `http://miko.local:8000/still.jpg` | One photo, 3280 x 2464, takes about a second | Photos that are saved, labelled or counted |
| `http://miko.local:8000/info` | The camera model and sizes, as JSON | Checking the server is up |

Both photo sizes show the whole field of view: the stream combines each 2 x 2 block of pixels into one, the still keeps every pixel. For counting cells, use the still.

## Per part of the project

**ML service (Python).** Copy `laptop/miko_camera.py` next to your code:

```python
from miko_camera import get_photo, save_photo

jpeg_bytes = get_photo(full=True)   # the photo as bytes, ready for your model
path = save_photo("photos", full=True)   # or saved as a file, if your code reads files
```

To turn the bytes into an image, use whichever library your model already uses, for example Pillow: `Image.open(io.BytesIO(jpeg_bytes))`. From the command line, `python miko_camera.py --full` saves one photo in `photos/`.

**Back-end (C#).** A photo is one GET request that returns a JPEG:

```csharp
using var http = new HttpClient { Timeout = TimeSpan.FromSeconds(15) };
byte[] photo = await http.GetByteArrayAsync("http://miko.local:8000/still.jpg");
```

From there it can be saved with its sample and passed to the ML service.

**Web app.** The live picture is one tag:

```html
<img src="http://miko.local:8000/stream" alt="Live picture from Miko">
```

The server allows other pages to fetch its photos with JavaScript (`fetch("http://miko.local:8000/still.jpg")`), so the web app can run on a different address.

## Known limits

- Only one capture runs at a time. Taking a `still.jpg` pauses the stream for about a second.
- `miko.local` only works on the same network as the Pi. It does not work on eduroam.
- The camera is the NoIR version, so colours look pink in daylight. Under Miko's LED they look normal.
- No password protects the server. Anyone on the same network can see the camera. That is fine on a phone hotspot, not on a public network.

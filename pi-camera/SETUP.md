# Setting up the Raspberry Pi for Miko's camera

This guide takes the Raspberry Pi 4 and the Pi Camera V2 from the box to a live picture in the laptop's browser. It was tested on 16 Nov 2026; every problem we ran into that day is in the steps and in the table at the end.

## What you need

- Raspberry Pi 4 with its USB-C power supply and a micro SD card (16 GB is enough)
- Pi Camera V2 and a 15-pin ribbon cable
- A laptop that can read the SD card (a slot, or a USB card reader)
- A phone with a hotspot
- Optional: the Ethernet cable from the kit, as a backup connection

No monitor, keyboard or HDMI cable is needed. Everything goes through the laptop.

For a first test, leave the camera's own lens **on**. Without it the camera only sees blur and light, which looks broken but is not.

## 1. Get the hotspot ready

The Pi and the laptop meet on your phone's hotspot. School Wi-Fi (eduroam) needs a login a Pi cannot do, and on it the laptop cannot see the Pi.

- **The hotspot's name must not contain an apostrophe.** An iPhone names its hotspot after the phone, like "Hugo's iPhone", and uses a curly `’` that you cannot type the same way in Imager. The Pi then looks for a network that does not exist. Rename the phone under **Settings > General > About > Name**, for example to `HugoPhone`.
- On an iPhone, turn on **Maximise Compatibility** under Personal Hotspot.

## 2. Put Raspberry Pi OS on the SD card

This wipes the card. You do not have to delete anything first: Imager overwrites all of it.

1. If the SD card sits in an adapter, check the small slider on the adapter's side is pushed **up** (towards the contacts). Down means locked, and Imager says the card is read only.
2. Install **Raspberry Pi Imager** from raspberrypi.com/software and open it. Click **Yes** when Windows asks if it may make changes.
3. Device: **Raspberry Pi 4**. Operating system: **Raspberry Pi OS (64-bit)**. Storage: the SD card.
4. Choose to customise the settings and go through **every page**:
   - Hostname: `miko`
   - **User: a username and password. Do not skip this page.** Without it the Pi has no user and refuses every password.
   - Wi-Fi: the hotspot name exactly as the phone shows it, its password, country `NL`
   - Remote access: **SSH on**, with password login
5. Write the card. If Windows asks to format a disk while it writes or afterwards, click **Cancel**: that is the Linux part of the card.

## 3. Connect the camera (power off)

Always plug the ribbon in with the Pi switched off.

1. The blue strip on the ribbon's ends stays on. It stiffens the end and shows which way round it goes.
2. Camera end: pull the black latch out gently, slide the ribbon in with the **silver contacts facing the board and the blue side facing away from it**, push the latch back.
3. Pi end: the slot marked **CAMERA** between the micro HDMI ports and the audio jack. Lift its latch, slide the ribbon in with the **blue side facing the USB and Ethernet ports**, push the latch down.
4. Tug softly at both ends. The ribbon should not move.

## 4. First start and log in

1. Turn on the hotspot, put the card in the Pi and plug in the power. The first start takes 3 to 5 minutes.
2. Connect the **laptop to the same hotspot**, not to eduroam. If Windows jumps back to eduroam, turn off "Connect automatically" for eduroam.
3. On the laptop, in PowerShell:

```bash
ssh yourname@miko.local
```

`yourname` is the username from step 2. Type `yes` the first time. The password does not show while you type.

4. Check the camera:

```bash
rpicam-hello --list-cameras
```

It should list an **imx219** camera.

5. Install the two Python libraries. The hotspot gives the Pi internet; this uses some mobile data.

```bash
sudo apt update
sudo apt install -y python3-flask python3-picamera2
```

## 5. Copy the code to the Pi

In a **normal** PowerShell window on the laptop (not inside the ssh session), go to the folder that holds `pi-camera` and copy it over:

```bash
scp -r pi-camera yourname@miko.local:~/
```

If you get `stat local "pi-camera": No such file or directory`, PowerShell is in another folder (an admin window starts in `C:\WINDOWS\system32`). Use `cd` to go to the folder that contains `pi-camera` first.

## 6. Start the camera

In the ssh session on the Pi:

```bash
cd ~/pi-camera/pi
python3 stream.py
```

When it says `Running on http://...:8000`, open **http://miko.local:8000** in the laptop's browser. Stop it with `Ctrl+C`.

Check the focus bar: point the camera at a plain bright area and click **Lock light**. Then point it at something with text and turn its lens (or the focus wheel) slowly one way and back. The bar should rise, peak and fall, and say "sharp, take the photo" once you are back at the peak. Click **New sample** when you point it at something else.

## 7. Start it automatically when the Pi boots (optional)

Then nobody has to ssh in before using the camera: plug in the Pi, wait a minute, open the page. If your username is not `hugo`, first change `User` and the two paths in `pi/miko-camera.service`.

```bash
sudo cp ~/pi-camera/pi/miko-camera.service /etc/systemd/system/
sudo systemctl enable --now miko-camera
```

Check it with `systemctl status miko-camera`. To stop it for good: `sudo systemctl disable --now miko-camera`. While the service runs, `python3 stream.py` by hand fails with "Address already in use", because the port is taken.

## 8. Turning it off

```bash
sudo shutdown now
```

Wait until the green light stops blinking, then pull the power.

## When something goes wrong

| What you see | Cause | Fix |
|---|---|---|
| Imager says the SD card is read only | Lock slider on the adapter is down | Push it up, towards the contacts |
| `Could not resolve hostname miko.local` | The laptop is on eduroam, or the Pi has not joined the hotspot | Put the laptop on the hotspot. Count the devices on the hotspot screen: if the Pi never shows up, the Wi-Fi name or password on the card is wrong (often the apostrophe), so flash again |
| Worked before, now `Could not resolve hostname miko.local`, and the hotspot shows only the laptop | The Pi dropped off (restart, power blip) and an iPhone hides its hotspot when nothing is connected, so the Pi can't find it again | Open **Settings > Personal Hotspot** on the iPhone and keep that screen open, then unplug the Pi and plug it back in. Wait 1 to 2 minutes |
| `Connection refused` | The Pi is still starting | Wait a minute and try again |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | The card was flashed again, so the Pi has a new key | `ssh-keygen -R miko.local`, then ssh again |
| "See http://rptl.io/newuser" and every password is refused | The Pi has no user: the User page in Imager was skipped | Flash again and fill in the User page |
| No camera listed | Ribbon the wrong way round or not in far enough | Power off, reseat both ends as in step 3 |
| `No module named 'flask'` | Step 4.5 was skipped | `sudo apt install -y python3-flask python3-picamera2` |
| Picture is pink or purple | It is the **NoIR** camera, which has no infrared filter | Normal. Under Miko's own LED it looks right |
| Picture is only blur | Lens is off, or the object is too close | Lens on for testing, point at something further away |
| Stream lags | Big frames over the hotspot | In `pi/stream.py`, set `STREAM_SIZE = (820, 616)` |
| Focus bar stays empty, `/info` says `"ok": false` | The camera stopped giving frames, or the server is still starting | Wait 10 seconds. If it stays, restart the server and check the ribbon |
| `RuntimeError` or `FileNotFoundError` about `imx219_noir.json` at start | The tuning file isn't where Picamera2 looks | Check with `ls /usr/share/libcamera/ipa/rpi/vc4/`. Update with `sudo apt update && sudo apt full-upgrade` |
| Lock light takes long, picture still dark | Not enough light to reach the target in one frame time, so it turns up the gain | Turn up the LED or check it's on, then lock again |
| Bar jumps around without touching anything | Dim picture, so the camera turns up the gain and the noise looks like edges | More light, then **Lock light** |
| `"throttled": true` in `/info` | The power supply is too weak or the Pi is too hot | Use the official 5 V 3 A supply, give the Pi air |
| `Address already in use` | Another `stream.py` or the service is already running | `pkill -f stream.py`, or `sudo systemctl stop miko-camera` |

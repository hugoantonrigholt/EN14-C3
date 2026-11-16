# shows the camera on the monitor plugged into the pi
# run it from a terminal on the pi's own desktop, not over ssh
from picamera2 import Picamera2, Preview

camera = Picamera2()
# 1640 x 1232 is the v2 sensor's full view, just binned 2x2
camera.configure(camera.create_preview_configuration(main={"size": (1640, 1232)}))
camera.start_preview(Preview.QTGL)
camera.start()

input("Camera is on. Press Enter to stop.")
camera.stop()

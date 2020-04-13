``` 
git clone https://github.com/oarriaga/face_classification
```

In `src/video_emotion_color_demo.py`, somewhere on top, we add a function to
capture the screen.

``` python
import sys
import mss
from PIL import Image

def capture_screen():
    with mss.mss() as sct:
        # The sceen part to capture (here half the screen)
        montior = {"top": 0, "left": 0, "width": 1920 // 2, "height": 1080}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        # last dimension is channel, RGB -> BGR
    return np.array(img)[:, :, ::-1]

if len(sys.argv) == 2 and sys.argv[1] == 'capture':
    print('Capturing screen...')
    capture_screen_mode = True
else:
    print('Capturing camera...')
    capture_screen_mode = False
```
Inside the "main" loop we call the function.
``` python
while True:

    if capture_screen_mode:
        bgr_image = capture_screen()
    else:
        bgr_image = video_capture.read()[1]
```
Run with `python src/video_emotion_color_demo.py capture` to turn on our new thing.

# hand-control
## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download the MediaPipe hand landmark model
curl -O https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

python3 main.py
```

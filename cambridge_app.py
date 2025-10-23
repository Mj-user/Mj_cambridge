from flask import Flask, Response, render_template_string
import os
from camera_reader import CameraReader

app = Flask(__name__)

RTSP_URL = os.environ.get('CAMERA_RTSP')  # contoh: rtsp://user:pass@192.168.1.50:554/stream
CAM_INDEX = os.environ.get('CAMERA_INDEX')  # fallback untuk USB camera (0,1,...)

reader = CameraReader(rtsp_url=RTSP_URL, cam_index=(int(CAM_INDEX) if CAM_INDEX else None))

@app.route('/')
def index():
    return render_template_string("""
    <html><body>
    <h2>MJ Home Camera Bridge</h2>
    <img src="/stream.mjpg" style="max-width:100%" />
    </body></html>
    """)

def gen_frames():
    for frame in reader.frames():
        # frame is bytes (jpeg)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream.mjpg')
def stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    reader.start()
    app.run(host='0.0.0.0', port=8000, threaded=True)

"""
Camera Reader - OpenCV helper
Membaca kamera RTSP/USB dan mengembalikan frame MJPEG.
"""

import cv2

class CameraReader:
    def __init__(self, camera_url):
        self.camera_url = camera_url
        self.cap = cv2.VideoCapture(camera_url)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def encode_frame(self, frame):
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return None, None
        return ret, jpeg.tobytes()

    def release(self):
        self.cap.release()

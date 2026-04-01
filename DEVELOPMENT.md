# Hướng dẫn Nâng cấp - Driver Drowsiness Detection

Tài liệu này cung cấp các gợi ý và hướng dẫn nâng cấp hệ thống hiện tại.

## 1. Tối ưu hóa Hiệu suất (GPU Acceleration)

### NVIDIA TensorRT
Tối ưu hóa suy luận mô hình để chạy nhanh hơn trên GPU

```bash
pip3 install tensorrt
```

### Jetson Inference
Sử dụng thư viện chính thức NVIDIA

```bash
git clone https://github.com/dusty-nv/jetson-inference.git
cd jetson-inference
./buildall.sh
```

## 2. Hỗ trợ Nhiều Camera

```python
# main.py - Sửa đổi để hỗ trợ nhiều camera
cameras = [cv2.VideoCapture(0), cv2.VideoCapture(1)]

for cap in cameras:
    ret, frame = cap.read()
    # Xử lý...
```

## 3. Mô hình Phát hiện Tốt hơn

### MediaPipe (Google)
Nhẹ hơn dlib, hiệu suất tốt:

```bash
pip3 install mediapipe
```

```python
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
with mp_face_detection.FaceDetection() as face_detection:
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
```

### OpenFace
Phát hiện biểu cảm khuôn mặt chi tiết:

```bash
git clone https://github.com/TadasBaltrusaitis/OpenFace.git
```

## 4. Học Sâu - Đào Tạo Mô hình Tùy chỉnh

### Chuẩn bị Dữ liệu
- Thu thập video tài xế ngủ gật
- Gán nhãn khung hình (ngủ/tỉnh)

### Training Framework
```bash
# TensorFlow Lite (tối ưu cho embedded)
pip3 install tensorflow-hub
```

### Mô hình CNN đơn giản
```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')  # Binary: drowsy/alert
])
```

## 5. Tích hợp IoT - Gửi Dữ liệu đến Cloud

### MQTT
```bash
pip3 install paho-mqtt
```

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mqtt.example.com", 1883, 60)
client.publish("drowsiness/alert", payload=json.dumps(detector_data))
```

### AWS IoT
```bash
pip3 install AWSIoTPythonSDK
```

### Azure IoT Hub
```bash
pip3 install azure-iot-device
```

## 6. Giao Diện Web Giám Sát

### Flask
```bash
pip3 install flask
```

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### WebRTC - Streaming Video Trực tiếp
```bash
pip3 install aiortc
```

## 7. Lưu Trữ Dữ liệu - Database

### SQLite (Lightweight)
```python
import sqlite3
conn = sqlite3.connect('drowsiness.db')
c = conn.cursor()
c.execute('''CREATE TABLE detections
    (id INT, timestamp TEXT, ear REAL, alert BOOLEAN)''')
```

### TimescaleDB (Time Series)
```bash
# Trên máy chủ riêng
docker run -d --name timescaledb timescale/timescaledb:latest-pg12
```

## 8. Nâng cấp Camera

### CSI Camera
Tốc độ cao hơn USB
```bash
# Jetson CSI Camera
# Kích hoạt trong raspi-config
# Sử dụng CV_CAP_PROP_CAM_MODE
```

### Thermal Camera
Phát hiện ngủ gật dựa vào nhiệt độ

```python
# FLIR Thermal Camera
# https://github.com/groupgets/get_thermal_camera
```

## 9. Xử lý Âm thanh - Phát Âm Thanh & Ghi Âm

### PyAudio
```bash
pip3 install pyaudio
```

```python
import pyaudio
import wave

def play_alarm_sound():
    with wave.open('sounds/alarm.wav', 'rb') as wav_file:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
                        channels=wav_file.getnchannels(),
                        rate=wav_file.getframerate(),
                        output=True)
        stream.write(wav_file.readframes(2048))
        stream.stop_stream()
        stream.close()
        p.terminate()
```

## 10. Nhân Tố Khác

### Theo dõi Hệ thống
```bash
pip3 install psutil
```

### Logging Nâng cấp
```bash
pip3 install python-json-logger
```

### Version Control & CI/CD
```bash
# GitHub Actions
.github/workflows/tests.yml
```

---

## Lộ Trình Phát triển Đề xuất

1. **Giai đoạn 1**: Tối ưu hóa hiệu suất (GPU, TensorRT)
2. **Giai đoạn 2**: Mô hình tốt hơn (MediaPipe, đào tạo tùy chỉnh)
3. **Giai đoạn 3**: Tích hợp IoT (MQTT, Cloud)
4. **Giai đoạn 4**: Giao diện web & giám sát
5. **Giai đoạn 5**: Hệ thống hoàn chỉnh

---

**Cần trợ giúp?** Tạo issue hoặc tham khảo các tài liệu chính thức.

# Driver Drowsiness Detection System - Jetson Nano

Hệ thống phát hiện tài xế lái xe ngủ gật sử dụng **Jetson Nano 4GB** với camera.

## 📋 Tính năng chính

- ✅ **Phát hiện mắt đóng/mở** sử dụng Eye Aspect Ratio (EAR)
- ✅ **Cảnh báo âm thanh** khi phát hiện ngủ gật
- ✅ **Ghi log** tất cả các sự kiện phát hiện
- ✅ **Lưu khung hình** ngủ để phân tích sau
- ✅ **Tối ưu cho Jetson Nano** (độ phân giải thấp, hiệu suất cao)
- ✅ **Hỗ trợ email/SMS** (tuỳ chọn)

## 🔧 Yêu cầu phần cứng

- **Jetson Nano 4GB** (hoặc Nano 2GB)
- **Camera**: USB camera hoặc CSI camera
- **Nguồn điện**: 5V/4A USB-C
- **MicroSD card**: 64GB (hoặc lớn hơn)
- **Kết nối mạng**: WiFi USB hoặc Ethernet USB

## 📦 Yêu cầu phần mềm

- JetPack OS (L4T)
- Python 3.6+
- OpenCV
- dlib
- numpy, scipy

## 🚀 Cài đặt

### 1. Cài đặt Jetson Nano

Tham khảo hướng dẫn chính thức:
https://developer.nvidia.com/jetson-nano-developer-kit

### 2. Clone dự án

```bash
git clone https://github.com/yourusername/Driver-drowsiness.git
cd Driver-drowsiness
```

### 3. Chạy script cài đặt

```bash
chmod +x setup_jetson.sh
./setup_jetson.sh
```

### 4. Tải mô hình phát hiện mặt

```bash
python3 install_dlib_model.py
```

**Lưu ý**: Lần đầu tiên tải file này (~100MB) có thể mất vài phút.

## 💻 Cách sử dụng

### Chạy hệ thống cơ bản

```bash
python3 main.py
```

### Chạy với các tùy chọn

```bash
# Chỉ định camera
python3 main.py --camera 0

# Thay đổi ngưỡng phát hiện (mặc định 0.2)
python3 main.py --threshold 0.15

# Thay đổi số khung hình để xác định ngủ (mặc định 20)
python3 main.py --frames 25

# Lưu video đầu ra
python3 main.py --save-video

# Không hiển thị video (chỉ xử lý nền)
python3 main.py --no-display

# Kết hợp nhiều tùy chọn
python3 main.py --camera 0 --threshold 0.18 --save-video --no-display
```

### Các phím tắt

- **Q**: Thoát chương trình
- **Space** (tuỳ chỉnh): Chụp ảnh

## 📊 Cấu trúc dự án

```
Driver-drowsiness/
├── README.md                    # File này
├── config.py                    # Cấu hình hệ thống
├── main.py                      # File chính
├── eye_detector.py              # Lớp phát hiện mắt
├── alert_system.py              # Hệ thống cảnh báo
├── requirements.txt             # Các gói Python cần thiết
├── setup_jetson.sh              # Script cài đặt
├── install_dlib_model.py        # Script tải mô hình
├── models/                      # Thư mục lưu mô hình
├── logs/                        # Lưu trữ log
├── captured_frames/             # Lưu trữ ảnh ngủ
└── sounds/                      # Âm thanh cảnh báo
```

## ⚙️ Cấu hình

Chỉnh sửa file `config.py` để tuỳ chỉnh:

```python
# Độ phân giải camera
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

# Ngưỡng Eye Aspect Ratio
EYE_AR_THRESHOLD = 0.2

# Số khung hình liên tiếp để phát hiện ngủ
EYE_AR_CONSEC_FRAMES = 20

# Loại cảnh báo
ALERT_TYPE = "sound"  # "sound", "email", "sms", "all"
```

## 🎯 Chi tiết thuật toán

### Eye Aspect Ratio (EAR)

Hệ thống sử dụng công thức EAR từ bài báo "Real-Time Eye Blink Detection using Facial Landmarks":

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
```

Trong đó p1-p6 là tọa độ các điểm mốc của mắt được phát hiện bởi dlib.

- **EAR cao** (> 0.2): Mắt mở
- **EAR thấp** (< 0.2): Mắt đóng

### Quy trình phát hiện

1. **Nhận khung hình** từ camera
2. **Phát hiện khuôn mặt** sử dụng HOG-SVM detector (dlib)
3. **Lấy điểm mốc kỹ thuật số** (68 điểm từ dlib)
4. **Tính EAR** cho cả hai mắt
5. **Kiểm tra ngủ**: Nếu EAR < ngưỡng cho N khung hình liên tiếp → Phát hiện ngủ
6. **Kích hoạt cảnh báo**

## 📈 Tối ưu hóa cho Jetson Nano

- **Độ phân giải giảm**: 320x240 (thay vì 1080p)
- **Tốc độ khung hình**: 20 FPS (thay vì 30 FPS)
- **Không lưu video**: Mặc định tắt (tiết kiệm bộ nhớ)
- **Xử lý nền**: Có thể chạy mà không hiển thị GUI

## 🔍 Khắc phục sự cố

### Lỗi: "Cannot open camera"

**Giải pháp**:
```bash
# Kiểm tra camera
ls -la /dev/video*

# Cấp quyền truy cập
sudo usermod -a -G video $USER
```

### Lỗi: "dlib model not found"

**Giải pháp**:
```bash
python3 install_dlib_model.py
```

### Hiệu suất thấp (FPS thấp)

**Giải pháp**:
- Giảm độ phân giải (Sửa `CAMERA_WIDTH`, `CAMERA_HEIGHT`)
- Tắt hiển thị video (`--no-display`)
- Tắt lưu video

## 📝 Log và Dữ liệu

### Log file
- Vị trí: `logs/drowsiness_detection.log`
- Chứa: Thời gian, mức độ, thông báo lỗi

### Khung hình ngủ
- Vị trí: `captured_frames/drowsy_YYYYMMDD_HHMMSS.jpg`
- Kèm theo: File metadata `.txt`

## 📡 Mở rộng - Tích hợp email/SMS

### Cấu hình email (Gmail)

1. Bật "Less secure app access" trong Gmail
2. Hoặc tạo "App Password"
3. Sửa `alert_system.py`:

```python
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"
```

### SMS (tuỳ chọn)

Sử dụng Twilio API:
```bash
pip3 install twilio
```

## 🎓 Tham khảo

- [dlib C++ Library](http://dlib.net/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Eye Blink Detection Paper](https://ieeexplore.ieee.org/document/7313418)
- [Jetson Nano Developer Guide](https://developer.nvidia.com/jetson-nano-developer-kit)

## 📄 Giấy phép

MIT License - Xem file LICENSE

## 👨‍💻 Tác giả

Dự án phát hiện ngủ gật cho Jetson Nano

## 🤝 Đóng góp

Hoan nghênh các pull request và issue reports!

## ⚠️ Chú ý an toàn

**CẢNH BÁO**: Hệ thống này chỉ một công cụ hỗ trợ để phát hiện ngủ gật. Nó **KHÔNG thay thế** sự luôn tỉnh táo của tài xế. 

- Luôn chú ý con đường
- Nếu cảm thấy mệt, hãy dừng xe ở nơi an toàn
- Cấm sử dụng hệ thống này để bỏ qua giới hạn lái xe

---

**Phiên bản**: 1.0 
**Cập nhật lần cuối**: 2026

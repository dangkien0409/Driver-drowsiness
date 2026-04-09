# Driver Drowsiness Detection System - Jetson Nano

Hệ thống phát hiện tài xế lái xe ngủ gật sử dụng **Jetson Nano 4GB** với camera.

## 📋 Tính năng chính

- ✅ **Phát hiện mắt đóng/mở** sử dụng Eye Aspect Ratio (EAR)
- ✅ **Phát hiện ngáp** sử dụng Mouth Aspect Ratio (MAR)
- ✅ **Phát hiện tư thế xấu** 
  - Lệch đầu (Head Roll)
  - Cúi/nâng đầu (Head Pitch)  
  - Cúi phía trước (Forward Head Posture)
- ✅ **Cảnh báo đa lớp** (ngủ/ngáp/tư thế xấu)
- ✅ **Ghi log** tất cả các sự kiện phát hiện
- ✅ **Lưu khung hình** khi phát hiện sự kiện
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
git clone https://github.com/dangkien0409/Driver-drowsiness.git
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

# Thay đổi ngưỡng phát hiện mắt (EAR, mặc định 0.2)
python3 main.py --threshold 0.15

# Thay đổi ngưỡng phát hiện ngáp (MAR, mặc định 0.5)
python3 main.py --yawn-threshold 0.4

# Thay đổi ngưỡng phát hiện tư thế (độ, mặc định 15)
python3 main.py --posture-threshold 20

# Thay đổi số khung hình để xác định ngủ (mặc định 20)
python3 main.py --frames 25

# Lưu video đầu ra
python3 main.py --save-video

# Không hiển thị video (chỉ xử lý nền)
python3 main.py --no-display

# Kết hợp nhiều tùy chọn
python3 main.py --camera 0 --threshold 0.18 --yawn-threshold 0.45 --posture-threshold 18 --save-video
```

### Các phím tắt

- **Q**: Thoát chương trình
- **Space** (tuỳ chỉnh): Chụp ảnh

## 📊 Cấu trúc dự án

```
Driver-drowsiness/
├── README.md                    # File này
├── ARCHITECTURE.md              # Sơ đồ kiến trúc chi tiết
├── YAWN_POSTURE_GUIDE.md        # Hướng dẫn ngáp & tư thế
├── config.py                    # Cấu hình hệ thống
├── main.py                      # File chính (tích hợp tất cả detectors)
├── eye_detector.py              # Phát hiện mắt (EAR)
├── yawn_detector.py             # Phát hiện ngáp (MAR)
├── posture_detector.py          # Phát hiện tư thế đầu
├── alert_system.py              # Hệ thống cảnh báo
├── requirements.txt             # Các gói Python cần thiết
├── setup_jetson.sh              # Script cài đặt
├── install_dlib_model.py        # Script tải mô hình
├── models/                      # Thư mục lưu mô hình
├── logs/                        # Lưu trữ log
├── captured_frames/             # Lưu trữ ảnh sự kiện
└── sounds/                      # Âm thanh cảnh báo
```

## ⚙️ Cấu hình

Chỉnh sửa file `config.py` để tuỳ chỉnh:

```python
# ===== CAMERA =====
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_FPS = 20

# ===== PHÁT HIỆN MẮT =====
EYE_AR_THRESHOLD = 0.2           # Ngưỡng EAR (Eye Aspect Ratio)
EYE_AR_CONSEC_FRAMES = 20        # Khung liên tiếp để xác nhận ngủ

# ===== PHÁT HIỆN NGÁP =====
MOUTH_AR_THRESHOLD = 0.5         # Ngưỡng MAR (Mouth Aspect Ratio)  
YAWN_CONSEC_FRAMES = 10          # Khung liên tiếp để xác nhận ngáp

# ===== PHÁT HIỆN TƯ THẾ =====
HEAD_ROLL_THRESHOLD = 15         # Góc lệch ngang tối đa (độ)
HEAD_PITCH_THRESHOLD = 20        # Góc cúi/nâng tối đa (độ)
FORWARD_HEAD_THRESHOLD = 1.5     # Ngưỡng cúi phía trước (tỷ lệ)
POSTURE_CONSEC_FRAMES = 15       # Khung để xác nhận tư thế xấu

# ===== CẢNH BÁO =====
ALERT_TYPE = "sound"             # "sound", "email", "sms", "all"
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
### Các Điểm Mốc Khuôn Mặt (68 dlib Landmarks)

Hệ thống phát hiện các tính năng khuôn mặt chính:

```
Mũi (Nose):        Điểm 30 (Đầu mũi)
Cằm (Chin):        Điểm 8
Mắt Phải (Right):  Điểm 36-41 (Tâm = 39)  [Viewer's right]
Mắt Trái (Left):   Điểm 42-47 (Tâm = 45)  [Viewer's left]
Miệng (Mouth):     Điểm 48-67
```

**Lưu ý**: "Phải" và "Trái" được xác định từ góc nhìn của người xem (camera), không phải từ góc nhìn của tài xế.

### Bug Fix v1.1 - Sửa Chỉ Number Landmarks

**Vấn đề**: Phiên bản trước đã sử dụng sai chỉ số để xác định các điểm mắt:
- `LEFT_EYE = 36` ❌ (điểm này thực chất là mắt PHẢI)
- `RIGHT_EYE = 45` ❌ (điểm này không phải một điểm mốc mắt chuẩn)

**Giải pháp** (v1.1+):
- `RIGHT_EYE = 39` ✅ (tâm mắt phải - viewer's right)
- `LEFT_EYE = 45` ✅ (tâm mắt trái - viewer's left)

**Tác động**: Cải thiện độ chính xác của phát hiện tư thế đầu (head roll angle).
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

### Lỗi Ký Tự Tiếng Việt (Encoding Issues)

Nếu thấy ký tự lỗi hoặc "mắt T" / "mắt P" thay vì "Mắt Trái" / "Mắt Phải":

**Nguyên nhân**: Các file Python cần khai báo mã hóa UTF-8

**Giải pháp** (từ v1.1+):
- Tất cả file `.py` đã được cập nhật với `# -*- coding: utf-8 -*-`
- Nếu vẫn gặp lỗi, kiểm tra:

```bash
# Kiểm tra mã hóa file (Linux/Mac)
file -i posture_detector.py
# Kết quả mong muốn: charset=utf-8

# Nếu cần chuyển mã hóa (Linux/Mac)
iconv -f ISO-8859-1 -t UTF-8 posture_detector.py -o posture_detector_fixed.py
mv posture_detector_fixed.py posture_detector.py
```

**Lưu ý Windows**: Mở VS Code, bấm Ctrl+Shift+P, gõ "Reopen with Encoding", chọn UTF-8

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

**Phiên bản**: 1.1
**Cập nhật lần cuối**: Tháng 4, 2026

### Lịch sử thay đổi

**v1.1** (Tháng 4, 2026):
- ✅ Sửa chỉ số landmark mắt (LEFT_EYE/RIGHT_EYE indices)
- ✅ Thêm khai báo UTF-8 encoding cho tất cả file Python
- ✅ Cập nhật ghi chú về facial landmarks (68-point dlib model)
- ✅ Thêm troubleshooting cho lỗi ký tự tiếng Việt
- ✅ Cải thiện ghi chú comment trong code

**v1.0**:
- Phiên bản ban đầu

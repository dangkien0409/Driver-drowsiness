# Hệ thống Phát hiện Ngủ gật - Jetson Nano 4GB

## 📊 Tóm tắt Dự án

Đây là một hệ thống **phát hiện tài xế lái xe ngủ gật** hoàn chỉnh sử dụng **Jetson Nano 4GB** và camera. 

Hệ thống sử dụng **Eye Aspect Ratio (EAR)** - một kỹ thuật phát hiện mắt dựa trên điểm mốc khuôn mặt để xác định khi nào tài xế đang ngủ gật.

---

## ⚡ Bắt đầu nhanh

### 1️⃣ Clone và cài đặt
```bash
git clone https://github.com/yourusername/Driver-drowsiness.git
cd Driver-drowsiness
chmod +x *.sh *.py
./setup_jetson.sh
```

### 2️⃣ Tải mô hình
```bash
python3 install_dlib_model.py
```

### 3️⃣ Chạy
```bash
python3 main.py
```

### Hoặc sử dụng Menu Tương tác
```bash
python3 run.py
```

---

## 📁 Cấu trúc Dự án

```
Driver-drowsiness/
├── 📄 main.py                 # Chương trình chính
├── 📄 eye_detector.py         # Phát hiện mắt & EAR
├── 📄 alert_system.py         # Hệ thống cảnh báo
├── 📄 config.py               # Cấu hình
├── 📄 run.py                  # Menu tương tác
├── 📄 quickstart.py           # Quick start
├── 📄 check_system.py         # Kiểm tra hệ thống
├── 📄 performance_test.py     # Kiểm tra hiệu suất
├── 📄 sensitivity_test.py     # Kiểm tra độ nhạy
├── 📄 install_dlib_model.py   # Tải mô hình
├── 🔧 setup_jetson.sh         # Script cài đặt
├── 🔧 debug.sh                # Bỏ gỡ log
├── 📄 requirements.txt         # Dependencies
├── 📄 Makefile                # Unix makefile
├── 📎 LICENSE                 # Giấy phép MIT
├── 📖 README.md               # Tài liệu chính
├── 📖 DEVELOPMENT.md          # Hướng dẫn nâng cấp
├── 📖 CONTRIBUTING.md         # Hướng dẫn đóng góp
├── 📚 QUICK_SUMMARY.md        # File này
├── 🌳 models/                 # Mô hình phát hiện
├── 📋 logs/                   # Log file
├── 🎥 captured_frames/        # Ảnh khi ngủ
└── 🔊 sounds/                 # Âm thanh cảnh báo
```

---

## 🎯 Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 👁️ **Phát hiện mắt** | Sử dụng EAR từ dlib landmark |
| ⚠️ **Cảnh báo** | Âm thanh, Email, SMS |
| 📊 **Logging** | Ghi lại tất cả sự kiện |
| 🎥 **Lưu ảnh** | Chụp khung hình khi ngủ |
| 📈 **Tối ưu** | Được thiết kế cho Jetson Nano |
| ⚙️ **Tuỳ chỉnh** | Ngưỡng, camera, cảnh báo |

---

## 💻 Lệnh Sử dụng

```bash
# Chạy cơ bản
python3 main.py

# Menu tương tác
python3 run.py

# Kiểm tra hệ thống
python3 check_system.py

# Kiểm tra hiệu suất
python3 performance_test.py

# Kiểm tra độ nhạy
python3 sensitivity_test.py

# Khởi tạo nhanh
python3 quickstart.py

# Tùy chỉnh camera
python3 main.py --camera 1 --threshold 0.15 --frames 25

# Lưu video
python3 main.py --save-video

# Chạy nền (không hiển thị)
python3 main.py --no-display
```

---

## 🤖 Thuật toán

### Eye Aspect Ratio (EAR)

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
```

- **EAR > 0.2**: Mắt mở ✓
- **EAR < 0.2**: Mắt đóng ⭕

**Detectionlogic**:  
Nếu cả hai mắt đóng cho N khung hình liên tiếp → **Phát hiện ngủ** → **Kích hoạt cảnh báo**

---

## 📋 Yêu cầu

### Phần cứng
- Jetson Nano 4GB (hoặc 2GB)
- Camera USB hoặc CSI
- MicroSD 64GB+
- Nguồn 5V/4A

### Phần mềm
- JetPack OS
- Python 3.6+
- OpenCV
- dlib
- NumPy, SciPy

---

## 🔧 Cài đặt

### Phương pháp 1: Script tự động
```bash
chmod +x setup_jetson.sh
./setup_jetson.sh
```

### Phương pháp 2: Thủ công
```bash
pip3 install -r requirements.txt
python3 install_dlib_model.py
mkdir -p models logs captured_frames sounds
```

---

## ⚙️ Cấu hình

Chỉnh sửa `config.py`:
```python
CAMERA_WIDTH = 320           # Độ phân giải
CAMERA_HEIGHT = 240
EYE_AR_THRESHOLD = 0.2       # Ngưỡng phát hiện
EYE_AR_CONSEC_FRAMES = 20    # Khung hình liên tiếp
ALERT_TYPE = "sound"         # Loại cảnh báo
```

---

## 📊 Kết quả & Log

- **Log**: `logs/drowsiness_detection.log`
- **Ảnh**: `captured_frames/drowsy_*.jpg`
- **Video**: `output_video.avi` (nếu --save-video)

---

## 🐛 Khắc phục Sự cố

| Vấn đề | Giải pháp |
|---------|----------|
| ❌ Camera không mở | `ls /dev/video*` + `sudo usermod -a -G video $USER` |
| ❌ Mô hình không tìm | `python3 install_dlib_model.py` |
| ⚠️ FPS thấp | Giảm độ phân giải, sử dụng `--no-display` |
| 💾 Hết bộ nhớ | Tắt lưu video, giảm độ phân giải |

---

## 📡 Nâng cấp

- 🚀 TensorRT (tối ưu GPU)
- 🧠 MediaPipe (mô hình tốt hơn)
- ☁️ Cloud Integration (AWS/Azure)
- 🌐 Web Dashboard (Flask)
- 📱 Mobile App (Kiểm soát từ xa)

Xem `DEVELOPMENT.md` để biết chi tiết.

---

## 📚 Tài liệu

| File | Nội dung |
|------|---------|
| `README.md` | Tài liệu chi tiết đầy đủ |
| `DEVELOPMENT.md` | Hướng dẫn nâng cấp & tối ưu |
| `CONTRIBUTING.md` | Hướng dẫn đóng góp |
| `LICENSE` | Giấy phép MIT |

---

## 👨‍💻 Phát triển

```bash
# Kiểm tra code
python3 -m py_compile *.py

# Chạy unit test (nếu có)
python3 -m pytest tests/

# Code formatting
pip3 install black
black *.py
```

---

## 🎓 Tham khảo

- [dlib - Machine Learning Library](http://dlib.net/)
- [OpenCV - Computer Vision](https://opencv.org/)
- [Eye Blink Detection (Paper)](https://ieeexplore.ieee.org/document/7313418)
- [Jetson Nano Guide](https://developer.nvidia.com/jetson-nano-developer-kit)

---

## ⚖️ Giấy phép

MIT License © 2024 - Xem [LICENSE](LICENSE)

---

## ⚠️ Chú ý An toàn

> **CẢNH BÁO**: Hệ thống này chỉ hỗ trợ phát hiện. Nó **KHÔNG thay thế** sự tỉnh táo của tài xế.

✓ Luôn chú ý con đường  
✓ Dừng xe nếu mệt  
✗ Không sử dụng để bỏ qua giới hạn lái xe

---

## 📞 Hỗ trợ

- 🐛 **Bug Reports**: GitHub Issues
- 💡 **Feature Requests**: GitHub Discussions
- 🤝 **Contributions**: Pull Requests Welcome!

---

## 📈 Lộ Trình Phát triển

- ✅ v1.0: Phát hiện cơ bản
- 🔄 v1.1: GPU acceleration (TensorRT)
- 🔄 v1.2: MediaPipe support
- 🔄 v2.0: Cloud integration
- 🔄 v2.1: Web dashboard

---

**Made with ❤️ for Jetson Nano**

**Phiên bản**: 1.0  
**Cập nhật**: 2024

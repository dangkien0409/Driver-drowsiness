# Jetson Nano Drowsiness Detection - Project Structure

```
Driver-drowsiness/
│
├── 🔷 CORE MODULES (Lõi chương trình)
│   ├── main.py                       # Chương trình chính - điểm bắt đầu
│   ├── eye_detector.py               # Phát hiện mắt & tính EAR
│   ├── alert_system.py               # Hệ thống cảnh báo
│   └── config.py                     # Cấu hình hệ thống
│
├── 🛠️  UTILITY & TESTING
│   ├── check_system.py               # Kiểm tra cấu hình hệ thống
│   ├── performance_test.py           # Kiểm tra hiệu suất (FPS, bộ nhớ)
│   ├── sensitivity_test.py           # Kiểm tra độ nhạy ngưỡng EAR
│   ├── analyze_log.py                # Phân tích log file
│   ├── run.py                        # Menu tương tác
│   ├── quickstart.py                 # Khởi tạo nhanh
│   └── install_dlib_model.py         # Tải mô hình
│
├── 🔧 INSTALLATION & SETUP
│   ├── setup_jetson.sh               # Script cài đặt toàn bộ
│   ├── install_service.sh            # Cài đặt systemd service
│   ├── debug.sh                      # Tool bỏ gỡ lỗi
│   ├── requirements.txt              # Dependencies Python
│   ├── Makefile                      # Unix make commands
│   └── drowsiness-detection.service  # Systemd service file
│
├── 📚 DOCUMENTATION
│   ├── README.md                     # Tài liệu chính (chi tiết)
│   ├── QUICK_SUMMARY.md              # Tóm tắt nhanh
│   ├── ARCHITECTURE.md               # Sơ đồ kiến trúc
│   ├── DEVELOPMENT.md                # Hướng dẫn nâng cấp
│   ├── CONTRIBUTING.md               # Hướng dẫn đóng góp
│   ├── PROJECT_STRUCTURE.md          # File này
│   └── LICENSE                       # Giấy phép MIT
│
├── 📁 DATA DIRECTORIES
│   ├── models/                       # Mô hình phát hiện mặt
│   │   └── shape_predictor_68_face_landmarks.dat
│   ├── logs/                         # File log hệ thống
│   │   └── drowsiness_detection.log
│   ├── captured_frames/              # Khung hình khi ngủ
│   │   ├── drowsy_20240101_120000.jpg
│   │   └── drowsy_20240101_120000.txt
│   └── sounds/                       # Âm thanh cảnh báo
│       └── alarm.wav
│
├── .git/                             # Git repository
├── .gitignore                        # Git ignore rules
│
└── 📄 Output Files (Generated)
    ├── output_video.avi              # Video đầu ra (nếu --save-video)
    └── (Khác)

```

## 📋 Chi Tiết Từng Thành Phần

### Core Modules
- **main.py**: Vòng lặp chính, xử lý camera, điều phối các module
- **eye_detector.py**: Phát hiện mắt dùng dlib, tính toán EAR
- **alert_system.py**: Cảnh báo, logging, lưu ảnh
- **config.py**: Các hằng số cấu hình toàn bộ hệ thống

### Utilities
- **check_system.py**: Kiểm tra camera, Python packages, mô hình, thư mục
- **performance_test.py**: Đo FPS, tốc độ xử lý, sử dụng bộ nhớ
- **sensitivity_test.py**: Kiểm tra ngưỡng EAR khác nhau
- **run.py**: Menu tương tác giúp người dùng chọn chế độ chạy

### Installation
- **setup_jetson.sh**: Tự động cài đặt dependencies trên Jetson
- **requirements.txt**: Danh sách Python packages cần thiết
- **Makefile**: Shortcut cho lệnh thường dùng (make help, make run, v.v.)

### Documentation
- **README.md**: Tài liệu đầy đủ, hướng dẫn sử dụng chi tiết
- **QUICK_SUMMARY.md**: Bản tóm tắt 1 trang dành cho người khám phá
- **ARCHITECTURE.md**: Sơ đồ, luồng dữ liệu, tối ưu hóa

## 🔄 Quy Trình Sử Dụng Điển Hình

```
1. INSTALL
   ./setup_jetson.sh
   ↓
2. CHECK
   python3 check_system.py
   ↓
3. CONFIGURE (tuỳ chọn)
   Sửa config.py
   ↓
4. RUN
   python3 main.py
   ↓
5. MONITOR
   tail -f logs/drowsiness_detection.log
   ↓
6. ANALYZE
   python3 analyze_log.py
```

## 💾 File Kích Thước (Ước tính)

| File | Kích thước |
|------|-----------|
| models/shape_predictor* | ~100 MB |
| logs/drowsiness*.log | ~1-10 MB |
| output_video.avi | ~100-500 MB |
| Code (.py files) | ~30 KB |
| Docs (.md files) | ~50 KB |

## 🔐 Quyền Truy Cập (Linux)

```bash
# Executable scripts
chmod +x *.sh *.py

# Video device access
sudo usermod -a -G video $USER

# Audio access (optional)
sudo usermod -a -G audio $USER
```

## 🎯 Điểm Bắt Đầu cho Người Dùng Mới

1. **Nhanh nhất**: `python3 quickstart.py`
2. **Menu tương tác**: `python3 run.py`
3. **Lệnh trực tiếp**: `python3 main.py`

## 🔍 Khám Phá Thêm

Sau khi cài đặt:
- Kiểm tra hiệu suất: `python3 performance_test.py`
- Điều chỉnh độ nhạy: `python3 sensitivity_test.py`
- Bỏ gỡ lỗi: `bash debug.sh`
- Có vấn đề: `python3 analyze_log.py`

---

**Tệp này được tạo tự động. Không chỉnh sửa!**

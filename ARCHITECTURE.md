"""
Triển khai Hệ thống Phát hiện Ngủ gật trên Jetson Nano 4GB

Sơ đồ Kiến trúc:

    📷 CAMERA (CSI/USB)
        ↓
    🎬 FRAME CAPTURE
        ↓
    [eye_detector.py]
        ├→ Phát hiện khuôn mặt (dlib HOG-SVM)
        ├→ Lấy điểm mốc (68 points)
        ├→ Tính EAR (Eye Aspect Ratio)
        └→ Xác định mắt đóng/mở
        ↓
    [DrowsinessDetectionSystem]
        ├→ Theo dõi số khung hình liên tiếp
        ├→ Xác nhận ngủ (N khung hình)
        └→ Ghi log sự kiện
        ↓
    [alert_system.py]
        ├→ Cảnh báo âm thanh 🔊
        ├→ Ghi log 📝
        ├→ Lưu ảnh 📸
        └→ Gửi email/SMS (tuỳ chọn) 📧
        ↓
    📊 OUTPUT
        ├→ Console video
        ├→ Log files
        ├→ Captured frames
        └→ Video file (optional)


## Quy Trình Chi Tiết:

1. KHỞI TẠO (Startup)
   - Mở camera
   - Tải mô hình dlib
   - Cấu hình alert system
   - In thông tin hệ thống

2. LỐI LẠI (Main Loop) - 20 FPS trên Jetson Nano
   Frame 1,2,3...
       ├─ Đọc khung hình từ camera (320x240)
       ├─ Chuyển sang grayscale
       ├─ Phát hiện khuôn mặt
       │   └─ Nếu không → skip khung hình
       ├─ Lấy 68 điểm mốc khuôn mặt
       ├─ Tính EAR:
       │   ├─ Mắt trái: avg(p2-p6, p3-p5) / (p1-p4)
       │   └─ Mắt phải: avg(p3-p7, p4-p6) / (p2-p5)
       ├─ So sánh với ngưỡng (0.2)
       │   ├─ EAR > 0.2 → Mắt mở ✓
       │   └─ EAR < 0.2 → Mắt đóng ⭕
       └─ Cập nhật bộ đếm khung hình đóng mắt

3. PHÁT HIỆN NGỦ
   - Kiểm tra: consecutive_closed_frames >= 20
   - Nếu đúng → Phát hiện ngủ
   - Kích hoạt alert
   - Lưu ảnh

4. DỪNG (Cleanup)
   - Giải phóng camera
   - Đóng file log
   - Giải phóng bộ nhớ


## Dòng Chảy Dữ Liệu:

Camera Input → Frame Processing → Feature Extraction
                                        ↓
                                EAR Calculation
                                        ↓
                                Drowsiness Logic
                                        ↓
                         Alert & Logging System
                                        ↓
                            Output (Video/Files/Log)


## Tối Ưu Hóa cho Jetson Nano:

✓ Độ phân giải thấp (320x240 thay vì 1920x1080)
✓ FPS vừa phải (20 fps thay vì 30fps)
✓ Thuật toán nhẹ (dlib HOG-SVM nhẹ hơn CNN)
✓ Không sử dụng GPU (dlib optimized cho CPU)
✓ Bỏ qua khung hình nếu không detect mặt
✓ Không lưu video mặc định
✓ Logging hiệu quả


## Chi Phí Tài Nguyên (Ước tính):

CPU:    ~40-60% (một core)
Memory: ~100-150 MB
Storage: ~50 MB (code + model)
FPS:    15-20 fps ổn định

Lưu ý: Tuỳ thuộc vào:
- Camera resolution & FPS
- Độ phức tạp hình ảnh
- Số mặt trong khung hình
- Các tiến trình nền khác


## Cải Thiện Hiệu Năng (Future):

1. GPU Acceleration
   - NVIDIA TensorRT
   - CUDA optimization
   - Dự kiến +50% tốc độ

2. Mô hình Tốt hơn
   - MediaPipe (30% nhanh hơn)
   - Quantized models
   - Edge TPU

3. Thuật toán Tuyên tinh
   - Tracking làm mượt
   - Multi-face support
   - Temporal smoothing


---
Xem thêm: README.md, DEVELOPMENT.md
"""

# Tệp này chỉ là để tài liệu

"""
Triển khai Hệ thống Phát hiện Ngủ gật trên Jetson Nano 4GB

Sơ đồ Kiến trúc:

    📷 CAMERA (CSI/USB)
        ↓
    🎬 FRAME CAPTURE
        ↓
    ┌─────────────────────────────────────────────────┐
    │ Phát hiện Khuôn Mặt & Lấy 68 Điểm Mốc (dlib)   │
    └─────────────────────────────────────────────────┘
        ↓
    ┌──────────────────┬──────────────────┬──────────────────┐
    ↓                  ↓                  ↓                  ↓
[eye_detector.py] [yawn_detector.py] [posture_detector.py] [landmarks]
├─ Tính EAR      ├─ Tính MAR      ├─ Head Roll       
├─ Mắt đóng/mở   ├─ Ngáp?         ├─ Head Pitch      
└─ Status        └─ is_yawning    ├─ Forward Head    
                                   └─ is_bad_posture
        ↓                  ↓                  ↓
    ┌─────────────────────────────────────────────────┐
    │ [DrowsinessDetectionSystem]                     │
    │ - Tổng hợp tất cả kết quả phát hiện            │
    │ - Theo dõi số khung hình liên tiếp              │
    │ - Xác nhận ngủ/ngáp/tư thế xấu                  │
    │ - Ghi log sự kiện đầy đủ                        │
    └─────────────────────────────────────────────────┘
        ↓
    [alert_system.py]
        ├→ Cảnh báo âm thanh 🔊 (khi ngủ/ngáp/tư thế)
        ├→ Ghi log 📝
        ├→ Lưu ảnh 📸
        └→ Gửi email/SMS (tuỳ chọn) 📧
        ↓
    📊 OUTPUT
        ├→ Console video (với overlay thông tin)
        ├→ Log files (đầy đủ thông tin sự kiện)
        ├→ Captured frames (ảnh cảnh báo)
        └→ Video file (tuỳ chọn)


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
       │
       ├─ [PHÁT HIỆN MẮT] Tính EAR (Eye Aspect Ratio):
       │   ├─ Mắt trái: avg(p2-p6, p3-p5) / (p1-p4)
       │   └─ Mắt phải: avg(p3-p7, p4-p6) / (p2-p5)
       │   └─ Kết quả: Mắt mở/đóng, cập nhật counter
       │
       ├─ [PHÁT HIỆN NGÁP] Tính MAR (Mouth Aspect Ratio):
       │   └─ MAR = (||p2-p5|| + ||p3-p4||) / (2 * ||p1-p6||)
       │   └─ So sánh với ngưỡng (0.5) → Ngáp hay không
       │
       └─ [PHÁT HIỆN TƯ THẾ] Tính chỉ số đầu:
           ├─ Head Roll (lệch ngang): góc giữa 2 mắt
           ├─ Head Pitch (cúi/nâng): góc giữa mũi-cằm
           └─ Forward Head (cúi phía trước): tỷ lệ khoảng cách

3. PHÁT HIỆN & KÍCH HOẠT ALERT
   
   a) PHÁT HIỆN NGỦ:
      - Kiểm tra: consecutive_closed_frames >= 20
      - Nếu đúng → Kích hoạt cảnh báo ngủ
   
   b) PHÁT HIỆN NGÁP:
      - Kiểm tra: consecutive_yawn_frames >= 10
      - Nếu đúng → Ghi log ngáp (cảnh báo nhẹ)
   
   c) PHÁT HIỆN TƯ THẾ XẤU:
      - Kiểm tra: consecutive_bad_posture_frames >= 15
      - Nếu đúng → Kích hoạt cảnh báo tư thế
   
   d) KÍCH HOẠT ALERT:
      - Phát âm thanh cảnh báo 🔊
      - Ghi log chi tiết sự kiện
      - Lưu ảnh hiện tại 📸
      - Gửi email/SMS (nếu cấu hình)

4. DỪNG (Cleanup)
   - Giải phóng camera
   - Đóng file log
   - Giải phóng bộ nhớ


## Dòng Chảy Dữ Liệu:

Camera Input → Face Detection → 68 Landmarks
                                    ↓
        ┌───────────────────┬──────────────────┬────────────────┐
        ↓                   ↓                  ↓                ↓
    EAR (Eye)          MAR (Yawn)        Head Angles (Posture) 
        ↓                   ↓                  ↓
  counter_eye         counter_yawn      counter_posture
        ↓                   ↓                  ↓
    └───────────────────┬──────────────────┬────────────────┘
                        ↓
              Decision Logic & Alerts
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

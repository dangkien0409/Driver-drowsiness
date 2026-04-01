# Hướng dẫn sử dụng các tính năng mới - Nhận diện Ngáp & Tư thế

## Các tính năng mới được thêm vào

### 1. **Nhận diện Ngáp** (Yawn Detection)
- Sử dụng **Mouth Aspect Ratio (MAR)** để phát hiện khi tài xế ngáp
- Dựa trên việc phân tích độ mở của miệng qua 68 điểm mốc khuôn mặt
- **Công thức MAR**: `MAR = (distance1 + distance2) / (2 * width)`

**Thông số cấu hình:**
```python
MOUTH_AR_THRESHOLD = 0.5      # Ngưỡng tỷ lệ mở miệng (càng nhỏ càng dễ phát hiện)
YAWN_CONSEC_FRAMES = 10       # Số khung liên tiếp để xác nhận ngáp (giảm = nhạy hơn)
```

### 2. **Phát hiện Tư thế Tài xế** (Posture Detection)
Hệ thống phát hiện 3 loại tư thế không an toàn:

**a) Nghiêng đầu (Head Roll)**
- Phát hiện khi tài xế nghiêng đầu sang hai bên
- Sử dụng góc giữa hai mắt

**b) Cúi/Nâng đầu (Head Pitch)**
- Phát hiện khi tài xế cúi đầu xuống hoặc nâng đầu lên quá cao
- Sử dụng góc giữa mũi và cằm

**c) Tư thế cúi phía trước (Forward Head Posture)**
- Phát hiện khi tài xế cúi đầu sâu vào
- Dựa trên tỷ lệ khoảng cách giữa các điểm khuôn mặt

**Thông số cấu hình:**
```python
HEAD_ROLL_THRESHOLD = 15              # Góc lệch ngang tối đa (độ)
HEAD_PITCH_THRESHOLD = 20             # Góc tilt dọc tối đa (độ)
FORWARD_HEAD_THRESHOLD = 1.5          # Ngưỡng tư thế cúi (tỷ lệ)
POSTURE_CONSEC_FRAMES = 15            # Số khung để xác nhận tư thế xấu
```

## Cấu trúc Module

### 1. `yawn_detector.py`
- **Class `YawnDetector`**: Phát hiện ngáp
- **Phương thức chính:**
  - `detect_yawn()`: Phát hiện ngáp từ landmarks
  - `mouth_aspect_ratio()`: Tính MAR
  - `draw_mouth()`: Vẽ miệng trên video

### 2. `posture_detector.py`
- **Class `PostureDetector`**: Phát hiện tư thế
- **Phương thức chính:**
  - `detect_posture()`: Phát hiện tư thế xấu
  - `calculate_head_roll()`: Tính góc lệch ngang
  - `calculate_head_pitch()`: Tính góc tilt dọc
  - `calculate_forward_head_position()`: Tính chỉ số cúi
  - `draw_posture_info()`: Vẽ thông tin tư thế

### 3. `main.py` (được cập nhật)
- Tích hợp cả 3 bộ phát hiện: mắt, ngáp, tư thế
- Xử lý từng khung hình và hiển thị kết quả tổng hợp

## Cách sử dụng

### Chạy với cấu hình mặc định:
```bash
python main.py
```

### Chạy với tuỳ chỉnh ngưỡng:
```bash
# Tuỳ chỉnh ngưỡng ngáp (MAR)
python main.py --yawn-threshold 0.4

# Tuỳ chỉnh ngưỡng góc đầu
python main.py --posture-threshold 20

# Tuỳ chỉnh ngưỡng mắt
python main.py --threshold 0.25

# Kết hợp nhiều thông số
python main.py --threshold 0.25 --yawn-threshold 0.4 --posture-threshold 18 --frames 25
```

### Tùy chọn khác:
```bash
# Lưu video
python main.py --save-video

# Không hiển thị video (chỉ xử lý)
python main.py --no-display

# Sử dụng camera khác
python main.py --camera 1
```

## Thông tin hiển thị trên màn hình

```
┌─────────────────────────────────────────────────────┐
│ Trang thai: NGU GAT!                                │
│ Khung ngu: 20/20                                    │
│ Ngap: 0.58 ⚠ NGAP                                  │
│ Tu the: Cúi đầu phía trước                          │
│ Khung: 1234                                         │
│                                                     │
│ L-EAR: 0.15 R-EAR: 0.16                            │
│ (+ Vẽ điểm mốc mắt, miệng, và các điểm đặc biệt)  │
└─────────────────────────────────────────────────────┘
```

## Giải thích thông số

| Thông số | Ý nghĩa | Mặc định |
|----------|---------|---------|
| EYE_AR_THRESHOLD | Ngưỡng EAR để phát hiện mắt đóng | 0.2 |
| EYE_AR_CONSEC_FRAMES | Khung liên tiếp để xác nhận ngủ | 20 |
| MOUTH_AR_THRESHOLD | Ngưỡng MAR để phát hiện ngáp | 0.5 |
| YAWN_CONSEC_FRAMES | Khung liên tiếp để xác nhận ngáp | 10 |
| HEAD_ROLL_THRESHOLD | Góc lệch ngang tối đa | 15° |
| HEAD_PITCH_THRESHOLD | Góc tilt dọc tối đa | 20° |
| FORWARD_HEAD_THRESHOLD | Ngưỡng tư thế cúi | 1.5 |
| POSTURE_CONSEC_FRAMES | Khung để xác nhận tư thế xấu | 15 |

## Điểm mốc khuôn mặt được sử dụng

Hệ thống sử dụng **68 điểm mốc khuôn mặt** từ dlib:

| Vùng | Điểm số | Ý nghĩa |
|------|---------|---------|
| **Mắt** | 36-47 | Mắt trái (36-41), Mắt phải (42-47) |
| **Miệng** | 60-67 | Các góc và điểm dọc giữa miệng |
| **Mũi** | 30 | Đầu mũi (tâm điểm) |
| **Cằm** | 8 | Điểm cằm dưới cùng |

## Công thức tính toán

### Eye Aspect Ratio (EAR)
```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
   = (khoảng cách dọc 1 + khoảng cách dọc 2) / (2 * khoảng cách ngang)

Khi mắt bình thường: EAR ≈ 0.4
Khi mắt đóng: EAR < 0.2
```

### Mouth Aspect Ratio (MAR)
```
MAR = (||p2 - p5|| + ||p3 - p4||) / (2 * ||p1 - p6||)
   = (khoảng cách dọc 1 + khoảng cách dọc 2) / (2 * khoảng cách ngang)

Khi miệng bình thường: MAR ≈ 0.3
Khi miệng mở (ngáp): MAR > 0.5
```

## Mẹo điều chỉnh

### Nếu phát hiện ngáp quá nhạy (cảnh báo liên tục):
1. **Tăng `MOUTH_AR_THRESHOLD`** từ 0.5 → 0.6 hoặc 0.7
2. **Tăng `YAWN_CONSEC_FRAMES`** từ 10 → 15 hoặc 20

### Nếu phát hiện tư thế quá nhạy:
1. **Tăng `HEAD_ROLL_THRESHOLD`** từ 15 → 20 hoặc 25
2. **Tăng `HEAD_PITCH_THRESHOLD`** từ 20 → 25 hoặc 30
3. **Tăng `POSTURE_CONSEC_FRAMES`** từ 15 → 20 hoặc 25

### Nếu không phát hiện được dấu hiệu:
1. **Giảm các threshold** xuống dưới giá trị mặc định
2. **Kiểm tra ánh sáng** trong phòng (cần đủ sáng để phát hiện mặt)
3. **Thử camera khác** hoặc điều chỉnh vị trí camera

## Tệp tin liên quan

- `config.py` - Chứa tất cả thông số cấu hình
- `eye_detector.py` - Phát hiện mắt (đã tồn tại)
- `yawn_detector.py` - Phát hiện ngáp (mới)
- `posture_detector.py` - Phát hiện tư thế (mới)
- `main.py` - Tích hợp tất cả (được cập nhật)
- `alert_system.py` - Hệ thống cảnh báo (cần cập nhật cho các tính năng mới)

## Bước tiếp theo

Bạn có thể:
1. **Cập nhật `alert_system.py`** để gửi cảnh báo khác nhau cho các loại phát hiện
2. **Thêm logging** để ghi lại thời gian phát hiện từng dấu hiệu
3. **Huấn luyện mô hình ML** để tăng độ chính xác
4. **Thêm phát hiện khác** như: mỏi mắt, tần suất chớp mắt, vị trí tay, v.v.

---
**Created**: 2026-04-01
**Language**: Vietnamese
**Dependencies**: opencv-python, dlib, scipy, numpy

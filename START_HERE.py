#!/usr/bin/env python3
"""
HƯỚNG DẪN BẮT ĐẦU - Driver Drowsiness Detection (Jetson Nano)
=============================================================

Chào mừng bạn đến với hệ thống phát hiện tài xế lái xe ngủ gật!

Tệp này cung cấp các hướng dẫn từng bước để bắt đầu.
"""

def print_welcome():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚗 DRIVER DROWSINESS DETECTION - JETSON NANO 4GB 🚗       ║
║                                                              ║
║   Hệ thống phát hiện tài xế lái xe ngủ gật sử dụng:          ║
║   • Jetson Nano 4GB                                          ║
║   • Camera USB hoặc CSI                                      ║
║   • Nhận diện khuôn mặt và mắt                               ║
║   • Cảnh báo âm thanh khi phát hiện ngủ                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def print_quick_start():
    print("""
⚡ QUICK START (3 BƯỚC)
═══════════════════════════════════════

Bước 1: Cài đặt
───────────────
  $ chmod +x *.sh *.py
  $ ./setup_jetson.sh
  
  (hoặc thủ công: pip3 install -r requirements.txt)

Bước 2: Tải mô hình
───────────────────
  $ python3 install_dlib_model.py
  
  ⏱️  Lần đầu tiên (~100MB, thường mất 5-10 phút...ở tùy thuộc kết nối internet)

Bước 3: Chạy
────────────
  $ python3 main.py
  
  Hoặc sử dụng menu tương tác:
  $ python3 run.py

✓ Xong! Hệ thống bắt đầu chạy.
    """)

def print_detailed_steps():
    print("""
📖 HƯỚNG DẪN CHI TIẾT
════════════════════════════════════════════════════════════════

1️⃣  CHUẨN BỊ JETSON NANO
───────────────────────────
  • Cài JetPack OS (L4T) trên microSD 64GB+
  • Kết nối camera (USB hoặc CSI)
  • Kết nối internet (WiFi hoặc Ethernet)
  • Nguồn điện 5V/4A USB-C

2️⃣  CLONE DỰ ÁN
────────────────
  $ git clone <repo_url>
  $ cd Driver-drowsiness

3️⃣  CÀI ĐẶT DEPENDENCIES
────────────────────────
  $ chmod +x setup_jetson.sh
  $ ./setup_jetson.sh
  
  Lệnh này sẽ:
  ✓ Cập nhật hệ thống
  ✓ Cài OpenCV, dlib, numpy, scipy
  ✓ Tạo các thư mục cần thiết

4️⃣  KIỂM TRA HỆ THỐNG
──────────────────────
  $ python3 check_system.py
  
  Đây sẽ kiểm tra:
  ✓ Gói Python
  ✓ Camera
  ✓ Mô hình
  ✓ Thư mục

5️⃣  CHẠY HỆ THỐNG
──────────────────
  
  Chế độ 1: Hiển thị video
  $ python3 main.py
  
  Chế độ 2: Không hiển thị (nền)
  $ python3 main.py --no-display
  
  Chế độ 3: Lưu video
  $ python3 main.py --save-video
  
  Chế độ 4: Tuỳ chỉnh ngưỡng
  $ python3 main.py --threshold 0.18 --yawn-threshold 0.45 --posture-threshold 18
  $ python3 main.py --save-video
  
  Chế độ 4: Tuỳ chỉnh ngưỡng
  $ python3 main.py --threshold 0.18 --yawn-threshold 0.45 --posture-threshold 18
  $ python3 main.py --save-video
  
  Chế độ 4: Tuỳ chỉnh tham số
  $ python3 main.py --threshold 0.15 --frames 25
  
  Hoặc sử dụng menu tương tác:
  $ python3 run.py

6️⃣  DỪNG HỆ THỐNG
──────────────────
  • Nhấn 'Q' trong cửa sổ video
  • Hoặc Ctrl+C trong terminal
    """)

def print_features():
    print("""
✨ TÍNH NĂNG CHÍNH
═════════════════════════════════════════================================

👁️  PHÁT HIỆN MẮT
  • Sử dụng Eye Aspect Ratio (EAR)
  • Phát hiện mũi tên mắt
  • Hỗ trợ cả hai mắt (trái + phải)

⚠️  CẢNH BÁO
  • Âm thanh cảnh báo 🔊
  • Ghi log sự kiện 📝
  • Gửi email (tuỳ chọn) 📧
  • Gửi SMS (tuỳ chọn) 📱

📊 THEO DÕI
  • Tính EAR thực thời
  • Số khung hình liên tiếp
  • FPS
  • Thời gian xử lý

🎥 LƯU TRỮ
  • Lưu khung hình khi ngủ 📸
  • Lưu video đầu ra (tuỳ chọn)
  • Ghi log chi tiết 📋

⚙️  TỐI ƯU
  • Chạy ổn định trên Jetson Nano
  • Độ phân giải thấp (320x240)
  • FPS cao (15-20)
  • Tiêu thụ ít bộ nhớ
    """)

def print_commands():
    print("""
💻 CÁC LỆNH THƯỜNG DÙNG
════════════════════════════════════════════════════════════════

Chạy hệ thống
  $ python3 main.py                          # Bình thường
  $ python3 main.py --no-display             # Không hiển thị
  $ python3 main.py --save-video             # Lưu video
  $ python3 main.py --camera 1               # Camera khác
  $ python3 main.py --threshold 0.15         # Độ nhạy khác

Kiểm tra & Thiết lập
  $ python3 check_system.py                  # Kiểm tra hệ thống
  $ python3 performance_test.py              # Kiểm tra hiệu suất
  $ python3 sensitivity_test.py              # Kiểm tra độ nhạy
  $ python3 quickstart.py                    # Quick start

Tiện ích
  $ bash debug.sh                            # Bỏ gỡ lỗi
  $ python3 analyze_log.py                   # Phân tích log
  $ make help                                # Xem makefile commands

Cài đặt dịch vụ (Tự động chạy khi boot)
  $ sudo bash install_service.sh             # Cài systemd service
  $ sudo systemctl start drowsiness-detection
  $ sudo systemctl stop drowsiness-detection
  $ sudo systemctl status drowsiness-detection
    """)

def print_troubleshooting():
    print("""
🔧 KHẮC PHỤC SỰ CỐ
═════════════════════════════════════════════════════════════════

❌ Lỗi: "Cannot open camera"
✓ Giải pháp:
  $ ls -la /dev/video*              # Kiểm tra camera
  $ sudo usermod -a -G video $USER  # Cấp quyền
  $ logout && login                 # Đăng nhập lại

❌ Lỗi: "dlib model not found"
✓ Giải pháp:
  $ python3 install_dlib_model.py   # Tải mô hình
  
  Nếu có lỗi kết nối:
  - Tài liệu tải thủ công: 
    http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
  - Giải nén: bzip2 -d file.dat.bz2
  - Đặt vào: models/shape_predictor_68_face_landmarks.dat

❌ Lỗi: "Module not found" (numpy, opencv, v.v.)
✓ Giải pháp:
  $ pip3 install -r requirements.txt
  $ python3 check_system.py         # Kiểm tra lại

❌ Lỗi: FPS thấp hoặc hiệu suất kém
✓ Giải pháp:
  - Giảm độ phân giải: Sửa CAMERA_WIDTH, CAMERA_HEIGHT trong config.py
  - Tắt hiển thị: python3 main.py --no-display
  - Tắt lưu video
  - Chạy: python3 performance_test.py để kiểm tra

❌ Lỗi: "Out of memory"
✓ Giải pháp:
  - Giảm độ phân giải camera
  - Tắt lưu video
  - Tắt các ứng dụng khác
  - Kiểm tra: free -h

❌ Lỗi: Camera không hoạt động (CSI camera)
✓ Giải pháp:
  $ sudo nano /boot/firmware/config.txt
  # Thêm: dtoverlay=imx219
  $ sudo reboot

📞 Cần giúp đỡ thêm?
  - Xem log: tail -f logs/drowsiness_detection.log
  - Phân tích log: python3 analyze_log.py
  - Tài liệu: README.md, DEVELOPMENT.md
    """)

def print_tips():
    print("""
💡 MẸO & THỦ THUẬT
═════════════════════════════════════════════════════════════════

🎯 Tối ưu hóa Độ nhạy
  • EAR thấp → Nhạy hơn (dễ cảnh báo nhầm)
  • EAR cao → Ít nhạy (có thể bỏ sót)
  • Giá trị tối ưu: 0.18-0.22
  • Kiểm tra: python3 sensitivity_test.py

🎥 Camera Tốt Nhất
  • CSI Camera: Tốc độ cao, ít độ trễ
  • USB Camera 1080p: Chuẩn, nhưng FPS thấp hơn
  • USB Camera 640x480: Cân bằng tốt

📊 Giám Sát Trong Quá Trình Chạy
  # Terminal 1: Chạy hệ thống
  $ python3 main.py
  
  # Terminal 2: Theo dõi log
  $ tail -f logs/drowsiness_detection.log
  
  # Terminal 3: Kiểm tra tài nguyên
  $ watch -n 1 'free -h && echo && top -b -n1 | head -15'

🔔 Tùy chỉnh Cảnh báo
  • Sửa alert_system.py để tùy chỉnh cảnh báo
  • Thêm email alert: Sửa send_email_alert()
  • Thêm SMS alert: Thêm Twilio API

🚀 Chạy Trong Background
  $ nohup python3 main.py --no-display > output.log 2>&1 &
  $ jobs
  $ bg
  $ fg

⚡ Tự động Khởi Động
  $ sudo bash install_service.sh
  $ sudo systemctl enable drowsiness-detection

🐛 Kiểm Tra Log
  $ python3 analyze_log.py
  $ bash debug.sh
    """)

def print_files_info():
    print("""
📂 HƯỚNG DẪN FILE
════════════════════════════════════════════════════════════════

Chương Trình Chính
  • main.py                      # Chạy cái này! 🎯
  • config.py                    # Sửa cấu hình tại đây
  • eye_detector.py              # Logic phát hiện
  • alert_system.py              # Logic cảnh báo

Công Cụ Hữu Ích
  • run.py                       # Menu tương tác 📋
  • check_system.py              # Kiểm tra setup ✓
  • performance_test.py          # Kiểm tra FPS 📊
  • sensitivity_test.py          # Kiểm tra độ nhạy 🎯
  • quickstart.py                # Quick start 🚀

Cài Đặt
  • setup_jetson.sh              # Cài đặt toàn bộ 🔧
  • requirements.txt             # Dependencies 📦
  • Makefile                     # Quick commands 🎯

Dịch Vụ (Optional)
  • install_service.sh           # Cài systemd service
  • drowsiness-detection.service # Service definition

Tài Liệu
  • README.md                    # Tài liệu chi tiết 📚
  • QUICK_SUMMARY.md             # Tóm tắt 1 trang ⚡
  • ARCHITECTURE.md              # Sơ đồ kiến trúc 🏗️
  • DEVELOPMENT.md               # Hướng dẫn phát triển 🚀
    """)

def main():
    """Hàm chính"""
    print_welcome()
    
    while True:
        print("""
┌──────────────────────────────────────────────────────────┐
│          CHỌN MỤC TÌM HIỂU THÊM (hoặc nhấn Q thoát)      │
├──────────────────────────────────────────────────────────┤
│  1. Quick Start (3 bước cơ bản)                          │
│  2. Hướng dẫn Chi Tiết (từng bước dễ hiểu)               │
│  3. Các Tính Năng                                        │
│  4. Lệnh Thường Dùng                                     │
│  5. Khắc Phục Sự Cố                                      │
│  6. Mẹo & Thủ Thuật                                      │
│  7. Hướng Dẫn File                                       │
│  Q. Thoát                                                │
└──────────────────────────────────────────────────────────┘

Chọn (1-7 hoặc Q): """)
        
        choice = input().strip().upper()
        
        if choice == '1':
            print_quick_start()
        elif choice == '2':
            print_detailed_steps()
        elif choice == '3':
            print_features()
        elif choice == '4':
            print_commands()
        elif choice == '5':
            print_troubleshooting()
        elif choice == '6':
            print_tips()
        elif choice == '7':
            print_files_info()
        elif choice == 'Q':
            print("\n👋 Chúc bạn thành công! (Nhớ chạy: python3 main.py)\n")
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ! Vui lòng thử lại.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tạm biệt!\n")

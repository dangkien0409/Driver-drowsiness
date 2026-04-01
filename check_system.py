#!/usr/bin/env python3
"""
Script kiểm tra camera và thiết lập hệ thống trên Jetson Nano
"""

import cv2
import sys
import os

def check_camera():
    """Kiểm tra camera có sẵn hay không"""
    print("\n📹 Kiểm tra Camera:")
    print("-" * 50)
    
    for camera_id in range(5):
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            print(f"✓ Camera {camera_id} được phát hiện:")
            print(f"  - Độ phân giải: {width}x{height}")
            print(f"  - FPS: {fps}")
            
            # Chụp một khung hình để kiểm tra
            ret, frame = cap.read()
            if ret:
                print(f"  - Đang hoạt động: ✓")
            else:
                print(f"  - Đang hoạt động: ✗ (không thể đọc khung hình)")
            
            cap.release()
        elif camera_id == 0:
            print(f"✗ Không tìm thấy camera mặc định (ID: 0)")

def check_python_packages():
    """Kiểm tra các gói Python cần thiết"""
    print("\n📦 Kiểm tra Gói Python:")
    print("-" * 50)
    
    required_packages = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'dlib': 'dlib',
        'imutils': 'imutils'
    }
    
    for package_name, display_name in required_packages.items():
        try:
            __import__(package_name)
            print(f"✓ {display_name}")
        except ImportError:
            print(f"✗ {display_name} - Chưa cài đặt")

def check_dlib_model():
    """Kiểm tra mô hình dlib"""
    print("\n🧠 Kiểm tra Mô hình dlib:")
    print("-" * 50)
    
    model_path = "models/shape_predictor_68_face_landmarks.dat"
    
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"✓ Mô hình tìm thấy: {model_path}")
        print(f"  - Kích thước: {size_mb:.1f} MB")
    else:
        print(f"✗ Mô hình không tìm thấy: {model_path}")
        print(f"  Hãy chạy: python3 install_dlib_model.py")

def check_directories():
    """Kiểm tra và tạo các thư mục cần thiết"""
    print("\n📁 Kiểm tra Thư mục:")
    print("-" * 50)
    
    directories = ['models', 'logs', 'captured_frames', 'sounds']
    
    for dir_name in directories:
        if os.path.exists(dir_name):
            print(f"✓ Thư mục '{dir_name}' tồn tại")
        else:
            print(f"✗ Thư mục '{dir_name}' không tồn tại")
            print(f"  Tạo thư mục...")
            os.makedirs(dir_name)
            print(f"  ✓ Đã tạo")

def print_summary():
    """In tóm tắt kiểm tra"""
    print("\n" + "=" * 50)
    print("📋 KIỂM TRA HỆ THỐNG HOÀN TẤT")
    print("=" * 50)
    print("\nNếu tất cả các mục đều ✓, bạn có thể:")
    print("  python3 main.py")
    print("\nNếu có ✗, hãy:")
    print("  1. Chạy: ./setup_jetson.sh (cài đặt gói)")
    print("  2. Chạy: python3 install_dlib_model.py (tải mô hình)")
    print("  3. Kết nối camera USB hoặc CSI camera")

def main():
    """Hàm chính"""
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║   KIỂM TRA HỆ THỐNG PHÁT HIỆN NGỦ GẬT        ║")
    print("║        Jetson Nano 4GB                        ║")
    print("╚════════════════════════════════════════════════╝")
    
    # Thực hiện các kiểm tra
    check_python_packages()
    check_directories()
    check_dlib_model()
    check_camera()
    
    # In tóm tắt
    print_summary()
    print()

if __name__ == "__main__":
    main()

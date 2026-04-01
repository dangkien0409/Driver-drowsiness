#!/usr/bin/env python3
"""
QUICK START - Bắt đầu nhanh hệ thống phát hiện ngủ gật
Chương trình này hướng dẫn bạn qua các bước khởi tạo
"""

import os
import sys
import subprocess

def run_command(command, description=""):
    """Chạy lệnh shell"""
    if description:
        print(f"\n📝 {description}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Thành công")
            return True
        else:
            print(f"✗ Lỗi: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║   QUICK START - BẮT ĐẦU NHANH                 ║")
    print("║   Phát hiện Ngủ gật - Jetson Nano             ║")
    print("╚════════════════════════════════════════════════╝")
    
    steps = [
        (
            "python3 check_system.py",
            "Bước 1: Kiểm tra cấu hình hệ thống"
        ),
        (
            "python3 install_dlib_model.py",
            "Bước 2: Tải mô hình phát hiện mặt"
        ),
        (
            "python3 performance_test.py --duration 10 --frames 20",
            "Bước 3: Kiểm tra hiệu suất (tuỳ chọn)"
        ),
        (
            "python3 main.py",
            "Bước 4: Chạy hệ thống chính"
        )
    ]
    
    print("\n📋 Các bước khởi tạo:\n")
    
    for i, (command, description) in enumerate(steps, 1):
        print(f"{i}. {description}")
        print(f"   Lệnh: {command}")
    
    print("\n" + "=" * 50)
    print("Bạn có muốn chạy các bước này? (y/n)")
    
    response = input("> ").strip().lower()
    
    if response != 'y':
        print("\nBạn có thể chạy các lệnh trên thủ công.")
        print("Hoặc chạy: ./setup_jetson.sh")
        return
    
    # Chạy các bước
    for command, description in steps:
        success = run_command(command, description)
        
        if not success and "Bước 2" in description:
            print("⚠️  Lỗi tải mô hình. Vui lòng kiểm tra kết nối internet.")
            print("Bạn có thể tải thủ công từ: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
            continue
        
        if command.strip().endswith("check_system.py"):
            input("\nNhấn Enter để tiếp tục...")
    
    print("\n" + "=" * 50)
    print("✓ Hoàn tất khởi tạo!")
    print("=" * 50)
    
    print("\n💡 Các lệnh hữu ích:\n")
    print("  python3 main.py                           # Chạy bình thường")
    print("  python3 main.py --no-display              # Không hiển thị (nền)")
    print("  python3 main.py --save-video              # Lưu video")
    print("  python3 main.py --threshold 0.15          # Thay đổi độ nhạy")
    print("  python3 sensitivity_test.py                # Kiểm tra độ nhạy")
    
    print("\n📚 Xem thêm:")
    print("  - README.md            : Tài liệu chính")
    print("  - DEVELOPMENT.md       : Hướng dẫn nâng cấp")
    print("  - CONTRIBUTING.md      : Cách đóng góp")
    
    print("\n")

if __name__ == "__main__":
    main()

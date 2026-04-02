#!/usr/bin/env python3
"""
Script để đơn giản hóa việc chạy hệ thống trên Jetson Nano
Menu tương tác để chọn các tùy chọn chạy
"""

import subprocess
import sys

def print_menu():
    """In menu"""
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║   DRIVER DROWSINESS DETECTION                  ║")
    print("║   Jetson Nano 4GB                              ║")
    print("╚════════════════════════════════════════════════╝")
    print("\n📋 Các tùy chọn:")
    print("  1. Chạy bình thường (hiển thị video)")
    print("  2. Chạy nền (không hiển thị)")
    print("  3. Chạy và lưu video")
    print("  4. Kiểm tra hệ thống")
    print("  5. Kiểm tra hiệu suất")
    print("  6. Kiểm tra độ nhạy")
    print("  7. Quick Start (khởi tạo)")
    print("  8. Thoát")
    print("\nChọn (1-8): ", end="")

def get_camera_id():
    """Lấy ID camera từ user"""
    print("ID Camera (mặc định: 0): ", end="")
    camera_id = input().strip()
    return camera_id if camera_id.isdigit() else "0"

def get_threshold():
    """Lấy ngưỡng từ user"""
    print("Ngưỡng EAR (mặc định: 0.2): ", end="")
    threshold = input().strip()
    try:
        return float(threshold)
    except:
        return 0.2

def run_command(command):
    """Chạy lệnh"""
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print("\n⏹️  Dừng...")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def main():
    """Hàm chính"""
    
    while True:
        print_menu()
        choice = input().strip()
        
        if choice == "1":
            # Chạy bình thường
            print("\n▶️  Chạy hệ thống...")
            camera_id = get_camera_id()
            threshold = get_threshold()
            command = f"python3 main.py --camera {camera_id} --threshold {threshold}"
            run_command(command)
        
        elif choice == "2":
            # Chạy nền
            print("\n▶️  Chạy hệ thống (nền)...")
            camera_id = get_camera_id()
            threshold = get_threshold()
            command = f"python3 main.py --camera {camera_id} --threshold {threshold} --no-display"
            run_command(command)
        
        elif choice == "3":
            # Chạy và lưu video
            print("\n▶️  Chạy hệ thống (lưu video)...")
            camera_id = get_camera_id()
            threshold = get_threshold()
            command = f"python3 main.py --camera {camera_id} --threshold {threshold} --save-video"
            run_command(command)
        
        elif choice == "4":
            # Kiểm tra hệ thống
            print("\n🔍 Kiểm tra hệ thống...")
            run_command("python3 check_system.py")
        
        elif choice == "5":
            # Kiểm tra hiệu suất
            print("\n📊 Kiểm tra hiệu suất...")
            camera_id = get_camera_id()
            run_command(f"python3 performance_test.py --camera {camera_id}")
        
        elif choice == "6":
            # Kiểm tra độ nhạy
            print("\n🎯 Kiểm tra độ nhạy...")
            camera_id = get_camera_id()
            run_command(f"python3 sensitivity_test.py --camera {camera_id}")
        
        elif choice == "7":
            # Quick Start
            print("\n🚀 Quick Start...")
            run_command("python3 quickstart.py")
        
        elif choice == "8":
            # Thoát
            print("\n👋 Tạm biệt!")
            sys.exit(0)
        
        else:
            print("\n❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tạm biệt!")

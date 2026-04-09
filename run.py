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
    print("║   (Mắt + Ngáp + Tư thế)                        ║")
    print("╚════════════════════════════════════════════════╝")
    print("\n📋 Các tùy chọn:")
    print("  1. Chạy bình thường (hiển thị video)")
    print("  2. Chạy nền (không hiển thị)")
    print("  3. Chạy và lưu video")
    print("  4. Kiểm tra hệ thống")
    print("  5. Kiểm tra hiệu suất")
    print("  6. Kiểm tra độ nhạy")
    print("  7. Quick Start (khởi tạo)")
    print("  8. Xem tài liệu")
    print("  9. Thoát")
    print("\nChọn (1-9): ", end=""))

def get_camera_id():
    """Lấy ID camera từ user"""
    print("ID Camera (mặc định: 0): ", end="")
    camera_id = input().strip()
    return camera_id if camera_id.isdigit() else "0"

def get_thresholds():
    """Lấy các ngưỡng từ user"""
    print("\nNgưỡng phát hiện (để trống = mặc định):")
    
    print("  Ngưỡng EAR (mắt, mặc định: 0.2): ", end="")
    ear_threshold = input().strip()
    ear_threshold = float(ear_threshold) if ear_threshold else "0.2"
    
    print("  Ngưỡng MAR (ngáp, mặc định: 0.5): ", end="")
    mar_threshold = input().strip()
    mar_threshold = float(mar_threshold) if mar_threshold else "0.5"
    
    print("  Ngưỡng tư thế (mặc định: 15): ", end="")
    posture_threshold = input().strip()
    posture_threshold = float(posture_threshold) if posture_threshold else "15"
    
    return ear_threshold, mar_threshold, posture_threshold

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
            ear_threshold, mar_threshold, posture_threshold = get_thresholds()
            command = f"python3 main.py --camera {camera_id} --threshold {ear_threshold} --yawn-threshold {mar_threshold} --posture-threshold {posture_threshold}"
            run_command(command)
        
        elif choice == "2":
            # Chạy nền
            print("\n▶️  Chạy hệ thống (nền)...")
            camera_id = get_camera_id()
            ear_threshold, mar_threshold, posture_threshold = get_thresholds()
            command = f"python3 main.py --camera {camera_id} --threshold {ear_threshold} --yawn-threshold {mar_threshold} --posture-threshold {posture_threshold} --no-display"
            run_command(command)
        
        elif choice == "3":
            # Chạy và lưu video
            print("\n▶️  Chạy hệ thống (lưu video)...")
            camera_id = get_camera_id()
            ear_threshold, mar_threshold, posture_threshold = get_thresholds()
            command = f"python3 main.py --camera {camera_id} --threshold {ear_threshold} --yawn-threshold {mar_threshold} --posture-threshold {posture_threshold} --save-video"
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
            # Xem tài liệu
            print("\n📖 Xem tài liệu...")
            print("\n  📚 Tài liệu chính: README.md")
            print("  🏗️  Kiến trúc: ARCHITECTURE.md")
            print("  🎯 Ngáp & Tư thế: YAWN_POSTURE_GUIDE.md")
            print("  ⚡ Bắt đầu nhanh: QUICK_SUMMARY.md")
        
        elif choice == "9":
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

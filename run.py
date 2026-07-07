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
    print("║   (Mat + Ngap)                                 ║")
    print("╚════════════════════════════════════════════════╝")
    print("\n📋 Cac tuy chon:")
    print("  1. Chay binh thuong (hien thi video)")
    print("  2. Chay nen (khong hien thi)")
    print("  3. Chay va luu video")
    print("  4. Kiem tra he thong")
    print("  5. Kiem tra hieu suat")
    print("  6. Kiem tra do nhay")
    print("  7. Quick Start (khoi tao)")
    print("  8. Xem tai lieu")
    print("  9. Thoat")
    print("\nChon (1-9): ", end="")

def get_camera_id():
    """Lấy ID camera từ user"""
    print("ID Camera (mac dinh: 0): ", end="")
    camera_id = input().strip()
    return camera_id if camera_id.isdigit() else "0"

def get_thresholds():
    """Lấy các ngưỡng từ user"""
    print("\nNguong phat hien (de trong = mac dinh):")
    
    print("  Nguong EAR (mat, mac dinh: 0.2): ", end="")
    ear_threshold = input().strip()
    ear_threshold = float(ear_threshold) if ear_threshold else "0.2"
    
    print("  Nguong MAR (ngap, mac dinh: 0.5): ", end="")
    mar_threshold = input().strip()
    mar_threshold = float(mar_threshold) if mar_threshold else "0.5"
    
    return ear_threshold, mar_threshold

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
            print("\n▶️  Chay he thong...")
            camera_id = get_camera_id()
            ear_threshold, mar_threshold = get_thresholds()
            command = f"python3 main.py --camera {camera_id} --threshold {ear_threshold} --yawn-threshold {mar_threshold}"
            run_command(command)
        
        elif choice == "2":
            # Chạy nền
            print("\n▶️  Chay he thong (nen)...")
            camera_id = get_camera_id()
            ear_threshold, mar_threshold = get_thresholds()
            command = f"python3 main.py --camera {camera_id} --threshold {ear_threshold} --yawn-threshold {mar_threshold} --no-display"
            run_command(command)
        
        elif choice == "3":
            # Chạy và lưu video
            print("\n▶️  Chay he thong (luu video)...")
            camera_id = get_camera_id()
            ear_threshold, mar_threshold = get_thresholds()
            command = f"python3 main.py --camera {camera_id} --threshold {ear_threshold} --yawn-threshold {mar_threshold} --save-video"
            run_command(command)
        
        elif choice == "4":
            # Kiểm tra hệ thống
            print("\n🔍 Kiem tra he thong...")
            run_command("python3 check_system.py")
        
        elif choice == "5":
            # Kiểm tra hiệu suất
            print("\n📊 Kiem tra hieu suat...")
            camera_id = get_camera_id()
            run_command(f"python3 performance_test.py --camera {camera_id}")
        
        elif choice == "6":
            # Kiểm tra độ nhạy
            print("\n🎯 Kiem tra do nhay...")
            camera_id = get_camera_id()
            run_command(f"python3 sensitivity_test.py --camera {camera_id}")
        
        elif choice == "7":
            # Quick Start
            print("\n🚀 Quick Start...")
            run_command("python3 quickstart.py")
        
        elif choice == "8":
            # Xem tài liệu
            print("\n📖 Xem tai lieu...")
            print("\n  📚 Tai lieu chinh: README.md")
            print("  🏗️  Kien truc: ARCHITECTURE.md")
            print("  🎯 Yawn Detection: YAWN_POSTURE_GUIDE.md")
            print("  ⚡ Bat dau nhanh: QUICK_SUMMARY.md")
        
        elif choice == "9":
            # Thoát
            print("\n👋 Tam biet!")
            sys.exit(0)
        
        else:
            print("\n❌ Lua chon khong hop le!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tam biet!")

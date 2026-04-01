#!/usr/bin/env python3
"""
Script kiểm tra hiệu suất hệ thống trên Jetson Nano
Giúp tối ưu hóa cấu hình cho hiệu suất tốt nhất
"""

import cv2
import time
import numpy as np
from eye_detector import EyeDetector
import argparse

class PerformanceTest:
    """Lớp kiểm tra hiệu suất"""
    
    def __init__(self):
        self.eye_detector = EyeDetector()
        self.frame_times = []
        self.detection_times = []
    
    def test_camera_fps(self, camera_id=0, duration=10, resolution=(320, 240)):
        """
        Kiểm tra tốc độ camera (FPS)
        
        Args:
            camera_id: ID camera
            duration: Thời gian kiểm tra (giây)
            resolution: Tuple (width, height)
        """
        print(f"\n📹 Kiểm tra FPS Camera:")
        print("-" * 50)
        
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        
        if not cap.isOpened():
            print(f"✗ Không thể mở camera {camera_id}")
            return 0
        
        frame_count = 0
        start_time = time.time()
        
        print(f"Đang đo FPS trong {duration} giây...")
        
        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if ret:
                frame_count += 1
            else:
                break
        
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        
        cap.release()
        
        print(f"✓ FPS trung bình: {fps:.1f}")
        print(f"  - Tổng khung hình: {frame_count}")
        print(f"  - Thời gian: {elapsed_time:.1f}s")
        
        return fps
    
    def test_detection_speed(self, camera_id=0, num_frames=30, resolution=(320, 240)):
        """
        Kiểm tra tốc độ xử lý phát hiện
        
        Args:
            camera_id: ID camera
            num_frames: Số khung hình kiểm tra
            resolution: Tuple (width, height)
        """
        print(f"\n🎯 Kiểm tra Tốc độ Xử lý Phát hiện:")
        print("-" * 50)
        
        cap = cv2.VideoCapture(camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        
        if not cap.isOpened():
            print(f"✗ Không thể mở camera {camera_id}")
            return 0
        
        detection_times = []
        
        print(f"Đang kiểm tra {num_frames} khung hình...")
        
        for i in range(num_frames):
            ret, frame = cap.read()
            if not ret:
                break
            
            start = time.time()
            self.eye_detector.detect_drowsiness(frame)
            detection_time = time.time() - start
            
            detection_times.append(detection_time)
            
            # Tiến độ
            if (i + 1) % 10 == 0:
                print(f"  Đã xử lý: {i + 1}/{num_frames}")
        
        cap.release()
        
        avg_time = np.mean(detection_times)
        max_time = np.max(detection_times)
        min_time = np.min(detection_times)
        fps_equivalent = 1.0 / avg_time if avg_time > 0 else 0
        
        print(f"\n✓ Kết quả:")
        print(f"  - Thời gian trung bình: {avg_time*1000:.1f}ms")
        print(f"  - Thời gian tối thiểu: {min_time*1000:.1f}ms")
        print(f"  - Thời gian tối đa: {max_time*1000:.1f}ms")
        print(f"  - FPS tương đương: {fps_equivalent:.1f}")
        
        return fps_equivalent
    
    def test_memory_usage(self):
        """
        Kiểm tra sử dụng bộ nhớ
        """
        print(f"\n💾 Kiểm tra Sử dụng Bộ nhớ:")
        print("-" * 50)
        
        try:
            import psutil
            
            process = psutil.Process()
            memory_info = process.memory_info()
            
            rss_mb = memory_info.rss / (1024 * 1024)
            vms_mb = memory_info.vms / (1024 * 1024)
            
            print(f"✓ Sử dụng bộ nhớ hiện tại:")
            print(f"  - RSS (Resident Set Size): {rss_mb:.1f} MB")
            print(f"  - VMS (Virtual Memory Size): {vms_mb:.1f} MB")
            
        except ImportError:
            print("⚠️  cần cài psutil: pip3 install psutil")
    
    def print_recommendations(self, fps, detection_fps):
        """
        In các khuyến nghị tối ưu hóa
        
        Args:
            fps: FPS camera
            detection_fps: FPS phát hiện
        """
        print(f"\n💡 Khuyến nghị Tối ưu hóa:")
        print("-" * 50)
        
        if detection_fps < 10:
            print("⚠️  Hiệu suất phát hiện thấp")
            print("   Khuyến nghị:")
            print("   - Giảm độ phân giải camera")
            print("   - Sử dụng --no-display")
            print("   - Tắt lưu video")
        elif detection_fps < 15:
            print("⚠️  Hiệu suất phát hiện trung bình")
            print("   Khuyến nghị:")
            print("   - Xem xét giảm độ phân giải")
        else:
            print("✓ Hiệu suất phát hiện tốt")
        
        if fps < 20:
            print(f"\n⚠️  FPS camera thấp ({fps:.1f})")
            print("   Khuyến nghị:")
            print("   - Kiểm tra camera USB hoặc đặc tính CSI")
            print("   - Thử camera khác nếu có")
        elif fps < 25:
            print(f"\n⚠️  FPS camera vừa ({fps:.1f})")
        else:
            print(f"\n✓ FPS camera tốt ({fps:.1f})")

def main():
    """Hàm chính"""
    parser = argparse.ArgumentParser(description="Kiểm tra hiệu suất Jetson Nano")
    parser.add_argument("--camera", type=int, default=0, help="ID camera")
    parser.add_argument("--duration", type=int, default=10, help="Thời gian kiểm tra FPS (giây)")
    parser.add_argument("--frames", type=int, default=30, help="Số khung hình kiểm tra phát hiện")
    parser.add_argument("--width", type=int, default=320, help="Chiều rộng camera")
    parser.add_argument("--height", type=int, default=240, help="Chiều cao camera")
    
    args = parser.parse_args()
    
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║   KIỂM TRA HIỆU SUẤT JETSON NANO              ║")
    print("╚════════════════════════════════════════════════╝")
    
    tester = PerformanceTest()
    
    # Kiểm tra FPS
    fps = tester.test_camera_fps(
        camera_id=args.camera,
        duration=args.duration,
        resolution=(args.width, args.height)
    )
    
    # Kiểm tra tốc độ phát hiện
    detection_fps = tester.test_detection_speed(
        camera_id=args.camera,
        num_frames=args.frames,
        resolution=(args.width, args.height)
    )
    
    # Kiểm tra bộ nhớ
    tester.test_memory_usage()
    
    # In khuyến nghị
    tester.print_recommendations(fps, detection_fps)
    
    print("\n" + "=" * 50)
    print("Kiểm tra hoàn tất!")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()

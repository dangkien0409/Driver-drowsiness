#!/usr/bin/env python3
"""
Script kiểm tra độ nhạy phát hiện ngủ gật
Thử nghiệm các mức ngưỡng EAR khác nhau
"""

import cv2
import numpy as np
import argparse
from eye_detector import EyeDetector
import time

def test_sensitivity(camera_id=0, duration=30, threshold_range=(0.15, 0.25)):
    """
    Kiểm tra độ nhạy với các ngưỡng khác nhau
    
    Args:
        camera_id: ID camera
        duration: Thời gian kiểm tra (giây)
        threshold_range: Tuple (min_threshold, max_threshold)
    """
    
    eye_detector = EyeDetector()
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"✗ Không thể mở camera {camera_id}")
        return
    
    # Lượng tử hóa các ngưỡng để kiểm tra
    thresholds = np.linspace(threshold_range[0], threshold_range[1], 5)
    results = {th: {'detections': 0, 'frames': 0} for th in thresholds}
    
    print(f"\n🔎 Kiểm tra Độ nhạy trong {duration} giây")
    print("=" * 60)
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Kiểm tra tất cả các ngưỡng
        for threshold in thresholds:
            result = eye_detector.detect_drowsiness(frame, threshold)
            results[threshold]['frames'] += 1
            
            if result['drowsy']:
                results[threshold]['detections'] += 1
    
    cap.release()
    
    # In kết quả
    print(f"\n{'Ngưỡng (EAR)':<15} {'Tỷ lệ phát hiện':<20} {'Số lần':<15}")
    print("-" * 60)
    
    for threshold in thresholds:
        total = results[threshold]['frames']
        detections = results[threshold]['detections']
        
        if total > 0:
            percentage = (detections / total) * 100
            print(f"{threshold:<15.3f} {percentage:<20.1f}% {detections}/{total}")
    
    print("\n💡 Khuyến nghị:")
    print("- Ngưỡng thấp → Nhạy cảm hơn, dễ cảnh báo nhầm")
    print("- Ngưỡng cao → Ít cảnh báo nhầm, có thể bỏ sót")
    print("- Giá trị tối ưu thường: 0.18 - 0.22")

def main():
    """Hàm chính"""
    parser = argparse.ArgumentParser(description="Kiểm tra độ nhạy phát hiện")
    parser.add_argument("--camera", type=int, default=0, help="ID camera")
    parser.add_argument("--duration", type=int, default=30, help="Thời gian kiểm tra (giây)")
    parser.add_argument("--min-threshold", type=float, default=0.15, help="Ngưỡng tối thiểu")
    parser.add_argument("--max-threshold", type=float, default=0.25, help="Ngưỡng tối đa")
    
    args = parser.parse_args()
    
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║   KIỂM TRA ĐỘ NHẠY PHÁT HIỆN                   ║")
    print("║   Jetson Nano - Driver Drowsiness Detection    ║")
    print("╚════════════════════════════════════════════════╝")
    
    test_sensitivity(
        camera_id=args.camera,
        duration=args.duration,
        threshold_range=(args.min_threshold, args.max_threshold)
    )
    
    print("\n")

if __name__ == "__main__":
    main()

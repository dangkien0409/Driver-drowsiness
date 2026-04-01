#!/usr/bin/env python3
"""
Hệ thống phát hiện tài xế lái xe ngủ gật - Jetson Nano
Sử dụng camera để theo dõi mắt và phát hiện ngủ gật
"""

import cv2
import sys
import time
import argparse
from collections import deque
import config
from eye_detector import EyeDetector
from alert_system import AlertSystem

class DrowsinessDetectionSystem:
    """
    Hệ thống phát hiện ngủ gật toàn bộ
    """
    
    def __init__(self, ear_threshold=0.2, consecutive_frames=20):
        """
        Khởi tạo hệ thống
        
        Args:
            ear_threshold: Ngưỡng Eye Aspect Ratio
            consecutive_frames: Số khung hình liên tiếp để phát hiện ngủ
        """
        self.eye_detector = EyeDetector()
        self.alert_system = AlertSystem(config)
        
        self.ear_threshold = ear_threshold
        self.consecutive_frames = consecutive_frames
        self.frame_count = 0
        self.drowsy_frame_count = 0
        
        # Lịch sử EAR để tính trung bình
        self.ear_history = deque(maxlen=10)
        
        # Cấu hình video
        self.cap = None
        self.fps = 0
        self.frame_width = 0
        self.frame_height = 0
    
    def initialize_camera(self, camera_device=0, width=320, height=240, fps=20):
        """
        Khởi tạo camera
        
        Args:
            camera_device: ID thiết bị camera
            width: Chiều rộng khung hình
            height: Chiều cao khung hình
            fps: Tốc độ khung hình
            
        Returns:
            bool: True nếu khởi tạo thành công
        """
        try:
            self.cap = cv2.VideoCapture(camera_device)
            
            # Cài đặt độ phân giải
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.cap.set(cv2.CAP_PROP_FPS, fps)
            
            # Kiểm tra camera có sẵn không
            if not self.cap.isOpened():
                print(f"Lỗi: Không thể mở camera {camera_device}")
                return False
            
            # Lấy thông tin camera
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            print(f"Camera khởi tạo thành công: {self.frame_width}x{self.frame_height} @ {self.fps} FPS")
            
            return True
            
        except Exception as e:
            print(f"Lỗi khi khởi tạo camera: {e}")
            return False
    
    def process_frame(self, frame):
        """
        Xử lý một khung hình
        
        Args:
            frame: Khung hình từ camera
            
        Returns:
            tuple: (frame_with_results, is_drowsy, detection_info)
        """
        self.frame_count += 1
        
        # Phát hiện mắt đóng/mở
        detection_result = self.eye_detector.detect_drowsiness(frame, self.ear_threshold)
        
        # Cập nhật lịch sử EAR
        avg_ear = (detection_result['left_ear'] + detection_result['right_ear']) / 2
        self.ear_history.append(avg_ear)
        
        # Kiểm tra ngủ gật
        is_drowsy = detection_result['drowsy']
        
        if is_drowsy:
            self.drowsy_frame_count += 1
        else:
            self.drowsy_frame_count = 0
        
        # Chỉ xác định là ngủ nếu liên tiếp
        confirmed_drowsy = self.drowsy_frame_count >= self.consecutive_frames
        
        # Vẽ kết quả
        frame_with_results = self.eye_detector.draw_results(frame, detection_result)
        
        # Thêm thông tin thống kê
        status_text = "BINH THUONG" if not confirmed_drowsy else "NGU GAT!"
        color = (0, 255, 0) if not confirmed_drowsy else (0, 0, 255)
        
        cv2.putText(frame_with_results, f"Trang thai: {status_text}", (10, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame_with_results, f"Khung ngu: {self.drowsy_frame_count}/{self.consecutive_frames}", (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(frame_with_results, f"Khung: {self.frame_count}", (10, 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        detection_result['confirmed_drowsy'] = confirmed_drowsy
        
        return frame_with_results, confirmed_drowsy, detection_result
    
    def run(self, camera_device=0, show_video=True, save_video=False):
        """
        Chạy hệ thống phát hiện
        
        Args:
            camera_device: ID thiết bị camera
            show_video: Hiển thị video trực tiếp
            save_video: Lưu video đầu ra
        """
        # Khởi tạo camera
        if not self.initialize_camera(camera_device):
            return
        
        # Khởi tạo video writer (nếu cần)
        out = None
        if save_video:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(config.VIDEO_OUTPUT_PATH, fourcc, self.fps,
                                 (self.frame_width, self.frame_height))
        
        print("Nhấn 'q' để thoát...")
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Lỗi: Không thể đọc khung hình từ camera")
                    break
                
                # Xử lý khung hình
                frame_result, is_drowsy, detection_info = self.process_frame(frame)
                
                # Kích hoạt cảnh báo nếu phát hiện ngủ gật
                if is_drowsy:
                    self.alert_system.trigger_alert(detection_info)
                
                # Lưu các khung hình khi ngủ gật
                if is_drowsy and detection_info.get('faces'):
                    self.alert_system.save_drowsy_frame(frame, detection_info)
                
                # Hiển thị video
                if show_video:
                    cv2.imshow("Driver Drowsiness Detection", frame_result)
                    
                    # Thoát nếu nhấn 'q'
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Lưu video
                if save_video and out:
                    out.write(frame_result)
                
                # Giới hạn tốc độ (tránh tận dụng CPU quá mức)
                time.sleep(0.01)
        
        except KeyboardInterrupt:
            print("\nDừng hệ thống...")
        
        finally:
            # Giải phóng tài nguyên
            if self.cap:
                self.cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()
            
            print(f"Tổng số khung hình xử lý: {self.frame_count}")
            print(f"Tổng lần phát hiện ngủ: {self.drowsy_frame_count}")

def main():
    """Hàm chính"""
    parser = argparse.ArgumentParser(
        description="Hệ thống phát hiện ngủ gật trên Jetson Nano"
    )
    parser.add_argument(
        "--camera", type=int, default=0,
        help="ID thiết bị camera (mặc định: 0)"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.2,
        help="Ngưỡng Eye Aspect Ratio (mặc định: 0.2)"
    )
    parser.add_argument(
        "--frames", type=int, default=20,
        help="Số khung hình liên tiếp để xác định ngủ (mặc định: 20)"
    )
    parser.add_argument(
        "--save-video", action="store_true",
        help="Lưu video đầu ra"
    )
    parser.add_argument(
        "--no-display", action="store_true",
        help="Không hiển thị video (chỉ xử lý nền)"
    )
    
    args = parser.parse_args()
    
    # Tạo và chạy hệ thống
    system = DrowsinessDetectionSystem(
        ear_threshold=args.threshold,
        consecutive_frames=args.frames
    )
    
    system.run(
        camera_device=args.camera,
        show_video=not args.no_display,
        save_video=args.save_video
    )

if __name__ == "__main__":
    main()

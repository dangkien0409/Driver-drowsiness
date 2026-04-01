import cv2
import numpy as np
from scipy.spatial import distance as dist
import dlib

class YawnDetector:
    """
    Lớp phát hiện ngáp dựa trên việc phân tích miệng
    """
    
    def __init__(self, dlib_landmark_path=None):
        """
        Khởi tạo bộ dò ngáp
        
        Args:
            dlib_landmark_path: Đường dẫn đến mô hình dlib landmark
        """
        self.detector = dlib.get_frontal_face_detector()
        
        if dlib_landmark_path:
            self.predictor = dlib.shape_predictor(dlib_landmark_path)
        else:
            try:
                self.predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
            except:
                print("Cảnh báo: Không tìm thấy mô hình dlib landmark.")
                self.predictor = None
        
        # Định nghĩa các chỉ số điểm mốc của dlib cho miệng
        # Miệng: từ điểm 60 đến 67
        self.MOUTH_INDICES = list(range(60, 68))
    
    def mouth_aspect_ratio(self, mouth):
        """
        Tính Mouth Aspect Ratio (MAR) từ tọa độ các điểm mốc của miệng
        MAR = khoảng cách ngang / khoảng cách dọc
        
        Args:
            mouth: Mảng 8x2 chứa tọa độ (x, y) của các điểm mốc miệng
            
        Returns:
            float: Giá trị Mouth Aspect Ratio
        """
        # Khoảng cách dọc của miệng (phía trên)
        A = dist.euclidean(mouth[2], mouth[5])
        # Khoảng cách dọc của miệng (phía dưới)
        B = dist.euclidean(mouth[3], mouth[4])
        # Khoảng cách ngang của miệng
        C = dist.euclidean(mouth[0], mouth[6])
        
        # MAR = (A + B) / (2 * C)
        mar = (A + B) / (2.0 * C)
        
        return mar
    
    def detect_yawn(self, landmarks, mar_threshold=0.5):
        """
        Phát hiện ngáp dựa trên Mouth Aspect Ratio
        
        Args:
            landmarks: Mảng 68x2 chứa tọa độ điểm mốc khuôn mặt
            mar_threshold: Ngưỡng MAR để xác định ngáp
            
        Returns:
            dict: Thông tin phát hiện gồm:
                - 'is_yawning': bool (có phát hiện ngáp hay không)
                - 'mar': float (Mouth Aspect Ratio)
        """
        result = {
            'is_yawning': False,
            'mar': 0.0
        }
        
        if landmarks is None:
            return result
        
        # Lấy tọa độ miệng
        mouth = landmarks[self.MOUTH_INDICES]
        
        # Tính MAR
        mar = self.mouth_aspect_ratio(mouth)
        result['mar'] = mar
        
        # Kiểm tra nếu miệng mở (ngáp)
        if mar > mar_threshold:
            result['is_yawning'] = True
        
        return result
    
    def detect_faces(self, frame):
        """
        Phát hiện khuôn mặt trong khung hình
        
        Args:
            frame: Khung hình từ camera
            
        Returns:
            list: Danh sách các khuôn mặt được phát hiện
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray, 0)
        
        return faces
    
    def get_facial_landmarks(self, frame, face):
        """
        Lấy các điểm mốc khuôn mặt từ dlib
        
        Args:
            frame: Khung hình từ camera
            face: Đối tượng face từ dlib detector
            
        Returns:
            np.ndarray: Mảng chứa tọa độ các điểm mốc (68 điểm)
        """
        if self.predictor is None:
            return None
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        shape = self.predictor(gray, face)
        
        # Chuyển đổi dlib.full_object_detection sang numpy array
        landmarks = np.zeros((68, 2), dtype="int")
        for i in range(0, 68):
            landmarks[i] = (shape.part(i).x, shape.part(i).y)
        
        return landmarks
    
    def draw_mouth(self, frame, landmarks, is_yawning=False):
        """
        Vẽ miệng lên khung hình
        
        Args:
            frame: Khung hình gốc
            landmarks: Mảng 68x2 chứa tọa độ điểm mốc
            is_yawning: Có phát hiện ngáp hay không
            
        Returns:
            np.ndarray: Khung hình với miệng được vẽ
        """
        if landmarks is None:
            return frame.copy()
        
        frame_draw = frame.copy()
        mouth = landmarks[self.MOUTH_INDICES]
        
        # Vẽ các điểm mốc miệng
        for (x, y) in mouth:
            cv2.circle(frame_draw, (x, y), 3, (0, 255, 255), -1)
        
        # Vẽ viền miệng
        mouth_hull = cv2.convexHull(mouth)
        color = (0, 0, 255) if is_yawning else (0, 255, 0)
        cv2.drawContours(frame_draw, [mouth_hull], 0, color, 2)
        
        return frame_draw

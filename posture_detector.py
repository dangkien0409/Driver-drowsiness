# -*- coding: utf-8 -*-
import cv2
import numpy as np
from scipy.spatial import distance as dist
import dlib
import math

class PostureDetector:
    """
    Lớp phát hiện tư thế tài xế dựa trên vị trí đầu
    """
    
    def __init__(self, dlib_landmark_path=None):
        """
        Khởi tạo bộ dò tư thế
        
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
        
        # Điểm mốc quan trọng cho phát hiện tư thế
        # Ghi chú: Dlib 68-point landmarks
        # - Mắt phải (viewer's right): điểm 36-41, tâm ≈ 39
        # - Mắt trái (viewer's left): điểm 42-47, tâm ≈ 45
        self.NOSE_TIP = 30           # Đầu mũi
        self.CHIN = 8                # Cằm
        self.RIGHT_EYE = 39          # Mắt phải (viewer's right) - tâm mắt
        self.LEFT_EYE = 45           # Mắt trái (viewer's left) - tâm mắt
        self.LEFT_MOUTH = 48         # Góc miệng trái
        self.RIGHT_MOUTH = 54        # Góc miệng phải
    
    def calculate_head_roll(self, landmarks):
        """
        Tính góc lệch ngang của đầu (roll angle)
        Dương = nghiêng sang phải, âm = nghiêng sang trái
        
        Args:
            landmarks: Mảng 68x2 chứa tọa độ điểm mốc
            
        Returns:
            float: Góc lệch ngang (độ)
        """
        if landmarks is None:
            return 0.0
        
        # Lấy tọa độ hai mắt
        right_eye = landmarks[self.RIGHT_EYE]  # viewer's right
        left_eye = landmarks[self.LEFT_EYE]    # viewer's left
        
        # Tính góc từ hai mắt (từ mắt trái sang mắt phải)
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        
        # Góc lệch (radian -> độ)
        angle = math.degrees(math.atan2(dy, dx))
        
        return angle
    
    def calculate_head_pitch(self, landmarks):
        """
        Tính góc tilt dọc của đầu (pitch angle)
        Dương = hướng xuống, âm = hướng lên
        
        Args:
            landmarks: Mảng 68x2 chứa tọa độ điểm mốc
            
        Returns:
            float: Góc tilt dọc (độ)
        """
        if landmarks is None:
            return 0.0
        
        # Lấy tọa độ các điểm
        nose = landmarks[self.NOSE_TIP]
        chin = landmarks[self.CHIN]
        
        # Tính khoảng cách
        dy = chin[1] - nose[1]
        dx = chin[0] - nose[0]
        
        # Góc pitch
        angle = math.degrees(math.atan2(dy, dx))
        
        return angle
    
    def calculate_forward_head_position(self, landmarks):
        """
        Phát hiện tư thế cúi đầu (forward head posture)
        Dựa trên khoảng cách giữa các điểm của mặt
        
        Args:
            landmarks: Mảng 68x2 chứa tọa độ điểm mốc
            
        Returns:
            float: Chỉ số tư thế cúi (0-1, càng lớn càng cúi)
        """
        if landmarks is None:
            return 0.0
        
        # Lấy tọa độ
        nose = landmarks[self.NOSE_TIP]
        chin = landmarks[self.CHIN]
        left_eye = landmarks[self.LEFT_EYE]
        right_eye = landmarks[self.RIGHT_EYE]
        
        # Tính khoảng cách từ mũi đến cằm
        nose_chin_dist = dist.euclidean(nose, chin)
        
        # Tính khoảng cách giữa hai mắt
        eye_dist = dist.euclidean(left_eye, right_eye)
        
        # Tỷ lệ để xác định tư thế cúi
        if eye_dist > 0:
            forward_ratio = nose_chin_dist / eye_dist
        else:
            forward_ratio = 0.0
        
        return forward_ratio
    
    def detect_posture(self, landmarks, roll_threshold=15, pitch_threshold=20, forward_threshold=1.5):
        """
        Phát hiện tư thế tài xế
        
        Args:
            landmarks: Mảng 68x2 chứa tọa độ điểm mốc
            roll_threshold: Ngưỡng góc lệch ngang (độ)
            pitch_threshold: Ngưỡng góc tilt dọc (độ)
            forward_threshold: Ngưỡng tư thế cúi
            
        Returns:
            dict: Thông tin phát hiện gồm:
                - 'is_bad_posture': bool (có tư thế xấu hay không)
                - 'roll_angle': float (góc lệch ngang)
                - 'pitch_angle': float (góc tilt dọc)
                - 'forward_score': float (chỉ số cúi)
                - 'posture_type': str (loại tư thế)
        """
        result = {
            'is_bad_posture': False,
            'roll_angle': 0.0,
            'pitch_angle': 0.0,
            'forward_score': 0.0,
            'posture_type': 'Binh thuong'
        }
        
        if landmarks is None:
            return result
        
        # Tính các góc
        roll_angle = self.calculate_head_roll(landmarks)
        pitch_angle = self.calculate_head_pitch(landmarks)
        forward_score = self.calculate_forward_head_position(landmarks)
        
        result['roll_angle'] = roll_angle
        result['pitch_angle'] = pitch_angle
        result['forward_score'] = forward_score
        
        # Phân loại tư thế
        if abs(roll_angle) > roll_threshold:
            result['is_bad_posture'] = True
            result['posture_type'] = 'Nghieng dau' if roll_angle > 0 else 'Nghieng sang trai'
        elif abs(pitch_angle) > pitch_threshold:
            result['is_bad_posture'] = True
            result['posture_type'] = 'Cui dau' if pitch_angle > 0 else 'Huong len'
        elif forward_score > forward_threshold:
            result['is_bad_posture'] = True
            result['posture_type'] = 'Cui dau phia truoc'
        
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
    
    def draw_posture_info(self, frame, landmarks, posture_result):
        """
        Vẽ thông tin tư thế lên khung hình
        
        Args:
            frame: Khung hình gốc
            landmarks: Mảng 68x2 chứa tọa độ điểm mốc
            posture_result: Kết quả từ detect_posture()
            
        Returns:
            np.ndarray: Khung hình với thông tin tư thế được vẽ
        """
        if landmarks is None:
            return frame.copy()
        
        frame_draw = frame.copy()
        
        # Vẽ các điểm mốc quan trọng
        key_points = {
            'Mũi': landmarks[self.NOSE_TIP],
            'Cằm': landmarks[self.CHIN],
            'Mắt Trái': landmarks[self.LEFT_EYE],
            'Mắt Phải': landmarks[self.RIGHT_EYE]
        }
        
        for name, (x, y) in key_points.items():
            cv2.circle(frame_draw, (x, y), 4, (255, 0, 0), -1)
            cv2.putText(frame_draw, name, (x+5, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)
        
        return frame_draw

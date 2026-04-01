import cv2
import numpy as np
from scipy.spatial import distance as dist
import dlib

class EyeDetector:
    """
    Lớp phát hiện mở/đóng mắt và tính Eye Aspect Ratio (EAR)
    """
    
    def __init__(self, dlib_landmark_path=None):
        """
        Khởi tạo bộ dò mắt
        
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
                print("Cảnh báo: Không tìm thấy mô hình dlib landmark. Sử dụng OpenCV Cascade.")
                self.predictor = None
        
        # Định nghĩa các chỉ số điểm mốc của dlib cho mắt trái và phải
        self.LEFT_EYE_INDICES = list(range(42, 48))
        self.RIGHT_EYE_INDICES = list(range(36, 42))
    
    def eye_aspect_ratio(self, eye):
        """
        Tính Eye Aspect Ratio (EAR) từ tọa độ các điểm mốc của mắt
        
        Args:
            eye: Mảng 6x2 chứa tọa độ (x, y) của các điểm mốc mắt
            
        Returns:
            float: Giá trị Eye Aspect Ratio
        """
        # Khoảng cách giữa các điểm mốc ngang
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        
        # Khoảng cách ngang
        C = dist.euclidean(eye[0], eye[3])
        
        # EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
        ear = (A + B) / (2.0 * C)
        
        return ear
    
    def detect_faces(self, frame):
        """
        Phát hiện khuôn mặt trong khung hình
        
        Args:
            frame: Khung hình từ camera
            
        Returns:
            list: Danh sách các khuôn mặt được phát hiện (dlib rectangles)
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
    
    def detect_drowsiness(self, frame, ear_threshold=0.2):
        """
        Phát hiện ngủ gật từ khung hình camera
        
        Args:
            frame: Khung hình từ camera
            ear_threshold: Ngưỡng EAR để xác định mắt đóng
            
        Returns:
            dict: Thông tin phát hiện gồm:
                - 'drowsy': bool (có phát hiện ngủ hay không)
                - 'left_ear': float (EAR mắt trái)
                - 'right_ear': float (EAR mắt phải)
                - 'faces': list (khuôn mặt phát hiện)
                - 'landmarks': np.ndarray (điểm mốc khuôn mặt)
        """
        faces = self.detect_faces(frame)
        
        result = {
            'drowsy': False,
            'left_ear': 0.0,
            'right_ear': 0.0,
            'faces': faces,
            'landmarks': None
        }
        
        if len(faces) == 0:
            return result
        
        # Lấy khuôn mặt đầu tiên (giả sử chỉ có một người lái xe)
        face = faces[0]
        
        # Lấy điểm mốc khuôn mặt
        landmarks = self.get_facial_landmarks(frame, face)
        result['landmarks'] = landmarks
        
        if landmarks is None:
            return result
        
        # Lấy tọa độ mắt trái và phải
        left_eye = landmarks[self.LEFT_EYE_INDICES]
        right_eye = landmarks[self.RIGHT_EYE_INDICES]
        
        # Tính EAR cho cả hai mắt
        left_ear = self.eye_aspect_ratio(left_eye)
        right_ear = self.eye_aspect_ratio(right_eye)
        
        result['left_ear'] = left_ear
        result['right_ear'] = right_ear
        
        # Kiểm tra nếu cả hai mắt đều đóng
        if left_ear < ear_threshold and right_ear < ear_threshold:
            result['drowsy'] = True
        
        return result
    
    def draw_results(self, frame, detection_result, show_landmarks=True):
        """
        Vẽ kết quả phát hiện lên khung hình
        
        Args:
            frame: Khung hình gốc
            detection_result: Kết quả từ detect_drowsiness()
            show_landmarks: Hiển thị điểm mốc khuôn mặt hay không
            
        Returns:
            np.ndarray: Khung hình với các kết quả được vẽ
        """
        frame_draw = frame.copy()
        
        # Vẽ độ tin cậy EAR
        ear_text = f"L-EAR: {detection_result['left_ear']:.2f} R-EAR: {detection_result['right_ear']:.2f}"
        cv2.putText(frame_draw, ear_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Vẽ cảnh báo nếu phát hiện ngủ
        if detection_result['drowsy']:
            cv2.putText(frame_draw, "CANH BAO: TAI XE DANG NGU GAT!", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Vẽ đường viền đỏ
            cv2.rectangle(frame_draw, (5, 5), (frame_draw.shape[1]-5, frame_draw.shape[0]-5),
                         (0, 0, 255), 3)
        
        # Vẽ mặt được phát hiện
        for face in detection_result['faces']:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame_draw, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Vẽ điểm mốc khuôn mặt
        if show_landmarks and detection_result['landmarks'] is not None:
            landmarks = detection_result['landmarks']
            for (x, y) in landmarks:
                cv2.circle(frame_draw, (x, y), 2, (0, 255, 255), -1)
        
        return frame_draw

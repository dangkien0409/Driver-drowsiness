# Cấu hình cho hệ thống phát hiện ngủ gật trên Jetson Nano

# Đường dẫn mô hình
FACE_DETECTOR_PATH = "models/face_detection_model"
EYE_DETECTOR_PATH = "models/eye_detection_model"
DLIB_LANDMARK_PATH = "models/shape_predictor_68_face_landmarks.dat"

# Thông số camera
CAMERA_WIDTH = 320  # Giảm độ phân giải cho Jetson Nano
CAMERA_HEIGHT = 240
CAMERA_FPS = 20
CAMERA_DEVICE = 0  # /dev/video0

# Thông số phát hiện mở/đóng mắt
EYE_AR_THRESHOLD = 0.2  # Eye Aspect Ratio ngưỡng
EYE_AR_CONSEC_FRAMES = 20  # Số khung hình liên tiếp để phát hiện ngủ

# Cảnh báo
ALARM_ENABLED = True
ALARM_SOUND_PATH = "sounds/alarm.wav"

# Logging
LOG_DIR = "logs"
SAVE_VIDEO = False
VIDEO_OUTPUT_PATH = "output_video.avi"

# Người dùng muốn gửi cảnh báo (email, SMS, v.v.)
ALERT_TYPE = "sound"  # "sound", "email", "sms", hoặc "all"
ALERT_EMAIL = "your_email@example.com"
ALERT_PHONE = "+84xxxxxxxxxx"

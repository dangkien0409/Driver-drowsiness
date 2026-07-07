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
EYE_AR_CONSEC_FRAMES = 8  # Số khung hình liên tiếp để phát hiện ngủ

# Thong so phat hien ngap
MOUTH_AR_THRESHOLD = 0.65  # Mouth Aspect Ratio nguong (tang tu 0.5 de giam nhiem duong am)
YAWN_CONSEC_FRAMES = 15  # So khung hinh lien tiep de xac nhan ngap (tang tu 10)

# Cảnh báo
ALARM_ENABLED = True
ALARM_SOUND_PATH = "sounds/alarm.wav"

# Còi 3 chân: VCC -> 3.3V, GND -> GND, IN/SIG -> chân signal GPIO
# Đặt theo BOARD pin numbering. BOARD 11 = chân signal điều khiển còi.
# Nếu module của bạn kích mức thấp, đổi BUZZER_ACTIVE_LOW = True.
BUZZER_ENABLED = True
BUZZER_PIN = 11
BUZZER_ACTIVE_LOW = True
BUZZER_BEEP_DURATION = 0.2

# Logging
LOG_DIR = "logs"
CAPTURED_FRAMES_DIR = "captured_frames"
SESSION_DIR_PREFIX = "session"
SAVE_VIDEO = False
VIDEO_OUTPUT_PATH = "output_video.avi"

# Người dùng muốn gửi cảnh báo (email, SMS, v.v.)
ALERT_TYPE = "sound"  # "sound", "email", "sms", hoặc "all"
ALERT_EMAIL = "your_email@example.com"
ALERT_PHONE = "+84xxxxxxxxxx"

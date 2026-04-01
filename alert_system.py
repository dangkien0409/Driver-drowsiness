import cv2
import os
import time
from datetime import datetime
import logging

class AlertSystem:
    """
    Hệ thống cảnh báo cho phát hiện ngủ gật
    """
    
    def __init__(self, config=None):
        """
        Khởi tạo hệ thống cảnh báo
        
        Args:
            config: Đối tượng cấu hình chứa các tham số cảnh báo
        """
        self.config = config
        self.last_alert_time = 0
        self.alert_cooldown = 2  # Khoảng thời gian giữa các cảnh báo (giây)
        
        # Khởi tạo logging
        self.setup_logger()
    
    def setup_logger(self):
        """Khởi tạo logger cho hệ thống"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/drowsiness_detection.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def should_trigger_alert(self):
        """
        Kiểm tra xem có nên kích hoạt cảnh báo hay không
        (Tránh cảnh báo liên tục)
        
        Returns:
            bool: True nếu đủ điều kiện kích hoạt cảnh báo
        """
        current_time = time.time()
        if current_time - self.last_alert_time > self.alert_cooldown:
            self.last_alert_time = current_time
            return True
        return False
    
    def sound_alert(self):
        """
        Kích hoạt cảnh báo âm thanh
        
        Lưu ý: Đối với Jetson Nano, có thể sử dụng:
        - beep (nội trang từ hệ thống)
        - Phát tệp audio
        - I2C speaker module
        """
        try:
            # Cách 1: Sử dụng beep nội trang (nếu có)
            os.system('beep')
        except:
            # Cách 2: In thông báo (fallback)
            print("\a\a\a")  # Terminal bell
    
    def log_alert(self, detection_info=None):
        """
        Ghi log sự kiện phát hiện ngủ
        
        Args:
            detection_info: Thông tin chi tiết về sự phát hiện
        """
        message = f"[ALERT] Phát hiện tài xế ngủ gật"
        if detection_info:
            message += f" - Left EAR: {detection_info.get('left_ear', 0):.3f}, Right EAR: {detection_info.get('right_ear', 0):.3f}"
        
        self.logger.warning(message)
    
    def send_email_alert(self, subject="Driver Drowsiness Alert", body=""):
        """
        Gửi cảnh báo qua email
        
        Args:
            subject: Chủ đề email
            body: Nội dung email
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Cấu hình email (cần cập nhật với thông tin thực)
            sender_email = "your_email@gmail.com"
            sender_password = "your_app_password"
            recipient_email = self.config.ALERT_EMAIL if self.config else "recipient@example.com"
            
            # Tạo message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            
            # Nội dung
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            email_body = f"""
            Cảnh báo: Tài xế đang ngủ gật
            
            Thời gian: {timestamp}
            
            {body}
            
            Hệ thống phát hiện ngủ gật trên Jetson Nano
            """
            
            message.attach(MIMEText(email_body, "plain"))
            
            # Gửi email (Gmail)
            # Lưu ý: Cần bật "Less secure app access" hoặc sử dụng App Password
            # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            # server.login(sender_email, sender_password)
            # server.sendmail(sender_email, recipient_email, message.as_string())
            # server.quit()
            
            self.logger.info(f"Email cảnh báo sẽ được gửi đến {recipient_email}")
            
        except Exception as e:
            self.logger.error(f"Lỗi khi gửi email: {e}")
    
    def trigger_alert(self, detection_info=None, alert_type="sound"):
        """
        Kích hoạt cảnh báo
        
        Args:
            detection_info: Thông tin phát hiện
            alert_type: Loại cảnh báo ("sound", "email", "sms", "all")
        """
        if not self.should_trigger_alert():
            return
        
        # Ghi log
        self.log_alert(detection_info)
        
        # Kích hoạt cảnh báo theo loại
        if alert_type in ["sound", "all"]:
            self.sound_alert()
        
        if alert_type in ["email", "all"]:
            self.send_email_alert(
                body=f"Left EAR: {detection_info.get('left_ear', 0):.3f}, Right EAR: {detection_info.get('right_ear', 0):.3f}"
            )
    
    def save_drowsy_frame(self, frame, detection_info=None):
        """
        Lưu khung hình khi phát hiện ngủ gật để phân tích sau
        
        Args:
            frame: Khung hình
            detection_info: Thông tin phát hiện
        """
        if not os.path.exists('captured_frames'):
            os.makedirs('captured_frames')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captured_frames/drowsy_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        
        # Ghi metadata
        with open(filename.replace('.jpg', '.txt'), 'w') as f:
            if detection_info:
                f.write(f"Left EAR: {detection_info.get('left_ear', 0):.3f}\n")
                f.write(f"Right EAR: {detection_info.get('right_ear', 0):.3f}\n")
            f.write(f"Timestamp: {datetime.now()}\n")

import cv2
import os
import time
from datetime import datetime
import logging
from importlib import import_module

try:
    GPIO = import_module("Jetson.GPIO")
except Exception:
    GPIO = None

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
        self.gpio_ready = False
        self.buzzer_pin = None
        self.buzzer_active_state = None
        self.buzzer_idle_state = None
        self.capture_root_dir = getattr(self.config, "CAPTURED_FRAMES_DIR", "captured_frames") if self.config else "captured_frames"
        self.active_capture_type = None
        self.active_capture_dir = None
        self.active_capture_frame_count = 0
        self.active_capture_started_at = None
        self.active_capture_last_info = None
        
        # Khởi tạo logging
        self.setup_logger()
        self.setup_buzzer()
    
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

    def setup_buzzer(self):
        """Khởi tạo GPIO cho còi 3 chân nếu được cấu hình."""
        if not self.config:
            return

        if not getattr(self.config, "BUZZER_ENABLED", False):
            return

        self.buzzer_pin = getattr(self.config, "BUZZER_PIN", None)
        if self.buzzer_pin is None or GPIO is None:
            return

        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.buzzer_pin, GPIO.OUT)

            active_low = bool(getattr(self.config, "BUZZER_ACTIVE_LOW", False))
            self.buzzer_active_state = GPIO.LOW if active_low else GPIO.HIGH
            self.buzzer_idle_state = GPIO.HIGH if active_low else GPIO.LOW

            GPIO.output(self.buzzer_pin, self.buzzer_idle_state)
            self.gpio_ready = True
            self.logger.info(f"Đã khởi tạo còi GPIO tại BOARD pin {self.buzzer_pin}")
        except Exception as e:
            self.gpio_ready = False
            self.logger.warning(f"Không thể khởi tạo còi GPIO: {e}")

    def cleanup(self):
        """Giải phóng tài nguyên GPIO nếu có."""
        if self.gpio_ready and GPIO is not None and self.buzzer_pin is not None:
            try:
                GPIO.output(self.buzzer_pin, self.buzzer_idle_state)
                GPIO.cleanup(self.buzzer_pin)
            except Exception:
                pass
            finally:
                self.gpio_ready = False
    
    def sound_alert(self):
        """
        Kích hoạt cảnh báo âm thanh
        
        Lưu ý: Đối với Jetson Nano, có thể sử dụng:
        - beep (nội trang từ hệ thống)
        - Phát tệp audio
        - I2C speaker module
        """
        if self.gpio_ready and self.buzzer_pin is not None:
            duration = getattr(self.config, "BUZZER_BEEP_DURATION", 0.2) if self.config else 0.2
            try:
                GPIO.output(self.buzzer_pin, self.buzzer_active_state)
                time.sleep(duration)
                GPIO.output(self.buzzer_pin, self.buzzer_idle_state)
                return
            except Exception as e:
                self.logger.warning(f"Lỗi khi kích hoạt còi GPIO: {e}")
        # Nếu GPIO không có hoặc failed, thử phát file âm thanh nếu có
        sound_path = getattr(self.config, "ALARM_SOUND_PATH", None) if self.config else None
        if sound_path and os.path.exists(sound_path):
            # ưu tiên aplay (ALSA) hoặc paplay
            players = ["aplay", "paplay", "ffplay -nodisp -autoexit", "play"]
            played = False
            for p in players:
                cmd = f"{p} {sound_path} >/dev/null 2>&1"
                try:
                    ret = os.system(cmd)
                    if ret == 0:
                        played = True
                        self.logger.info(f"Đã phát âm thanh cảnh báo bằng {p}")
                        break
                except Exception:
                    continue
            if played:
                return

        # Thử lệnh beep (nếu cài)
        try:
            ret = os.system('beep')
            if ret == 0:
                return
        except Exception:
            pass

        # Cuối cùng dùng terminal bell làm fallback
        try:
            print("\a\a\a")  # Terminal bell
            self.logger.info("Đã dùng terminal bell làm fallback cho cảnh báo")
        except Exception:
            self.logger.warning("Không thể phát bất kỳ cảnh báo âm thanh nào")

    def _normalize_event_type(self, event_type):
        if not event_type:
            return None

        normalized = str(event_type).strip().lower()
        if normalized in ["ngu gat", "ngủ gật", "drowsy", "sleep", "sleepy", "sleeping"]:
            return "Ngu Gat"
        if normalized in ["ngap", "ngáp", "buon ngu", "buồn ngủ", "yawn"]:
            return "Ngap"
        return None

    def _start_capture_session(self, event_type):
        normalized_type = self._normalize_event_type(event_type)
        if normalized_type is None:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = os.path.join(self.capture_root_dir, normalized_type, timestamp)
        os.makedirs(session_dir, exist_ok=True)

        self.active_capture_type = normalized_type
        self.active_capture_dir = session_dir
        self.active_capture_frame_count = 0
        self.active_capture_started_at = datetime.now()
        self.active_capture_last_info = None

        self.logger.info(f"Bắt đầu lưu frame cho sự kiện {normalized_type}: {session_dir}")
        return session_dir

    def _write_capture_summary(self):
        if not self.active_capture_dir:
            return

        summary_path = os.path.join(self.active_capture_dir, "session_info.txt")
        try:
            with open(summary_path, "w", encoding="utf-8") as summary_file:
                summary_file.write(f"Event type: {self.active_capture_type}\n")
                summary_file.write(f"Started at: {self.active_capture_started_at}\n")
                summary_file.write(f"Ended at: {datetime.now()}\n")
                summary_file.write(f"Frame count: {self.active_capture_frame_count}\n")
                if self.active_capture_last_info:
                    summary_file.write("Last detection info:\n")
                    summary_file.write(
                        f"  Left EAR: {self.active_capture_last_info.get('left_ear', 0):.3f}\n"
                    )
                    summary_file.write(
                        f"  Right EAR: {self.active_capture_last_info.get('right_ear', 0):.3f}\n"
                    )
                    summary_file.write(
                        f"  MAR: {self.active_capture_last_info.get('yawn_result', {}).get('mar', 0):.3f}\n"
                    )
        except Exception as e:
            self.logger.warning(f"Không thể ghi file tóm tắt sự kiện: {e}")

    def end_capture_session(self):
        if self.active_capture_type is None:
            return

        self._write_capture_summary()
        self.logger.info(
            f"Kết thúc lưu frame cho sự kiện {self.active_capture_type}: {self.active_capture_dir}"
        )
        self.active_capture_type = None
        self.active_capture_dir = None
        self.active_capture_frame_count = 0
        self.active_capture_started_at = None
        self.active_capture_last_info = None

    def record_event_frame(self, frame, event_type=None, detection_info=None):
        normalized_type = self._normalize_event_type(event_type)

        if normalized_type is None:
            self.end_capture_session()
            return

        if self.active_capture_type != normalized_type or self.active_capture_dir is None:
            self.end_capture_session()
            self._start_capture_session(normalized_type)

        if self.active_capture_dir is None:
            return

        self.active_capture_frame_count += 1
        self.active_capture_last_info = detection_info
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(
            self.active_capture_dir,
            f"frame_{self.active_capture_frame_count:04d}_{timestamp}.jpg"
        )

        try:
            cv2.imwrite(filename, frame)
        except Exception as e:
            self.logger.warning(f"Không thể lưu frame sự kiện: {e}")
    
    def log_alert(self, detection_info=None):
        """
        Ghi log sự kiện phát hiện ngủ
        
        Args:
            detection_info: Thông tin chi tiết về sự phát hiện
        """
        alert_label = "Phát hiện tài xế ngủ gật"
        if detection_info and detection_info.get("confirmed_yawn") and not detection_info.get("confirmed_drowsy"):
            alert_label = "Phát hiện tài xế buồn ngủ"

        message = f"[ALERT] {alert_label}"
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

    def __del__(self):
        try:
            self.cleanup()
        except Exception:
            pass
    
    def save_drowsy_frame(self, frame, detection_info=None):
        """Giữ tương thích ngược: lưu vào phiên sự kiện Ngủ Gật."""
        self.record_event_frame(frame, "Ngu Gat", detection_info)

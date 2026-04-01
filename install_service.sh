#!/usr/bin/env bash
# Script để bắt đầu hệ thống như một dịch vụ systemd
# Cài đặt: sudo cp drowsiness-detection.service /etc/systemd/system/
#         sudo systemctl daemon-reload
#         sudo systemctl enable drowsiness-detection
#         sudo systemctl start drowsiness-detection

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "╔════════════════════════════════════════════════╗"
echo "║   Cài đặt Systemd Service                      ║"
echo "║   Driver Drowsiness Detection                  ║"
echo "╚════════════════════════════════════════════════╝"

# Kiểm tra quyền root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Script này phải chạy với quyền root"
   echo "Chạy: sudo ./install_service.sh"
   exit 1
fi

# Cập nhật đường dẫn trong service file
SERVICE_FILE="$SCRIPT_DIR/drowsiness-detection.service"
INSTALL_PATH="/etc/systemd/system/drowsiness-detection.service"

echo "📝 Cấu hình service file..."
echo "Đường dẫn dự án: $SCRIPT_DIR"

# Sao chép file service
cp "$SERVICE_FILE" "$INSTALL_PATH"

# Cập nhật đường dẫn
sed -i "s|/home/nvidia/Driver-drowsiness|$SCRIPT_DIR|g" "$INSTALL_PATH"

# Tải lại systemd daemon
systemctl daemon-reload

# Enable service
systemctl enable drowsiness-detection

echo "✓ Service đã được cài đặt"
echo ""
echo "📋 Các lệnh hữu ích:"
echo "  sudo systemctl start drowsiness-detection      # Khởi động"
echo "  sudo systemctl stop drowsiness-detection       # Dừng"
echo "  sudo systemctl restart drowsiness-detection    # Khởi động lại"
echo "  sudo systemctl status drowsiness-detection     # Kiểm tra trạng thái"
echo "  sudo journalctl -u drowsiness-detection -f     # Xem log"
echo ""
echo "🎯 Service sẽ tự động khởi động khi boot"
echo ""

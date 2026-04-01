#!/usr/bin/env bash
# Script bỏ gỡ lỗi từ log
# Sử dụng: ./debug.sh [log_file]

LOG_FILE="${1:-logs/drowsiness_detection.log}"

echo "🔍 Phân tích Log File: $LOG_FILE"
echo "=" * 60

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ File không tìm thấy: $LOG_FILE"
    exit 1
fi

echo ""
echo "📊 Thống kê:"
echo "-" * 60

echo "Tổng số dòng: $(wc -l < "$LOG_FILE")"
echo "Số lỗi:"
echo "  - ERROR: $(grep -c "ERROR" "$LOG_FILE")"
echo "  - WARNING: $(grep -c "WARNING" "$LOG_FILE")"
echo "  - ALERT: $(grep -c "ALERT" "$LOG_FILE")"

echo ""
echo "⚠️  Các lỗi gần đây:"
echo "-" * 60
tail -30 "$LOG_FILE" | grep -i "error\|warning\|alert" || echo "Không tìm thấy lỗi"

echo ""
echo "🔴 Các lỗi:"
echo "-" * 60
grep "ERROR" "$LOG_FILE" | tail -10

echo ""
echo "💡 Gợi ý khắc phục sự cố:"
echo "-" * 60

if grep -q "Cannot open camera" "$LOG_FILE"; then
    echo "❌ Lỗi camera:"
    echo "   - Kiểm tra camera kết nối: ls -la /dev/video*"
    echo "   - Cấp quyền: sudo usermod -a -G video \$USER"
fi

if grep -q "dlib model not found" "$LOG_FILE"; then
    echo "❌ Lỗi mô hình dlib:"
    echo "   - Chạy: python3 install_dlib_model.py"
fi

if grep -q "out of memory" "$LOG_FILE"; then
    echo "❌ Hết bộ nhớ:"
    echo "   - Giảm độ phân giải camera"
    echo "   - Sử dụng --no-display"
fi

echo ""

#!/bin/bash
# Script cài đặt hệ thống phát hiện ngủ gật trên Jetson Nano

echo "================================================"
echo "Cài đặt hệ thống phát hiện ngủ gật - Jetson Nano"
echo "================================================"

# Cập nhật hệ thống
echo "Cập nhật hệ thống..."
sudo apt-get update
sudo apt-get upgrade -y

# Cài đặt các gói cơ bản
echo "Cài đặt các gói cơ bản..."
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    python3-numpy \
    python3-pip \
    cmake \
    git \
    libatlas-base-dev \
    libsuperpack-blas-dev \
    libjasper-dev \
    libtiff-dev \
    libjasper1 \
    libjpeg-dev \
    libpng-dev \
    libharfbuzz0b \
    libwebp6 \
    libtiff5 \
    libjasper1 \
    libjpeg-turbo8 \
    libqtgui4 \
    python3-pyqt5 \
    libqt4-test \
    libhdf5-dev \
    libharfbuzz0b \
    libwebp6 \
    libtiff5 \
    libjasper1 \
    libjpeg-turbo8 \
    sox

# Cài đặt OpenCV (nếu chưa có)
echo "Cài đặt OpenCV..."
pip3 install --upgrade pip
pip3 install opencv-python==4.5.5.64

# Cài đặt các thư viện Python cần thiết
echo "Cài đặt các thư viện Python..."
pip3 install -r requirements.txt

# Tải mô hình dlib shape predictor nếu chưa có
echo "Tải mô hình phát hiện mặt..."
mkdir -p models

if [ ! -f "models/shape_predictor_68_face_landmarks.dat" ]; then
    echo "Tải shape_predictor_68_face_landmarks.dat..."
    # Bạn cần tải từ: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    # Sau đó giải nén vào thư mục models/
    echo "Hãy tải file từ: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    echo "Giải nén vào thư mục models/"
else
    echo "Mô hình đã tồn tại"
fi

# Tạo các thư mục cần thiết
echo "Tạo các thư mục..."
mkdir -p logs
mkdir -p captured_frames
mkdir -p sounds

# Sao chép tệp âm thanh cảnh báo (nếu có)
echo "Kiểm tra file âm thanh cảnh báo..."
if [ ! -f "sounds/alarm.wav" ]; then
    echo "Chú ý: Chưa có file âm thanh alarm.wav"
    echo "Bạn có thể tạo một file âm thanh hoặc sử dụng âm thanh hệ thống"
fi

echo "================================================"
echo "Cài đặt hoàn tất!"
echo "================================================"
echo ""
echo "Hướng dẫn chạy:"
echo "  python3 main.py              # Chạy bình thường"
echo "  python3 main.py --camera 0   # Chỉ định camera"
echo "  python3 main.py --save-video # Lưu video"
echo "  python3 main.py --no-display # Không hiển thị (chỉ xử lý nền)"
echo ""
echo "Yêu cầu: Có camera USB hoặc CSI camera kết nối với Jetson Nano"

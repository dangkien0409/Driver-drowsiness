#!/bin/bash
# Makefile đơn giản cho dự án (thay thế cho make)

# Màu sắc
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Hàm in colors
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Các lệnh

help:
	@echo "Các lệnh có sẵn:"
	@echo "  make help              - Hiển thị trợ giúp này"
	@echo "  make install           - Cài đặt các gói cần thiết"
	@echo "  make check             - Kiểm tra hệ thống"
	@echo "  make run               - Chạy hệ thống chính"
	@echo "  make test-performance  - Kiểm tra hiệu suất"
	@echo "  make test-sensitivity  - Kiểm tra độ nhạy"
	@echo "  make clean             - Xóa các file tạm"
	@echo "  make setup             - Cấu hình toàn bộ"

install:
	@echo "Cài đặt các gói Python..."
	pip3 install -r requirements.txt
	python3 install_dlib_model.py

check:
	@echo "Kiểm tra hệ thống..."
	python3 check_system.py

run:
	@echo "Chạy hệ thống chính..."
	python3 main.py

run-noui:
	@echo "Chạy hệ thống (không hiển thị)..."
	python3 main.py --no-display

test-performance:
	@echo "Kiểm tra hiệu suất..."
	python3 performance_test.py

test-sensitivity:
	@echo "Kiểm tra độ nhạy..."
	python3 sensitivity_test.py

clean:
	@echo "Xóa file tạm..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Hoàn tất"

setup: install
	@echo "Khởi tạo hệ thống..."
	chmod +x *.py *.sh
	python3 check_system.py
	@echo "Sẵn sàng để chạy: make run"

.PHONY: help install check run run-noui test-performance test-sensitivity clean setup

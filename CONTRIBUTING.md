# Hướng dẫn Đóng góp

Cảm ơn bạn quan tâm đến dự án! Chúng tôi hoan nghênh các đóng góp từ cộng đồng.

## Cách Đóng Góp

### 1. Fork Dự Án
```bash
git clone https://github.com/yourusername/Driver-drowsiness.git
cd Driver-drowsiness
```

### 2. Tạo Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Thực hiện Thay đổi
- Sửa đổi code
- Thêm comments/docstring
- Kiểm tra code của bạn

### 4. Commit
```bash
git add .
git commit -m "Chức năng: Mô tả ngắn thay đổi"
```

### 5. Push
```bash
git push origin feature/your-feature-name
```

### 6. Tạo Pull Request
- Nhấp "Compare & pull request" trên GitHub
- Mô tả rõ ràng các thay đổi của bạn
- Chờ review

## Hướng dẫn Code

### Style
- Tuân theo PEP 8
- Sử dụng snake_case cho hàm/biến
- Sử dụng UPPER_CASE cho hằng số
- Thêm type hints khi có thể

### Documentation
```python
def function_name(param1, param2):
    """
    Mô tả ngắn gọn về hàm
    
    Args:
        param1: Mô tả tham số 1
        param2: Mô tả tham số 2
        
    Returns:
        Mô tả giá trị trả về
    """
```

### Testing
- Kiểm tra trên Jetson Nano nếu có thể
- Kiểm tra bằng lệnh: `python3 check_system.py`
- Kiểm tra hiệu suất: `python3 performance_test.py`

## Báo Cáo Bug

Nếu phát hiện bug:
1. Kiểm tra xem đã có issue tương tự chưa
2. Tạo issue mới với:
   - Tiêu đề rõ ràng
   - Mô tả chi tiết
   - Bước tái thiết lập
   - Thông tin hệ thống (JetPack version, camera model, v.v.)

## Yêu Cầu Tính Năng

Bạn có ý tưởng mới? Hãy tạo issue với:
- Mô tả tính năng
- Lý do cần tính năng này
- Các bài báo/tài liệu tham khảo (nếu có)

## Các Lĩnh Vực Cần Đóng Góp

- [ ] Hỗ trợ GPU (CUDA) để tăng tốc
- [ ] Thoát hiện tối ưu hơn
- [ ] Hỗ trợ nhiều camera
- [ ] Tích hợp với hệ thống thông minh (IoT)
- [ ] Tài liệu cải thiện
- [ ] Hỗ trợ ngôn ngữ khác

---

Cảm ơn đã đóng góp! 🎉

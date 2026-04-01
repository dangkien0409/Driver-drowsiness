#!/usr/bin/env python3
"""
Script để tải và trích xuất mô hình shape predictor của dlib
"""

import os
import urllib.request
import bz2
import shutil

def download_dlib_model():
    """
    Tải mô hình shape_predictor_68_face_landmarks từ dlib
    """
    
    model_dir = "models"
    model_path = os.path.join(model_dir, "shape_predictor_68_face_landmarks.dat")
    model_bz2_path = os.path.join(model_dir, "shape_predictor_68_face_landmarks.dat.bz2")
    
    # Tạo thư mục nếu chưa có
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    # Kiểm tra mô hình đã tồn tại chưa
    if os.path.exists(model_path):
        print(f"Mô hình đã tồn tại: {model_path}")
        return True
    
    # URL để tải mô hình
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    
    print(f"Đang tải mô hình từ {url}...")
    print("Lưu ý: File này khá lớn (~100MB), quá trình có thể mất vài phút...")
    
    try:
        # Tải file
        urllib.request.urlretrieve(url, model_bz2_path)
        print(f"Tải xong: {model_bz2_path}")
        
        # Giải nén
        print("Đang giải nén...")
        with bz2.BZ2File(model_bz2_path) as f:
            with open(model_path, "wb") as out:
                out.write(f.read())
        
        print(f"Giải nén thành công: {model_path}")
        
        # Xóa file .bz2
        os.remove(model_bz2_path)
        print(f"Đã xóa file nén: {model_bz2_path}")
        
        return True
        
    except Exception as e:
        print(f"Lỗi khi tải mô hình: {e}")
        print("\nHướng dẫn tải thủ công:")
        print("1. Truy cập: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        print("2. Tải file shape_predictor_68_face_landmarks.dat.bz2")
        print("3. Giải nén (bzip2) để được file .dat")
        print(f"4. Đặt file vào thư mục: {model_dir}/")
        
        return False

if __name__ == "__main__":
    print("Script tải mô hình dlib shape predictor")
    print("=" * 50)
    
    success = download_dlib_model()
    
    if success:
        print("\nThành công! Sẵn sàng chạy hệ thống phát hiện ngủ gật")
    else:
        print("\nCó lỗi xảy ra. Vui lòng kiểm tra lại hoặc tải thủ công.")

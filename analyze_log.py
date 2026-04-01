#!/usr/bin/env python3
"""
Trích xuất & Phân tích Log
Công cụ để phân tích file log phát hiện ngủ gật
"""

import re
import sys
from datetime import datetime
from collections import defaultdict

def parse_log_file(filepath):
    """Phân tích log file"""
    
    data = {
        'total_lines': 0,
        'errors': [],
        'warnings': [],
        'alerts': [],
        'timestamps': [],
    }
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                data['total_lines'] += 1
                
                if 'ERROR' in line:
                    data['errors'].append(line.strip())
                elif 'WARNING' in line:
                    data['warnings'].append(line.strip())
                elif 'ALERT' in line:
                    data['alerts'].append(line.strip())
                
                # Trích xuất timestamp
                match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if match:
                    data['timestamps'].append(match.group(1))
    
    except FileNotFoundError:
        print(f"❌ File không tìm thấy: {filepath}")
        return None
    
    return data

def print_report(data):
    """In báo cáo"""
    
    print("\n")
    print("╔════════════════════════════════════════════════╗")
    print("║   PHÂN TÍCH LOG - DRIVER DROWSINESS           ║")
    print("╚════════════════════════════════════════════════╝")
    
    print(f"\n📊 Thống kê Tổng Quát:")
    print("-" * 50)
    print(f"Tổng dòng: {data['total_lines']}")
    print(f"Lỗi: {len(data['errors'])}")
    print(f"Cảnh báo: {len(data['warnings'])}")
    print(f"Sự kiện ngủ: {len(data['alerts'])}")
    
    if data['timestamps']:
        print(f"Khoảng thời gian: {data['timestamps'][0]} → {data['timestamps'][-1]}")
    
    # Lỗi
    if data['errors']:
        print(f"\n❌ Lỗi ({len(data['errors'])}):")
        print("-" * 50)
        for error in data['errors'][-5:]:  # 5 lỗi cuối cùng
            print(f"  {error}")
        
        if len(data['errors']) > 5:
            print(f"  ... và {len(data['errors']) - 5} lỗi khác")
    
    # Cảnh báo
    if data['warnings']:
        print(f"\n⚠️  Cảnh báo ({len(data['warnings'])}):")
        print("-" * 50)
        for warning in data['warnings'][-5:]:
            print(f"  {warning}")
        
        if len(data['warnings']) > 5:
            print(f"  ... và {len(data['warnings']) - 5} cảnh báo khác")
    
    # Sự kiện ngủ
    if data['alerts']:
        print(f"\n🚨 Phát hiện Ngủ ({len(data['alerts'])}):")
        print("-" * 50)
        for alert in data['alerts'][-10:]:
            print(f"  {alert}")
        
        if len(data['alerts']) > 10:
            print(f"  ... và {len(data['alerts']) - 10} sự kiện khác")
    
    print("\n")

def main():
    """Hàm chính"""
    
    if len(sys.argv) < 2:
        log_file = "logs/drowsiness_detection.log"
        print(f"Sử dụng log mặc định: {log_file}")
    else:
        log_file = sys.argv[1]
    
    data = parse_log_file(log_file)
    
    if data:
        print_report(data)

if __name__ == "__main__":
    main()

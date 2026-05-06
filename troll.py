import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os

def get_current_dir():
    if getattr(sys, 'frozen', False):
        # Nếu đang chạy từ file .exe đã build
        return os.path.dirname(sys.executable)
    else:
        # Nếu đang chạy từ script python
        return os.path.dirname(os.path.abspath(__file__))

def show_troll():
    root = tk.Tk()
    root.title("Mở quà đi!")
    
    # Lấy kích thước màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Fullscreen
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.attributes('-fullscreen', True)
    root.configure(background='black')

    # Tìm file ảnh có tên image.jpg hoặc image.png ở cùng thư mục
    img_path = os.path.join(get_current_dir(), "image.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(get_current_dir(), "image.png")
    
    try:
        img = Image.open(img_path)
        
        # Scale ảnh cho vừa màn hình mà vẫn giữ tỉ lệ
        img_ratio = img.width / img.height
        screen_ratio = screen_width / screen_height
        
        if screen_ratio > img_ratio:
            new_height = screen_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = screen_width
            new_height = int(new_width / img_ratio)
            
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        label = tk.Label(root, image=photo, bg='black')
        label.image = photo
        label.place(relx=0.5, rely=0.5, anchor='center')
    except Exception as e:
        error_msg = ("Hãy đặt một file ảnh tên là 'image.jpg' hoặc 'image.png'\n"
                     "vào chung thư mục với file chương trình này nhé!\n\n"
                     f"Lỗi: {str(e)}")
        error_label = tk.Label(root, text=error_msg, fg="white", bg="black", font=("Arial", 16))
        error_label.place(relx=0.5, rely=0.5, anchor='center')

    # Hiện thông báo sau 1.5 giây
    def show_msg():
        # Bring the tkinter window to the foreground if it isn't
        messagebox.showinfo("Thông báo", "Bạn đã bị troll rồi")
        root.destroy()
        
    root.after(1500, show_msg)
    
    # Chặn không cho tắt bằng nút X hoặc Alt+F4
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Đảm bảo cửa sổ hiện lên trên cùng lúc mới bật
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    
    root.mainloop()

if __name__ == "__main__":
    show_troll()

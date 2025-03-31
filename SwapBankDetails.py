import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import os
import subprocess

# Thêm thư mục chứa config.py vào sys.path
sys.path.append(os.path.abspath("d:\\CODE\\VSCode\\AutoBank"))

import config  # Import file cấu hình

# Biến toàn cục để lưu thông tin ngân hàng và số tài khoản
selected_bank = ""
account_number = ""

# Hàm cập nhật thông tin ngân hàng, số tài khoản và xuất file .exe
def update_and_export():
    global selected_bank, account_number
    selected_bank = bank_var.get().split(" - ")[0]  # Chỉ lấy mã ngân hàng (phần trước dấu '-')
    account_number = account_entry.get()

    if not account_number:
        messagebox.showwarning("Thông báo", "Vui lòng nhập số tài khoản!")
        return

    # Ghi thông tin vào file config.py
    try:
        with open("d:\\CODE\\VSCode\\AutoBank\\config.py", "w") as config_file:
            config_file.write(f'selected_bank = "{selected_bank}"\n')
            config_file.write(f'account_number = "{account_number}"\n')
        messagebox.showinfo("Thành công", f"Đã cập nhật:\nNgân hàng: {selected_bank}\nSố tài khoản: {account_number}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật thông tin: {str(e)}")
        return

    # Hiển thị hộp thoại chọn thư mục lưu file .exe
    output_dir = filedialog.askdirectory(title="Chọn thư mục lưu file .exe")
    if not output_dir:
        messagebox.showwarning("Thông báo", "Bạn chưa chọn thư mục lưu file .exe!")
        return

    # Đóng gói CreateQRCode.py thành file .exe
    try:
        script_path = "d:\\CODE\\VSCode\\AutoBank\\CAGBank\\CreateQRCode.py"
        subprocess.run(
            ["pyinstaller", "--onefile", "--noconsole", "--hidden-import", "customtkinter", "--distpath", output_dir, script_path],
            check=True
        )
        messagebox.showinfo("Thành công", f"Đã xuất file .exe thành công!\nFile được lưu tại: {output_dir}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Lỗi", f"Không thể xuất file .exe. Lỗi: {e}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xuất file .exe: {str(e)}")

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("Cập nhật thông tin ngân hàng")
root.geometry("600x400")
root.configure(bg="lightblue")

# Nhãn chọn ngân hàng
tk.Label(root, text="Chọn ngân hàng:", font=("Arial", 12), bg="lightblue").pack(pady=5)

# Danh sách ngân hàng
banks = [
    "ACB - Ngân hàng Á Châu (Asia Commercial Bank)",
]

# Biến lưu ngân hàng được chọn
bank_var = tk.StringVar(value="Chọn ngân hàng")

# Tạo OptionMenu
menu = tk.OptionMenu(root, bank_var, *banks)
menu.config(font=("Arial", 12), bg="white", width=50)
menu.pack(pady=10)

# Nhãn và ô nhập số tài khoản
tk.Label(root, text="Nhập số tài khoản:", font=("Arial", 12), bg="lightblue").pack(pady=5)
account_entry = tk.Entry(root, font=("Arial", 12), width=50)
account_entry.pack(pady=5, ipadx=5)

# Nút cập nhật (tích hợp xuất file .exe)
update_button = tk.Button(root, text="Cập nhật và Xuất file .exe", font=("Arial", 12), bg="#007BFF", fg="white", command=update_and_export)
update_button.pack(pady=10)

# Chạy ứng dụng
root.mainloop()

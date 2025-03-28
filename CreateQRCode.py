import qrcode
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
from io import BytesIO

import customtkinter as ctk
ctk.set_appearance_mode("light")  # Giao diện sáng
ctk.set_default_color_theme("blue")  # Chủ đề màu

# Số tài khoản mặc định
ACCOUNT_NUMBER = "19745371"
update_id = None  # Biến lưu trạng thái cập nhật

# Hàm tạo QR Code từ VietQR sau khi kiểm tra
def generate_qr():
    amount = entry_amount.get()
    content = entry_content.get()

    if not amount or not content:
        messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ Số tiền và Tên tài khoản!")
        return

    # Hộp thoại xác nhận CHỈ xuất hiện khi nhấn nút "Tạo QR"
    confirm = messagebox.askyesno("Xác nhận", f"Xác nhận tạo QR với thông tin sau:\n\n- Tài khoản: {content}\n- Số tiền: {amount}đ\n\nTiếp tục?")
    if not confirm:
        return

    qr_url = f"https://img.vietqr.io/image/ACB-{ACCOUNT_NUMBER}-qr_only.png?amount={amount}&addInfo={content}"

    try:
        response = requests.get(qr_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            qr_label.config(image=img)
            qr_label.image = img
        else:
            messagebox.showerror("Lỗi", "Không thể tải QR Code từ VietQR!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải QR: {str(e)}")

# Hàm thay đổi số tiền khi nhấn nút
def set_amount(value):
    """Thay thế số tiền khi nhấn nút"""
    entry_amount.delete(0, tk.END)
    entry_amount.insert(0, str(value))

# Hàm tạo QR Code mặc định (làm mờ)
def generate_default_qr():
    try:
        img = Image.open("D:\CODE\VSCode\AutoBank\CAGBank\img\ICON-CAGPRO.png")  # Ảnh mặc định
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        qr_label.config(image=img)
        qr_label.image = img
    except Exception as e:
        print(f"Lỗi tải ảnh mặc định: {e}")

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("QR Code Chuyển Khoản")
root.configure(bg="lightblue")

frame_main = tk.Frame(root, bg="lightblue")
frame_main.pack(padx=20, pady=20)

# Khung chứa QR code (bo góc)
frame_left = tk.Frame(frame_main, bg="white", padx=10, pady=10)
frame_left.pack(pady=10)

qr_label = tk.Label(frame_main, bg="white")
qr_label.pack(pady=10)

# Hàm kiểm tra nhập số
def validate_number(P):
    """Chỉ cho phép nhập số và không cho số 0 đứng đầu."""
    if P.isdigit():
        return not (P.startswith("0") and len(P) > 0)  # Không cho nhập nếu số đầu tiên là 0
    return P == ""  

def validate_account(P):
    return P.isalnum() and (P.islower() or P.isdigit()) or P == ""   # Chỉ nhận chữ cái và số, hoặc cho phép ô trống
vcmd_account = root.register(validate_account)

# Form nhập tên tài khoản nạp tiền
tk.Label(frame_main, text="Tài khoản nạp", font=("Arial", 12, "bold"), bg="lightblue").pack()
entry_content = tk.Entry(frame_main, width=20, font=("Arial", 12),validate="key", validatecommand=(vcmd_account, "%P"))
entry_content.pack(pady=5, ipadx=5)

# Form nhập số tiền
tk.Label(frame_main, text="Số tiền", font=("Arial", 12, "bold"), bg="lightblue").pack()

vcmd = root.register(validate_number)

entry_amount = tk.Entry(frame_main, width=20, font=("Arial", 12), validate="key", validatecommand=(vcmd, "%P"))
entry_amount.pack(pady=5, ipadx=5)

# Nút tạo QR
btn_generate = ctk.CTkButton(
    frame_main, text="Tạo QR", width=100, height=40,
    fg_color="#007BFF", text_color="white",
    corner_radius=15, command=generate_qr
)
btn_generate.pack(pady=10)

# Tạo khung chứa các nút chọn mệnh giá
frame_buttons = ctk.CTkFrame(frame_main, fg_color="lightblue")
frame_buttons.pack(pady=10)

tk.Label(frame_buttons, text="Chọn số tiền", font=("Arial", 12, "bold"), bg="lightblue").grid(row=0, column=0, columnspan=3)

# Danh sách các mệnh giá (thêm 2 ô trống cuối cùng)
amounts = [10000, 20000, 50000, 100000, 200000, 500000]

# Tạo nút bấm với bo góc
for idx, amt in enumerate(amounts):
    row, col = divmod(idx, 3)  # Tính vị trí hàng và cột
    if amt:  # Nếu có giá trị, tạo nút số tiền
        btn = ctk.CTkButton(
            frame_buttons, text=f"{amt:,}đ", width=90, height=40,
            fg_color="#4CAF50", text_color="white",
            corner_radius=15, command=lambda a=amt: set_amount(a)
        )
    else:  # Nếu là chỗ trống, tạo nút ẩn
        btn = ctk.CTkLabel(frame_buttons, text="", width=90, height=40, fg_color="lightblue")

    btn.grid(row=row + 1, column=col, padx=5, pady=5)  # Cộng 1 vì hàng đầu tiên là tiêu đề

# Nhãn phiên bản
version_label = tk.Label(root, text="Phiên bản: 1.0.0.0", font=("Arial", 10), bg="lightblue", fg="black")
version_label.place(relx=0.01, rely=0.98, anchor="sw") 

# Tạo QR mặc định khi mở ứng dụng
generate_default_qr()

root.resizable(False, False)
root.configure(bg="lightblue")  # Đổi màu nền toàn bộ

# Chạy ứng dụng
root.mainloop()
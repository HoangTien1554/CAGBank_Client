import qrcode
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
from io import BytesIO

# Số tài khoản mặc định
ACCOUNT_NUMBER = "19745371"
update_id = None  # Biến lưu trạng thái cập nhật


# Hàm tạo QR Code từ VietQR
def generate_qr():
    amount = entry_amount.get()
    content = entry_content.get()

    if not amount or not content:
        return  # Không tạo QR nếu chưa nhập đủ

    # URL QRCode VietQR
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


# Hàm xử lý khi nhập dữ liệu (delay 0.5s trước khi tạo QR)
def on_entry_change(event=None):
    global update_id
    if update_id:
        root.after_cancel(update_id)  # Hủy cập nhật trước đó nếu có
    update_id = root.after(500, generate_qr)  # Đặt lịch cập nhật sau 0.5s


# Hàm tạo QR Code mặc định (làm mờ)
def generate_default_qr():
    qr = qrcode.make("QR Mặc Định")
    qr = qr.resize((250, 250), Image.Resampling.LANCZOS)

    # Chuyển sang ảnh RGB để tránh lỗi
    qr = qr.convert("RGB")

    # Làm mờ ảnh QR
    enhancer = ImageEnhance.Brightness(qr)
    qr_blurred = enhancer.enhance(1.7)  # Tăng độ sáng để làm mờ

    # Chuyển ảnh về dạng hiển thị trên Tkinter
    qr_blurred = ImageTk.PhotoImage(qr_blurred)

    qr_label.config(image=qr_blurred)
    qr_label.image = qr_blurred


# Tạo giao diện Tkinter
root = tk.Tk()
root.title("QR Code Chuyển Khoản ACB")

# Khung chính để bố trí ngang
frame_main = tk.Frame(root)
frame_main.pack(padx=20, pady=20)

# Khung bên trái (QR Code)
frame_left = tk.Frame(frame_main)
frame_left.pack(side=tk.LEFT, padx=10)

qr_label = tk.Label(frame_left)
qr_label.pack()

# Khung bên phải (Thông tin nhập)
frame_right = tk.Frame(frame_main)
frame_right.pack(side=tk.RIGHT, padx=20, pady=10)

tk.Label(frame_right, text="Số tài khoản:", font=("Arial", 12, "bold")).pack()
tk.Label(frame_right, text=ACCOUNT_NUMBER, font=("Arial", 12), fg="blue").pack()

tk.Label(frame_right, text="Số tiền:", font=("Arial", 12)).pack()
entry_amount = tk.Entry(frame_right, width=25, font=("Arial", 12))
entry_amount.pack(pady=5)
entry_amount.bind("<KeyRelease>", on_entry_change)  # Gọi khi nhập

tk.Label(frame_right, text="Nội dung:", font=("Arial", 12)).pack()
entry_content = tk.Entry(frame_right, width=25, font=("Arial", 12))
entry_content.pack(pady=5)
entry_content.bind("<KeyRelease>", on_entry_change)  # Gọi khi nhập

# Tạo QR mặc định khi mở ứng dụng
generate_default_qr()

# Chạy ứng dụng
root.mainloop()

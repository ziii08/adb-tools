import tkinter as tk
from tkinter import messagebox, simpledialog
import adb_util


def show_status():
    status = adb_util.check_status()
    messagebox.showinfo("Status", status)


def connect_usb():
    result = adb_util.connect_via_usb()
    messagebox.showinfo("Connect via USB", result)


def disconnect_wifi():
    result = adb_util.disconnect_wifi()
    messagebox.showinfo("Disconnect", result)


def connect_manual():
    ip = simpledialog.askstring(
        "Connect Manual", "Masukkan IP Address (contoh: 192.168.1.10):"
    )
    if ip:
        result = adb_util.connect_to_ip(ip)
        messagebox.showinfo("Connect Manual", result)


# GUI Setup
window = tk.Tk()
window.title("ADB WiFi Tool")
window.geometry("300x250")

tk.Label(window, text="ADB WiFi Launcher", font=("Arial", 14)).pack(pady=10)

tk.Button(window, text="🔍 Cek Status", width=30, command=show_status).pack(pady=5)
tk.Button(window, text="⚡ Connect via USB", width=30, command=connect_usb).pack(pady=5)
tk.Button(window, text="🌐 Connect Manual (IP)", width=30, command=connect_manual).pack(
    pady=5
)
tk.Button(window, text="❌ Disconnect WiFi", width=30, command=disconnect_wifi).pack(
    pady=5
)
tk.Button(
    window, text="Keluar", width=30, command=window.destroy, bg="red", fg="white"
).pack(pady=5)

window.mainloop()

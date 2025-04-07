import tkinter as tk
from tkinter import messagebox
import adb_util
import re


def show_status():
    status = adb_util.check_status()
    messagebox.showinfo("Status", status)


def connect_usb():
    result = adb_util.connect_via_usb()
    messagebox.showinfo("Connect via USB", result)


def disconnect_wifi():
    result = adb_util.disconnect_wifi()
    messagebox.showinfo("Disconnect", result)


def auto_connect_last_ip():
    last_ip = adb_util.load_last_ip()
    if last_ip:
        devices = adb_util.get_connected_devices()
        if not any(last_ip in dev for dev in devices):
            result = adb_util.connect_to_ip(last_ip)
            print("🧠 Auto Connect:", result)


def connect_manual():
    def toggle_show():
        if entry.cget("show") == "":
            entry.config(show="*")
            toggle_btn.config(text="Show")
        else:
            entry.config(show="")
            toggle_btn.config(text="Hide")

    def is_valid_ip(ip):
        return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip) is not None

    def on_connect():
        ip = entry.get().strip()
        if not is_valid_ip(ip):
            messagebox.showerror("Error", "Format IP tidak valid.")
            return
        top.destroy()
        result = adb_util.connect_to_ip(ip)
        messagebox.showinfo("Connect Manual", result)

    last_ip = adb_util.load_last_ip()

    top = tk.Toplevel()
    top.title("Connect Manual")
    top.geometry("300x150")
    top.resizable(False, False)

    tk.Label(top, text="Masukkan IP Address:").pack(pady=10)

    entry_frame = tk.Frame(top)
    entry_frame.pack()

    entry = tk.Entry(entry_frame, width=25, show="*")
    entry.insert(0, last_ip)
    entry.pack(side="left")

    toggle_btn = tk.Button(entry_frame, text="Show", command=toggle_show, width=5)
    toggle_btn.pack(side="left", padx=5)

    connect_btn = tk.Button(top, text="Connect", command=on_connect)
    connect_btn.pack(pady=10)

    entry.focus()
    top.transient()
    top.grab_set()
    top.mainloop()


# GUI Setup
window = tk.Tk()
window.title("ADB WiFi Tool")
window.geometry("300x280")
window.resizable(False, False)

# Header
tk.Label(window, text="ADB WiFi Launcher", font=("Arial", 14, "bold")).pack(pady=10)

# Menu Buttons
tk.Button(window, text="🔍 Cek Status", width=30, command=show_status).pack(pady=5)
tk.Button(window, text="⚡ Connect via USB", width=30, command=connect_usb).pack(pady=5)
tk.Button(window, text="🌐 Connect Manual (IP)", width=30, command=connect_manual).pack(
    pady=5
)
tk.Button(window, text="❌ Disconnect WiFi", width=30, command=disconnect_wifi).pack(
    pady=5
)
tk.Button(
    window, text="❄ Keluar", width=30, command=window.destroy, bg="red", fg="white"
).pack(pady=10)

# Auto connect if possible
auto_connect_last_ip()

window.mainloop()

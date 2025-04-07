import subprocess
import re
import time
import os

LAST_IP_FILE = "last_ip.txt"


def save_last_ip(ip):
    with open(LAST_IP_FILE, "w") as f:
        f.write(ip.strip())


def load_last_ip():
    if os.path.exists(LAST_IP_FILE):
        with open(LAST_IP_FILE, "r") as f:
            return f.read().strip()
    return ""


def connect_to_ip(ip):
    ip = ip.strip()
    result = run_cmd(f"adb connect {ip}:5555")
    if "connected" in result or "already connected" in result:
        save_last_ip(ip)
        return f"✓ Berhasil connect ke {ip}:5555"
    return f"X Gagal connect ke {ip}:5555\n{result}"


def run_cmd(cmd):
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    return result.stdout.strip()


def get_connected_devices():
    output = run_cmd("adb devices")
    return [line.split("\t")[0] for line in output.splitlines() if "\tdevice" in line]


def check_status():
    devices = get_connected_devices()
    if any(":5555" in d for d in devices):
        return f"✓ Sudah terhubung via Wi-Fi: {devices}"
    elif devices:
        return f"Terhubung via USB: {devices}"
    else:
        return "X Tidak ada device terdeteksi."


def get_ip_from_device():
    output = run_cmd("adb shell ip route")
    match = re.search(r"src (\d+\.\d+\.\d+\.\d+)", output)
    return match.group(1) if match else None


def connect_via_usb():
    ip = get_ip_from_device()
    if not ip:
        return "X Gagal mendapatkan IP dari device."
    run_cmd("adb tcpip 5555")
    time.sleep(2)
    result = run_cmd(f"adb connect {ip}:5555")
    if "connected" in result:
        return f"✓ Berhasil connect ke {ip}:5555"
    return f"X Gagal connect ke {ip}:5555\n{result}"


def disconnect_wifi():
    devices = get_connected_devices()
    for d in devices:
        if ":5555" in d:
            run_cmd(f"adb disconnect {d}")
            return f"✓ Terputus dari {d}"
    return "Tidak ada koneksi Wi-Fi aktif."


# Tambahkan fungsi ini di akhir file
def connect_to_ip(ip):
    ip = ip.strip()
    result = run_cmd(f"adb connect {ip}:5555")
    if "connected" in result or "already connected" in result:
        return f"✓ Berhasil connect ke {ip}:5555"
    return f"X Gagal connect ke {ip}:5555\n{result}"

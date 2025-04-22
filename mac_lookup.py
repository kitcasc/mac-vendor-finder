import tkinter as tk
from tkinter import messagebox
import re
import requests
import os
import uuid
import subprocess
import platform

# File name
OUI_FILENAME = "oui.txt"

# Download OUI file from IEEE
def download_oui_file(filename=OUI_FILENAME):
    url = "http://standards-oui.ieee.org/oui/oui.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        messagebox.showinfo("Successful!", "OUI data downloaded！")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed ：{e}")

# Query OUI from the file
def lookup_oui(mac, filename=OUI_FILENAME):
    clean_mac = re.sub(r'[^0-9A-Fa-f]', '', mac).upper()
    if len(clean_mac) != 12:
        return "Invalid MAC address format"

    oui = '-'.join([clean_mac[i:i+2] for i in range(0, 6, 2)])
    oui_search = oui.replace("-", "").upper()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if oui_search in line:
                    return line.strip()
        return "Vendor information not found"
    except FileNotFoundError:
        return "OUI data file not found, please download manually"

# Get MAC addresses of the host machine
def get_local_mac_addresses():
    mac_addresses = []
    
    # Method 1: Using UUID (may not always work)
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                       for elements in range(0,8*6,8)][::-1])
        if not mac.startswith('00:00:00:00:00:00'):
            mac_addresses.append(mac)
    except:
        pass
    
    # Method 2: Using system commands
    system = platform.system()
    try:
        if system == "Windows":
            # Windows method
            result = subprocess.check_output("getmac", shell=True).decode()
            for line in result.split('\n'):
                mac = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
                if mac:
                    mac_addresses.append(mac.group(0))
        elif system == "Linux" or system == "Darwin":
            # Linux/Mac method
            result = subprocess.check_output(["ifconfig"]).decode()
            for line in result.split('\n'):
                mac = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
                if mac:
                    mac_addresses.append(mac.group(0))
    except:
        pass
    
    # Remove duplicates
    unique_macs = []
    seen = set()
    for mac in mac_addresses:
        if mac not in seen:
            seen.add(mac)
            unique_macs.append(mac)
    
    return unique_macs if unique_macs else ["No MAC addresses found"]

# Create GUI
def create_gui():
    def on_lookup():
        mac = mac_entry.get()
        result = lookup_oui(mac)
        result_label.config(text=f"Query result：{result}")

    def on_download():
        download_oui_file()
    
    def on_autofill():
        macs = get_local_mac_addresses()
        if macs:
            mac_entry.delete(0, tk.END)
            mac_entry.insert(0, macs[0])
            if len(macs) > 1:
                messagebox.showinfo("Multiple MACs Found", 
                                  f"Found multiple MAC addresses:\n{', '.join(macs)}\nUsing the first one.")

    window = tk.Tk()
    window.title("MAC Manufacturer Lookup Tool")
    window.geometry("500x280")

    tk.Label(window, text="Please Enter MAC Address（ex. 00:1A:2B:3C:4D:5E）").pack(pady=5)
    mac_entry = tk.Entry(window, width=30)
    mac_entry.pack()

    button_frame = tk.Frame(window)
    button_frame.pack(pady=5)
    
    tk.Button(button_frame, text="Query Manufacturer", command=on_lookup).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Auto-fill Local MAC", command=on_autofill).pack(side=tk.LEFT, padx=5)
    
    tk.Button(window, text="Download/Update OUI database", command=on_download).pack(pady=5)

    global result_label
    result_label = tk.Label(window, text="", fg="blue", wraplength=480, justify="left")
    result_label.pack(pady=10)

    window.mainloop()

# Main function
if __name__ == "__main__":
    if not os.path.exists(OUI_FILENAME):
        try:
            download_oui_file()
        except:
            print("OUI file download failed, please download manually.")

    create_gui()
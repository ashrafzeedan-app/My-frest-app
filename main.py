import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

sock = None
running = False

def get_my_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def log_me(msg):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, f"انت: {msg}\n", "me")
    chat_box.config(state='disabled')
    chat_box.see(tk.END)

def log_other(msg):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, f"الطرف الاخر: {msg}\n", "other")
    chat_box.config(state='disabled')
    chat_box.see(tk.END)

def receive_loop(conn):
    global running
    while running:
        try:
            data = conn.recv(4096).decode('utf-8', errors='ignore')
            if not data: break
            log_other(data)
        except: break
    running = False

def start_server():
    global sock, running
    port = int(port_entry.get() or 5000)
    try:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", port))
        sock.listen(1)
        running = True
        my_ip = get_my_ip()
        log_me(f"السيرفر خدام... الـ IP ديالك هو {my_ip} عطيه لصاحبك")
        threading.Thread(target=accept_client, daemon=True).start()
    except Exception as e:
        log_other(f"Error: {e}")

def accept_client():
    global sock
    conn, addr = sock.accept()
    sock = conn
    receive_loop(conn)

def connect_client():
    global sock, running
    ip = ip_entry.get() or "127.0.0.1"
    port = int(port_entry.get() or 5000)
    try:
        sock = socket.socket()
        sock.connect((ip, port))
        running = True
        threading.Thread(target=lambda: receive_loop(sock), daemon=True).start()
        log_me(f"تم الاتصال")
    except Exception as e:
        log_other(f"Error: {e}")

def send_msg():
    msg = msg_entry.get().strip()
    if not msg or not sock: return
    try:
        sock.send(msg.encode())
        log_me(msg)
        msg_entry.delete(0, tk.END)
    except Exception as e:
        log_other(f"Error: {e}")

# --- واجهة WASL ---
root = tk.Tk()
try:
    root.iconbitmap("wasl_logo.ico")
except:
    pass
root.title(f"WASL - وصل - IP: {get_my_ip()}")
root.geometry("500x650")
root.configure(bg="#ece5dd")

tk.Label(root, text=f"WASL - وصل | الـ IP ديالك: {get_my_ip()} | عطيه لصاحبك", bg="#075e54", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, ipady=6)

top = tk.Frame(root, bg="#f0f0f0")
top.pack(pady=8, fill=tk.X, padx=10)
tk.Label(top, text="IP صاحبك:", bg="#f0f0f0").grid(row=0, column=0)
ip_entry = tk.Entry(top, width=18)
ip_entry.insert(0, "127.0.0.1")
ip_entry.grid(row=0, column=1, padx=5)
tk.Label(top, text="Port:", bg="#f0f0f0").grid(row=0, column=2)
port_entry = tk.Entry(top, width=8)
port_entry.insert(0, "5000")
port_entry.grid(row=0, column=3, padx=5)

f=tk.Frame(root, bg="#f0f0f0")
f.pack(pady=5)
tk.Button(f, text="شغل كـ سيرفر", bg="#4CAF50", fg="white", width=14, command=start_server).grid(row=0,column=0,padx=5)
tk.Button(f, text="اتصل", bg="#2196F3", fg="white", width=10, command=connect_client).grid(row=0,column=1,padx=5)

chat_box = scrolledtext.ScrolledText(root, state='disabled', height=25, font=("Arial", 11), bg="#e5ddd5")
chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
chat_box.tag_config("me", foreground="#075e54", font=("Arial", 11, "bold"))
chat_box.tag_config("other", foreground="#000000")

bottom = tk.Frame(root, bg="#f0f0f0")
bottom.pack(fill=tk.X, padx=10, pady=10)
msg_entry = tk.Entry(bottom, font=("Arial", 12))
msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
msg_entry.bind("<Return>", lambda e: send_msg())
send_btn = tk.Button(bottom, text="ارسال ➤", bg="#25D366", fg="white", font=("Arial", 11, "bold"), width=8, command=send_msg)
send_btn.pack(side=tk.RIGHT, padx=(8,0))

root.mainloop()

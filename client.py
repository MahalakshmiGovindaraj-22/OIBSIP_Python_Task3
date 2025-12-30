import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Chat Application")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_area.pack(padx=10, pady=10)
chat_area.config(state='disabled')

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=5)

def send_message():
    message = message_entry.get()
    if message:
        client.send(f"{username}: {message}".encode('utf-8'))
        message_entry.delete(0, tk.END)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# ---------------- MESSAGE HANDLING ---------------- #

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "USERNAME":
                client.send(username.encode('utf-8'))
            else:
                chat_area.config(state='normal')
                chat_area.insert(tk.END, message + "\n")
                chat_area.yview(tk.END)
                chat_area.config(state='disabled')
        except:
            break

# ---------------- LOAD CHAT HISTORY ---------------- #

try:
    with open("chat_history.txt", "r", encoding="utf-8") as f:
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f.read())
        chat_area.config(state='disabled')
except FileNotFoundError:
    pass

# ---------------- USERNAME ---------------- #

username = simpledialog.askstring("Username", "Enter your username:", parent=root)

thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

root.mainloop()

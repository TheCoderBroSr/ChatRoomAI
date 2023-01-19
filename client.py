import socket
import sys
import tkinter as tk
from tkinter import ttk
from threading import Thread
from queue import Queue

def receive(queue):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                queue.put(data)
        except:
            break

def update_text(queue):
    while True:
        try:
            data = queue.get(timeout=0.1)

            text.config(state='normal')
            
            #Assigning different tags, to different types of text
            if "has joined" in data:
                tag = "joined"
            elif "has disconnected" in data:
                tag = "disconnected"
            else:
                tag = data[0:data.index(':')] #Getting Username from data

            tag += "_tag"
            text.insert(tk.END, data + '\n', tag)

            text.config(state='disabled')
        except:
            root.after(1000, update_text, queue)
            break


def send_message():
    message = entry.get()
    client_socket.send(message.encode())
    entry.delete(0, 'end')

def on_closing():
    client_socket.close()
    root.destroy()
    sys.exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345

username = input("Enter your name: ")
client_socket.connect((host, port))
client_socket.send(username.encode())

queue = Queue()
receive_thread = Thread(target=receive, args=(queue,))
receive_thread.start()

root = tk.Tk()
root.title("Chat Client")
root.protocol("WM_DELETE_WINDOW", on_closing)

text = tk.Text(root)
text.config(font=("Courier", 12), state='disabled')
text.tag_config("joined_tag", foreground="green")
text.tag_config("disconnected_tag", foreground="red")
text.tag_config(f"{username}_tag", foreground="blue")
text.pack()

entry = tk.Entry(root, width=40)
entry.bind("<Return>", lambda event: send_message())
entry.pack()

style = ttk.Style()
style.configure("TButton", font="Verdana 15", padding=6, relief="flat", background="#ccc")
send_button = ttk.Button(root, text="Send", style="TButton", command=send_message)
send_button.pack()

root.after(0, update_text, queue)
root.mainloop()
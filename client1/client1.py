import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Настройки клиента
HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# Функция для отправки сообщения
def send_message():
    message = message_entry.get()
    if message.strip():  # Отправляем только если сообщение не пустое
        client_socket.sendall(message.encode('utf-8'))
        chat_window.insert(tk.END, f"Вы (клиент 1): {message}\n")
        message_entry.delete(0, tk.END)  # Очищаем поле ввода


# Функция для получения сообщений от сервера
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            chat_window.insert(tk.END, f"Друг (клиент 2): {data.decode('utf-8')}\n")
        except:
            chat_window.insert(tk.END, "Соединение разорвано.\n")
            break


# Создаем графический интерфейс
root = tk.Tk()
root.title("Чат клиент 1")

# Задаем фон для основного окна
root.config(bg='lightblue')  # Цвет фона для основного окна

# Устанавливаем иконку для окна
root.iconbitmap('./icon/background.jpg')  # Замените на путь к вашему файлу иконки

# Окно для отображения чата
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='normal', height=20, width=50)
chat_window.pack(pady=10)

# Задаем фон для окна чата
chat_window.config(bg='white')  # Цвет фона для окна чата

# Поле для ввода сообщения
message_entry = tk.Entry(root, width=40)
message_entry.pack(pady=5, side=tk.LEFT, padx=(10, 0))

# Кнопка для отправки сообщения
send_button = tk.Button(root, text="Отправить", command=send_message)
send_button.pack(pady=5, side=tk.LEFT, padx=(5, 10))

# Поток для получения сообщений
threading.Thread(target=receive_messages, daemon=True).start()

# Запуск интерфейса
root.mainloop()

# Закрытие сокета при завершении программы
client_socket.close()

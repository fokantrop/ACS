import socket
import threading

# Настройка сервера
HOST = '127.0.0.1'
PORT = 12345

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)  # Сервер рассчитан на двух клиентов
print(f"Сервер запущен и слушает {HOST}:{PORT}...")

# Список для хранения подключенных клиентов
clients = []

# Функция для обработки каждого клиента
def handle_client(client_socket, client_id):
    while True:
        try:
            # Получение данных от клиента
            data = client_socket.recv(1024)
            if not data:
                break

            # Вывод сообщения в консоль сервера
            message = f"Сообщение от клиента {client_id}: {data.decode('utf-8')}"
            print(message)

            # Пересылка сообщения другому клиенту
            other_client_id = 1 if client_id == 2 else 2  # Находим ID второго клиента
            if len(clients) >= 2:  # Проверяем наличие второго клиента
                other_client_socket = clients[other_client_id - 1]  # ID в списке на 1 меньше
                other_client_socket.sendall(data)
        except:
            break

    # Удаление клиента при разрыве соединения
    print(f"Клиент {client_id} отключился.")
    clients[client_id - 1] = None  # Удаляем клиента из списка
    client_socket.close()

# Основной цикл сервера
while len(clients) < 2:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    client_id = len(clients)
    print(f"Клиент {client_id} подключился: {client_address}")
    threading.Thread(target=handle_client, args=(client_socket, client_id)).start()

print("Сервер больше не принимает новых клиентов.")

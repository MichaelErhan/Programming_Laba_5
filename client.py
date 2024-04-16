import socket                                                                           #
import nacl.utils                                                                       # Импортируем нужные библиотеки
from nacl.public import PrivateKey, Box                                                 #

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                       # Создаем сокет
client_socket.connect(('localhost', 12345))                                             # Прописываем хост, порт

try:
    with open("client_private_key.txt", "rb") as f:
        client_private_key = PrivateKey(f.read())                                       # Загружаем приватный ключ клиента
        print("Ключ найден. Закрытый ключ клиента:", client_private_key)

    with open("client_public_key.txt", "rb") as f:
        client_public_key = nacl.public.PublicKey(f.read())                             # Загружаем открытый ключ клиента
        print("Ключ найден. Открытый ключ клиента:", client_public_key)

except FileNotFoundError:                                                               # Если файл не найден - создаем ключи
    client_private_key = PrivateKey.generate()
    client_public_key = client_private_key.public_key
    with open("client_private_key.txt", "wb") as f:
        f.write(client_private_key.encode())
        print("Ключ не найден. Создан закрытый ключ:", client_private_key)
    with open("client_public_key.txt", "wb") as f:
        f.write(client_public_key.encode())
        print("Ключ не найден. Создан открытый ключ:", client_public_key)

client_socket.send(client_public_key.encode())                                          # Отправляем открытый ключ клиента

server_public_key = client_socket.recv(1024)                                            # Получаем открытый ключ сервера
server_public_key = nacl.public.PublicKey(server_public_key)                            # Создаём объект открытого ключа
print("Получен открытый ключ сервера: ", server_public_key)

client_box = Box(client_private_key, server_public_key)                                 # Генерируем общий секретный ключ

client_port = '54321'                                                                   # Номер порта для основного общения
client_socket.send(client_port.encode())                                                # Отправляем порт серверу

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                         # Подключаемся к порту для основного общения
main_socket.connect(('localhost', int(client_port)))
print(f"Подключаемся к порту {client_port} для основного общения")

while True:                                                                             # Бесконечный цикл для отправки сообщений
    message = input("Введите сообщение для отправки серверу: ")

    encrypted_message = client_box.encrypt(message.encode())                            # Зашифровываем сообщение клиента
    client_socket.send(encrypted_message)                                               # Отправляем сообщение на сервер
    print("Зашифрованное сообщение отправлено на сервер:", encrypted_message)

    response = client_socket.recv(1024)                                                 # Получаем ответ от сервера
    decrypted_response = client_box.decrypt(response).decode()                          # Расшифровываем ответ с сервера
    print(f"Получен ответ от сервера: {response}")
    print(f"Расшифрованный ответ от сервера: " + decrypted_response)
import socket                                                                   #
import nacl.utils                                                               # Импортируем нужные библиотеки
from nacl.public import PrivateKey, Box                                         #

encrypt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               # Создаем сокет
encrypt_socket.bind(('localhost', 12345))                                        # Прописываем хост, порт
encrypt_socket.listen(1)                                                         # Начинаем слушать (ждём подключения (одного))
print("Сервер запущен и ждет подключения...")

try:
    # Загрузка приватного ключа сервера
    with open("server_private_key.txt", "rb") as f:
        server_private_key = PrivateKey(f.read())                               # Загружаем закрытый ключ сервера
        print("Ключ найден. Закрытый ключ сервера:", server_private_key)

    # Загрузка публичного ключа сервера
    with open("server_public_key.txt", "rb") as f:
        server_public_key = nacl.public.PublicKey(f.read())                     # Загружаем открытый ключ сервера
        print("Ключ найден. Открытый ключ сервера:", server_public_key)

except FileNotFoundError:                                                       # Если файл не найден - создаем ключи
    server_private_key = PrivateKey.generate()
    server_public_key = server_private_key.public_key
    with open("server_private_key.txt", "wb") as f:
        f.write(server_private_key.encode())
        print("Ключ не найден. Создан закрытый ключ:", server_private_key)
    with open("server_public_key.txt", "wb") as f:
        f.write(server_public_key.encode())
        print("Ключ не найден. Создан открытый ключ:", server_public_key)

connection, address = encrypt_socket.accept()                                    # Принимаем подключение клиента
print("Подключился клиент для шифрования:", address)

connection.send(server_public_key.encode())                                     # Отправляем открытый ключ сервера клиенту

client_public_key = connection.recv(1024)                                       # Получаем открытый ключ клиента
client_public_key = nacl.public.PublicKey(client_public_key)                    # Создаем объект открытого ключа
print("Получен открытый ключ клиента:", client_public_key)

server_box = Box(server_private_key, client_public_key)                         # Генерируем общий секретный ключ

port_number = connection.recv(1024).decode()                                    # Получаем новый порт от клиента

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 # Подключаемся к новому порту
main_socket.bind(('localhost', int(port_number)))
main_socket.listen(1)
print(f"Получен порт для основного общения. Сервер запустил порт {port_number}")

while True:                                                                     # Бесконечный цикл для приёма сообщений
    encrypted_message = connection.recv(1024)                                   # Получаем сообщение от клиента
    print(f"Получено от клиента зашифрованное сообщение: {encrypted_message}")

    decrypted_message = server_box.decrypt(encrypted_message).decode()          # Расшифровываем сообщение клиента
    print(f"Расшифрованное сообщение от клиента: {decrypted_message}")

    encrypted_response = server_box.encrypt(decrypted_message.encode())         # Зашифровываем сообщение для отправки клиенту
    connection.send(encrypted_response)                                         # Отправляем клиенту сообщение
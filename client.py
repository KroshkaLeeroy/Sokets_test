import os
import socket
import struct
import time


def send_file(sck: socket.socket, filename):
    # Получение размера файла.
    filesize = os.path.getsize(filename)
    # В первую очередь сообщим серверу,
    # сколько байт будет отправлено.
    sck.sendall(struct.pack("<Q", filesize))
    # Отправка файла блоками по 1024 байта.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)


count = 0
text = ''
with socket.create_connection(("192.168.0.128", 6190)) as conn:
    print("Подключение к серверу.")
    print("Передача файла...")


    while True:
        text += f'[{count}] kek\n'
        with open('file.txt', 'w') as file:
            file.write(text)
        send_file(conn, "file.txt")
        print("Отправлено.")
        count += 1
        time.sleep(2)


print("Соединение закрыто.")

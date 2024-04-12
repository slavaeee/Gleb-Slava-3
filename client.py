import os
import time
import json
import socket
import struct

# ФУНКЦИЯ СЛАВЫ
def send_numbers(numbers):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", 12345))  # Подставьте нужный хост и порт программы 1
        for num in numbers:
            num_bytes = struct.pack("!i", num)  # Упаковываем число в байты
            sock.sendall(num_bytes)
        sock.shutdown(socket.SHUT_WR)  # Закрываем запись на сокете
        print("Дерево создано")
        
# ФУНКЦИИ ГЛЕБА
def pack_data(data):
    """
    Упаковывает данные перед отправкой через сокет.
    """
    packed_data = json.dumps(data).encode()
    return packed_data

def send_changes(sock, folder):
    """
    Отправляет изменения в содержимом папки через сокет.
    """
    files1 = get_directory_structure(folder)
    packed_data = pack_data(files1)
    sock.sendall(packed_data)

def receive_changes(sock):
    """
    Получает изменения в содержимом папки через сокет.
    """
    data = sock.recv(1024)  # предполагаем, что не более 1024 байт
    if data:
        file_data = json.loads(data.decode())
        print(f"Received {len(file_data)} files with sizes: {file_data}")
        # Далее можно добавить логику применения изменений к папке

if __name__ == "__main__":
    income = int(input('Введите 1(Слава), введите 2(Глеб)'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("localhost", 12345))  # Подставьте нужный хост и порт программы 1
            sock.sendall(struct.pack("!i", income))
            sock.shutdown(socket.SHUT_WR)
    if income == 1:
        while True:
            income = int(input('Введите 1, чтобы создать дерево, введите 2, чтобы получить файл: '))
            if income == 1:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(("localhost", 12345))  # Подставьте нужный хост и порт программы 1
                    sock.sendall(struct.pack("!i", income))
                    sock.shutdown(socket.SHUT_WR)
                    # numbers = [1, 2, 3, 4, 5]  # Пример чисел для отправки
                    numbers = []
                    while True:
                        income = input('Введите число, когда закончите, введите \'stop\': ')
                        if income == 'stop':
                            break
                        try:
                            int(income)
                        except ValueError:
                            print('Введено неправильное значение')
                            continue
                        else:
                            numbers.append(int(income))
                send_numbers(numbers)
            elif income == 2:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(("localhost", 12345)) 
                    filename = input("Введите имя файла для отправки: ")
                    sock.sendall(filename.encode())

                    data = b''
                    while True:
                        piece = sock.recv(1024)
                        if not piece:
                            break
                        data += piece

                    if data == b"File not found":
                        print("Файл не найден на сервере")
                    else:
                        with open(filename, 'wb') as file:
                            file.write(data)
                        print("Файл успешно получен от сервера")
                    sock.shutdown(socket.SHUT_WR)
    elif income == 2:
        folder1 = input("Введите путь к первой папке: ")
        
        # Установить сокетное соединение с программой 1
        server_address = ('localhost', 10000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        connected = False
        while not connected:
            try:
                sock.connect(server_address)
                connected = True
            except ConnectionRefusedError:
                print("Не удалось установить соединение. Повторная попытка через 10 секунд...")
                time.sleep(10)

        while True:
            def get_directory_structure(folder):
                """Получает структуру папки, возвращает список файлов и их размеры."""
                files = []
                for dirpath, _, filenames in os.walk(folder):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        filesize = os.path.getsize(filepath)
                        files.append((filename, filesize))
                return files
            # Отправить содержимое своей папки программе 1
            send_changes(sock, folder1)
            # Получить изменения из программы 1 и применить их к своей папке
            receive_changes(sock)
            # Дополнительно можно добавить логику ожидания или цикла проверки каждые n секунд
            time.sleep(5)
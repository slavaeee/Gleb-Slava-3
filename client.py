import socket
import struct

def send_numbers(numbers):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", 12345))  # Подставьте нужный хост и порт программы 1
        for num in numbers:
            num_bytes = struct.pack("!i", num)  # Упаковываем число в байты
            sock.sendall(num_bytes)
        sock.shutdown(socket.SHUT_WR)  # Закрываем запись на сокете
        print("Дерево создано")

if __name__ == "__main__":
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
                sock.connect(('localhost', 12345))
                sock.sendall(struct.pack("!i", income))
                sock.shutdown(socket.SHUT_WR)
                
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
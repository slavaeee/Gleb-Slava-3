import os
import datetime
import json
import xml.etree.ElementTree as ET
import socket
import struct

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        if value < self.value:
            if self.left is None:
                self.left = TreeNode(value)
            else:
                self.left.insert(value)
        elif value > self.value:
            if self.right is None:
                self.right = TreeNode(value)
            else:
                self.right.insert(value)

def create_folder():
    now = datetime.datetime.now()
    folder_name = now.strftime("%d-%m-%Y_%H:%M:%S")
    os.makedirs(folder_name)
    return folder_name

def save_json(tree_root, folder_path):
    filename = os.path.join(folder_path, "tree.json")
    data = serialize_tree(tree_root)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# count = 0
# def create_json(num, folder_path):
#     global count
#     count += 1
#     filename = os.path.join(folder_path, f"{count}.json")
#     with open(filename, 'w') as f:
#         json.dump(num, f, indent=4)

def save_xml(tree_root, folder_path):
    filename = os.path.join(folder_path, "tree.xml")
    data = serialize_tree(tree_root)
    root = ET.Element("tree")
    append_xml_node(root, data)
    tree = ET.ElementTree(root)
    tree.write(filename)

def serialize_tree(root):
    if root is None:
        return None
    return {
        "value": root.value,
        "left": serialize_tree(root.left),
        "right": serialize_tree(root.right)
    }

def append_xml_node(parent, data):
    if data is None:
        return
    node = ET.Element("node")
    value = ET.SubElement(node, "value")
    value.text = str(data["value"])
    append_xml_node(node, data["left"])
    append_xml_node(node, data["right"])
    parent.append(node)

def handle_client(conn, addr, root, folder_path):
    print(f"Установлено соединение с {addr}")
    while True:
        try:
            num_bytes = conn.recv(4)  # Принимаем 4 байта (размер int)
            if not num_bytes:
                break
            num = struct.unpack("!i", num_bytes)[0]  # Распаковываем байты в число
            if root is None:
                root = TreeNode(num)
            else:
                root.insert(num)
            print(f"Число {num} добавлено в дерево.")
        except Exception as e:
            print(f"Ошибка обработки данных от {addr}: {e}")
            break
    conn.close()
    print(f"Соединение с {addr} закрыто.")
    return root

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))  # Подставьте нужный хост и порт
    server_socket.listen(5)
    
    while True:
        print("Программа 1 ожидает соединений...")
        conn, addr = server_socket.accept()
        print(f"Установлено соединение с {addr}")
        num_bytes = conn.recv(4)
        num = struct.unpack("!i", num_bytes)[0]
        if num == 1:
            folder_path = create_folder()
            root = None
            conn, addr = server_socket.accept()
            root = handle_client(conn, addr, root, folder_path)
            # После обработки клиента можно сохранить дерево в файлы
            save_json(root, folder_path)
        else:
            conn, addr = server_socket.accept()
            print("Подключение установлено с", addr)

            # dir = b''
            # while True:
            #     data = conn.recv(1024)
            #     if not data:
            #         break
            #     dir += data
            #     if b'\n' in data:
            #         break
            
            dir = conn.recv(1024)
                
            
            print("Получено имя директории:", dir)
            filename = dir + b'/tree.json'
            print(filename)

            try:
                with open(filename, 'rb') as file:
                    data = file.read()
                conn.send(data)
                print("Файл успешно отправлен клиенту")
            except FileNotFoundError:
                conn.send(b"File not found")
            conn.close()



if __name__ == "__main__":
    main()
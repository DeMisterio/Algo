import os
import json
import socket
import time
import socket
import time

class Communicator:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
    def receive_signal(self):
        """Клиент получает сигнал и отправляет подтверждение"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        print("✅ Подключился к серверу")

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                print("❌ Сервер отключился")
                break
            print("📩 Получен сигнал:", data)
            client_socket.send(b"Got")   # подтверждение
            return data   # возвращаем сигнал наружу
        client_socket.close()
    def send_signal(self, signal):
        """Клиент отправляет сигнал и ждёт подтверждения"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        print("✅ Подключился к серверу")
        client_socket.send(signal.encode())
        print("📤 Отправил:", signal)
        while True:
            feedback = client_socket.recv(1024).decode()
            if not feedback:
                print("⚠️ Сервер не отвечает, пробую ещё...")
                time.sleep(0.2)
                continue
            else:
                print("📨 Подтверждение получено:", feedback)
                client_socket.close()
                return "Sent"
            
if __name__ == "__main__":
    Client = Communicator()
    signal = Client.receive_signal()
    
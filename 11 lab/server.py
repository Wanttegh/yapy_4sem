import socket
import threading
import time
import sys


def receive_messages(conn, stop_event):
    while not stop_event.is_set():
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            if data.lower() == 'exit':
                print("\nКлиент инициировал отключение.")
                stop_event.set()
                break

            print(f"\nКлиент: {data}")
            print("Вы: ", end='', flush=True)
        except:
            break


def start_server():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Сервер запущен на {host}:{port}. Ожидание клиента...")

    conn, addr = server_socket.accept()
    print(f"Подключено к: {addr}")

    stop_event = threading.Event()

    # Поток для приема сообщений
    recv_thread = threading.Thread(target=receive_messages, args=(conn, stop_event))
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while not stop_event.is_set():
            message = input("Вы: ")

            if message.lower() == 'exit':
                conn.send("exit".encode('utf-8'))
                stop_event.set()
                break

            if message.lower().startswith('sleep'):
                try:
                    parts = message.split()
                    seconds = int(parts[1]) if len(parts) > 1 else 5
                    conn.send(f"Сервер ушел в спящий режим на {seconds} сек.".encode('utf-8'))
                    print(f"Сон на {seconds} секунд...")
                    time.sleep(seconds)
                    print("Сервер проснулся.")
                    conn.send("Сервер снова онлайн.".encode('utf-8'))
                    continue
                except ValueError:
                    print("Ошибка: используйте 'sleep <секунды>'")
                    continue

            conn.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        pass
    finally:
        print("Закрытие сервера...")
        conn.close()
        server_socket.close()
        sys.exit()


def main():
    start_server()


if __name__ == "__main__":
    main()
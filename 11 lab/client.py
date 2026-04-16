import socket
import threading
import sys


def receive_messages(client_socket, stop_event):
    while not stop_event.is_set():
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print("\nСоединение разорвано сервером.")
                stop_event.set()
                break

            if data.lower() == 'exit':
                print("\nСервер прислал команду EXIT. Отключение...")
                stop_event.set()
                break

            print(f"\nСервер: {data}")
            print("Вы: ", end='', flush=True)
        except:
            break


def start_client():
    host = '127.0.0.1'
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу. Убедитесь, что он запущен.")
        return

    print("Подключено к серверу. Введите 'exit' для выхода.")

    stop_event = threading.Event()

    recv_thread = threading.Thread(target=receive_messages, args=(client_socket, stop_event))
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while not stop_event.is_set():
            message = input("Вы: ")
            if stop_event.is_set():
                break

            client_socket.send(message.encode('utf-8'))

            if message.lower() == 'exit':
                stop_event.set()
                break
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()
        print("Клиент завершил работу.")
        sys.exit()


def main():
    start_client()


if __name__ == "__main__":
    main()
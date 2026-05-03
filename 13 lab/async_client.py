import asyncio
import sys


async def send_messages(writer):
    """
    Считывает ввод пользователя и отправляет на сервер.

    :param writer: Объект потока записи.
    """
    while True:
        message = await asyncio.to_thread(sys.stdin.readline)
        if not message:
            break
        writer.write(message.encode())
        await writer.drain()


async def receive_messages(reader):
    """
    Принимает сообщения от сервера и выводит в консоль.

    :param reader: Объект потока чтения.
    """
    while True:
        data = await reader.read(1024)
        if not data:
            print("\nСоединение с сервером разорвано.")
            break
        print(f"\nСервер: {data.decode().strip()}")
        print("Вы: ", end="", flush=True)


async def main():
    """Подключение к серверу и запуск цикла обмена сообщениями."""
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        print("Подключено к серверу. Введите сообщение:")

        await asyncio.gather(
            receive_messages(reader),
            send_messages(writer)
        )
    except ConnectionRefusedError:
        print("Ошибка: Не удалось подключиться к серверу. Проверьте, запущен ли он.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nВыход из чата.")
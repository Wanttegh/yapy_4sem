import asyncio
import sys


async def send_messages(writer):
    """
    Считывает ввод из консоли и отправляет его клиенту.

    writer: Объект потока записи asyncio.
    """
    while True:
        # Используем to_thread, чтобы input() не блокировал event loop
        message = await asyncio.to_thread(sys.stdin.readline)
        if not message:
            break
        writer.write(message.encode())
        await writer.drain()


async def receive_messages(reader):
    """
    Принимает сообщения от клиента и выводит их в консоль.

    reader: Объект потока чтения asyncio.
    """
    while True:
        data = await reader.read(1024)
        if not data:
            print("\nКлиент отключился.")
            break
        print(f"\nКлиент: {data.decode().strip()}")
        print("Вы: ", end="", flush=True)


async def handle_client(reader, writer):
    """
    Управляет соединением с клиентом.

    reader: Объект потока чтения.
    writer: Объект потока записи.
    """
    addr = writer.get_extra_info('peername')
    print(f"Новое соединение от {addr}")
    print("Вы можете писать сообщения...")

    # Запускаем чтение и отправку параллельно
    try:
        await asyncio.gather(
            receive_messages(reader),
            send_messages(writer)
        )
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    """Запуск сервера."""
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Сервер запущен на {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
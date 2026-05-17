from aiohttp import web
from hident import identify_hashes, long_solve_hash


async def handle_define(request: web.Request) -> web.Response:
    """
    Обрабатывает запрос на определение алгоритмов хеширования.

    request: Объект запроса aiohttp.
    return: JSON со списком возможных алгоритмов.
    """
    hash_value = request.match_info.get('hash', '')
    algorithms = identify_hashes(hash_value)
    return web.json_response(algorithms)


async def handle_solve(request: web.Request) -> web.Response:
    """
    Обрабатывает запрос на 'раскрытие' хеша по конкретному алгоритму.

    request: Объект запроса aiohttp.
    return: JSON с результатом вычисления.
    """
    hash_value = request.query.get('hash', '')
    algorithm = request.query.get('algorithm', '')

    if not hash_value or not algorithm:
        return web.json_response(
            {'error': 'Missing hash or algorithm parameters'},
            status=400
        )

    result = await long_solve_hash(hash_value, algorithm)
    return web.json_response({'hash': hash_value, 'result': result})


def main():
    """Настройка и запуск приложения aiohttp."""
    app = web.Application()
    app.add_routes([
        web.get('/define/{hash}', handle_define),
        web.get('/solve', handle_solve),
    ])
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
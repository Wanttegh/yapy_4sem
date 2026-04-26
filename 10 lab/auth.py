import json
import hashlib
import os
import secrets


class AuthSystem:
    def __init__(self, db_path='users_db.json'):
        self.db_path = db_path
        self.users = self._load_db()

    def _load_db(self):
        """Загружает базу данных из файла."""
        if not os.path.exists(self.db_path):
            return {}
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_db(self):
        """Сохраняет текущую базу данных в файл."""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=4)

    def _hash_password(self, password, salt=None):
        """
        Создает защищенный хеш пароля с использованием соли.
        Возвращает кортеж (salt, hash) в виде шестнадцатеричных строк.
        """
        if salt is None:
            # Генерируем случайную соль (16 байт)
            salt = secrets.token_hex(16)

        # Используем PBKDF2 (более безопасен, чем обычный sha256)
        # 100,000 итераций замедляют брутфорс
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()

        return salt, pwd_hash

    def add_user(self, login, password):
        """Добавляет нового пользователя."""
        if login in self.users:
            print(f"Ошибка: Пользователь '{login}' уже существует.")
            return False

        salt, pwd_hash = self._hash_password(password)
        self.users[login] = {
            'salt': salt,
            'hash': pwd_hash
        }
        self._save_db()
        print(f"Пользователь '{login}' успешно зарегистрирован.")
        return True

    def authenticate(self, login, password):
        """Проверяет логин и пароль."""
        if login not in self.users:
            return False

        user_data = self.users[login]
        # Хешируем введенный пароль с той же солью, что хранится в базе
        _, check_hash = self._hash_password(password, user_data['salt'])

        # Сравниваем полученный хеш с сохраненным
        return secrets.compare_digest(user_data['hash'], check_hash)

    def change_password(self, login, old_password, new_password):
        """Меняет пароль существующего пользователя."""
        if not self.authenticate(login, old_password):
            print("Ошибка: Старый пароль неверен или пользователя не существует.")
            return False

        # Генерируем новую соль и хеш для нового пароля
        new_salt, new_pwd_hash = self._hash_password(new_password)
        self.users[login] = {
            'salt': new_salt,
            'hash': new_pwd_hash
        }
        self._save_db()
        print(f"Пароль для пользователя '{login}' успешно изменен.")
        return True


def main():
    auth = AuthSystem()

    # 1. Регистрация
    auth.add_user("admin", "qwerty12345")
    auth.add_user("user_ivan", "my_secret_pass")

    # 2. Попытка входа
    print(f"Вход admin: {auth.authenticate('admin', 'qwerty12345')}")  # True
    print(f"Вход admin (ошибка): {auth.authenticate('admin', '1111')}")  # False

    # 3. Смена пароля
    auth.change_password("admin", "qwerty12345", "new_secure_password")

    # 4. Проверка после смены
    print(f"Вход admin со старым паролем: {auth.authenticate('admin', 'qwerty12345')}")  # False
    print(f"Вход admin с новым паролем: {auth.authenticate('admin', 'new_secure_password')}")  # True


# --- Пример использования ---
if __name__ == "__main__":
    main()
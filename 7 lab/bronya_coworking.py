import datetime
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class BookingStatus(Enum):
    """Статусы бронирования."""
    ACTIVE = "активно"
    CANCELED = "отменено"


class WorkspaceType(Enum):
    """Типы рабочих пространств."""
    DESK = "рабочее место"
    PRIVATE_OFFICE = "личный кабинет"
    MEETING_ROOM = "переговорная"


@dataclass
class Address:
    """Местоположение коворкинга."""
    city: str
    street: str
    floor: int


@dataclass
class User:
    """Пользователь системы."""
    id: int
    name: str
    rating: float  # рейтинг от 1 до 5
    bonus_points: int  # бонусные баллы для компенсации


@dataclass
class Booking:
    """
    Бронирование рабочего места.
    
    Использует композицию с классами Address и User.
    """
    address: Address
    user: User
    workspace_type: WorkspaceType
    price_per_hour: int
    date: datetime.date
    hours: int
    
    # Автоматически генерируемые поля
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8], init=False)
    created_at: datetime.datetime = field(
        default_factory=datetime.datetime.now, 
        init=False
    )
    status: BookingStatus = field(default=BookingStatus.ACTIVE, init=False)

    def __post_init__(self):
        """Валидация данных после инициализации."""
        if self.hours <= 0:
            raise ValueError("Количество часов должно быть больше 0.")
        if not (1 <= self.user.rating <= 5):
            raise ValueError(f"Рейтинг пользователя {self.user.name} "
                             f"должен быть в пределах от 1 до 5.")

    def total_price(self) -> int:
        """Возвращает общую стоимость бронирования."""
        return self.price_per_hour * self.hours

    def cancel(self) -> None:
        """Меняет статус бронирования на 'отменено'."""
        self.status = BookingStatus.CANCELED

    def change_user(self, new_user: User) -> None:
        """Передает бронь другому пользователю."""
        self.user = new_user


def exchange_bookings(booking1: Booking, booking2: Booking) -> bool:
    """
    Обменивает брони между пользователями.

    Если цены разные, разница компенсируется бонусными баллами:
    тот, кто получает более дорогую бронь, отдает баллы тому,
    кто получает более дешевую.
    """
    # 1. Проверка активности броней
    if (booking1.status != BookingStatus.ACTIVE or 
            booking2.status != BookingStatus.ACTIVE):
        print("Ошибка: Одна из броней не активна.")
        return False

    # 2. Проверка совпадения дат
    if booking1.date != booking2.date:
        print("Ошибка: Даты бронирований не совпадают.")
        return False

    # Расчет стоимостей и разницы
    price1 = booking1.total_price()
    price2 = booking2.total_price()
    diff = price1 - price2

    # Сохраняем ссылки на пользователей
    user1 = booking1.user
    user2 = booking2.user

    # 3. Обмен пользователями
    booking1.change_user(user2)
    booking2.change_user(user1)

    # 4. Компенсация разницы
    # Если diff > 0, значит бронь 1 была дороже. 
    # Теперь её получил user2, он должен отдать баллы user1.
    if diff > 0:
        user2.bonus_points -= diff
        user1.bonus_points += diff
    elif diff < 0:
        # Если diff < 0, значит бронь 2 была дороже.
        # Теперь её получил user1, он отдает баллы user2.
        user1.bonus_points -= abs(diff)
        user2.bonus_points += abs(diff)

    return True


def main():
    """Демонстрация работы системы бронирования."""
    # Создаем пользователей
    alice = User(id=1, name="Алиса", rating=4.8, bonus_points=500)
    bob = User(id=2, name="Боб", rating=4.2, bonus_points=200)
    
    # Создаем адреса
    desk_addr = Address(city="Москва", street="Тверская, 15", floor=3)
    office_addr = Address(city="Москва", street="Тверская, 15", floor=5)
    
    # Создаем брони
    booking1 = Booking(
        address=desk_addr,
        user=alice,
        workspace_type=WorkspaceType.DESK,
        price_per_hour=300,
        date=datetime.date(2026, 3, 25),
        hours=4
    )
    
    booking2 = Booking(
        address=office_addr,
        user=bob,
        workspace_type=WorkspaceType.PRIVATE_OFFICE,
        price_per_hour=1200,
        date=datetime.date(2026, 3, 25),
        hours=3
    )

    print(f"До обмена:")
    print(f"  {alice.name}: {alice.bonus_points}б. Бронь ID: {booking1.id}")
    print(f"  {bob.name}: {bob.bonus_points}б. Бронь ID: {booking2.id}")
    print(f"  Стоимость брони 1: {booking1.total_price()}")
    print(f"  Стоимость брони 2: {booking2.total_price()}")

    # 1. Тест обмена
    print("\n--- Выполняем обмен бронями ---")
    if exchange_bookings(booking1, booking2):
        print("Обмен успешен!")
    
    print(f"После обмена:")
    print(f"  {alice.name} (теперь в офисе): {alice.bonus_points}б.")
    print(f"  {bob.name} (теперь за столом): {bob.bonus_points}б.")

    # 2. Тест отмены
    print("\n--- Тест отмены ---")
    booking1.cancel()
    print(f"Статус брони 1 после отмены: {booking1.status.value}")

    # 3. Тест смены пользователя вручную
    print("\n--- Тест прямой смены пользователя ---")
    charlie = User(id=3, name="Чарли", rating=4.5, bonus_points=100)
    booking2.change_user(charlie)
    print(f"Владелец брони 2 теперь: {booking2.user.name}")


if __name__ == "__main__":
    main()
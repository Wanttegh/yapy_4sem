from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Union, Tuple
import calendar


class WithdrawalType(Enum):
    """Типы возможности снятия средств."""
    NONE = "none"  # Снятие невозможно
    PARTIAL = "partial"  # Частичное снятие возможно
    FULL_ONLY = "full_only"  # Только полное закрытие


class CapitalizationType(Enum):
    """Типы капитализации процентов."""
    NONE = "none"  # Без капитализации
    MONTHLY = "monthly"  # Ежемесячная капитализация


class Deposit:
    """
    Класс, представляющий банковский вклад.

    Attributes:
        percent (float): Процентная ставка за месяц (в долях).
        amount (float): Текущая сумма вклада.
        period_months (int): Срок вклада в месяцах.
        start_date (datetime): Дата открытия вклада.
        replenishment_allowed (bool): Разрешено ли пополнение.
        auto_prolongation (bool): Автоматическое продление.
        withdrawal_type (WithdrawalType): Тип возможности снятия.
        capitalization (CapitalizationType): Тип капитализации.
        is_active (bool): Активен ли вклад.
        last_calculation_date (datetime): Дата последнего начисления процентов.
    """

    def __init__(
        self,
        percent: float,
        amount: float,
        period_months: int,
        start_date: Optional[datetime] = None,
        replenishment_allowed: bool = False,
        auto_prolongation: bool = False,
        withdrawal_type: WithdrawalType = WithdrawalType.FULL_ONLY,
        capitalization: CapitalizationType = CapitalizationType.NONE,
    ) -> None:
        """
        Инициализирует объект Deposit.

        Args:
            percent: Процентная ставка за месяц (например, 0.5 для 0.5%).
            amount: Начальная сумма вклада.
            period_months: Срок вклада в месяцах.
            start_date: Дата открытия вклада. Если None, используется текущая дата.
            replenishment_allowed: Разрешено ли пополнение.
            auto_prolongation: Будет ли вклад автоматически продлён.
            withdrawal_type: Тип возможности снятия средств.
            capitalization: Тип капитализации процентов.

        Raises:
            ValueError: Если параметры некорректны.
        """
        if percent <= 0:
            raise ValueError("Процентная ставка должна быть положительной")
        if amount <= 0:
            raise ValueError("Сумма вклада должна быть положительной")
        if period_months <= 0:
            raise ValueError("Срок вклада должен быть положительным")

        self.percent = percent / 100  # Переводим процент в доли
        self.amount = amount
        self.initial_amount = amount
        self.period_months = period_months
        self.start_date = start_date or datetime.now()
        self.replenishment_allowed = replenishment_allowed
        self.auto_prolongation = auto_prolongation
        self.withdrawal_type = withdrawal_type
        self.capitalization = capitalization

        # Состояние вклада
        self.is_active = True
        self.last_calculation_date = self.start_date
        self.end_date = self._calculate_end_date()

    def _calculate_end_date(self) -> datetime:
        """Вычисляет дату окончания вклада."""
        # Прибавляем месяцы к дате
        year = self.start_date.year
        month = self.start_date.month + self.period_months
        while month > 12:
            year += 1
            month -= 12

        # Обрабатываем последний день месяца
        last_day = calendar.monthrange(year, month)[1]
        day = min(self.start_date.day, last_day)

        return datetime(year, month, day)

    def _calculate_interest(self, days: int) -> float:
        """
        Вычисляет проценты за указанный период.

        Args:
            days: Количество дней.

        Returns:
            Сумма процентов.
        """
        # Месячный процент пересчитываем пропорционально дням
        days_in_month = calendar.monthrange(
            self.last_calculation_date.year,
            self.last_calculation_date.month
        )[1]
        monthly_rate = self.percent / days_in_month * days
        return self.amount * monthly_rate

    def wait(self, days: int) -> float:
        """
        Ожидание указанного количества дней с начислением процентов.

        Args:
            days: Количество дней ожидания.

        Returns:
            Начисленные проценты.

        Raises:
            RuntimeError: Если вклад неактивен.
        """
        if not self.is_active:
            raise RuntimeError("Вклад закрыт")

        # Проверяем, не превышает ли период ожидания срок вклада
        current_date = self.last_calculation_date
        target_date = current_date + timedelta(days=days)

        if target_date > self.end_date:
            days = (self.end_date - current_date).days
            if days < 0:
                days = 0

        if days <= 0:
            return 0.0

        # Начисляем проценты
        interest = self._calculate_interest(days)

        if self.capitalization == CapitalizationType.MONTHLY:
            self.amount += interest
        # При отсутствии капитализации проценты не прибавляются к сумме

        self.last_calculation_date += timedelta(days=days)

        # Проверяем, не истёк ли срок вклада
        if self.last_calculation_date >= self.end_date:
            self._handle_maturity()

        return interest

    def _handle_maturity(self) -> None:
        """Обрабатывает окончание срока вклада."""
        if self.auto_prolongation:
            # Продлеваем вклад
            self.start_date = self.end_date
            self.end_date = self._calculate_end_date()
            self.last_calculation_date = self.start_date
            self.initial_amount = self.amount
        else:
            # Вклад закрывается
            self.is_active = False

    def replenish(self, amount: float) -> None:
        """
        Пополняет вклад.

        Args:
            amount: Сумма пополнения.

        Raises:
            RuntimeError: Если пополнение запрещено или вклад закрыт.
            ValueError: Если сумма пополнения неположительная.
        """
        if not self.is_active:
            raise RuntimeError("Нельзя пополнить закрытый вклад")

        if not self.replenishment_allowed:
            raise RuntimeError("Пополнение данного вклада запрещено")

        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")

        self.amount += amount

    def withdraw(self, amount: Optional[float] = None) -> float:
        """
        Снимает средства со вклада.

        Args:
            amount: Сумма для снятия. Если None, закрывает весь вклад.

        Returns:
            Сумма, полученная при снятии.

        Raises:
            RuntimeError: Если операция запрещена или вклад закрыт.
            ValueError: Если сумма снятия некорректна.
        """
        if not self.is_active:
            raise RuntimeError("Вклад уже закрыт")

        # Полное закрытие вклада
        if amount is None:
            if self.withdrawal_type == WithdrawalType.NONE:
                raise RuntimeError("Досрочное закрытие вклада запрещено")

            # При полном закрытии проценты не начисляются
            self.is_active = False
            return self.amount

        # Частичное снятие
        if self.withdrawal_type != WithdrawalType.PARTIAL:
            raise RuntimeError("Частичное снятие средств запрещено")

        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        if amount > self.amount:
            raise ValueError("Недостаточно средств на вкладе")

        self.amount -= amount
        return amount

    def close(self) -> float:
        """
        Закрывает вклад и возвращает средства.

        Returns:
            Итоговая сумма с учётом процентов.
        """
        if not self.is_active:
            raise RuntimeError("Вклад уже закрыт")

        # Доначисляем проценты до текущей даты
        today = datetime.now()
        if today > self.last_calculation_date:
            days = (today - self.last_calculation_date).days
            if days > 0:
                interest = self._calculate_interest(days)
                self.amount += interest

        self.is_active = False
        return self.amount

    def calculate_for_period(self, months: int) -> float:
        """
        Рассчитывает итоговую сумму за указанный период.

        Args:
            months: Количество месяцев.

        Returns:
            Итоговая сумма.
        """
        result = self.amount
        for _ in range(months):
            if self.capitalization == CapitalizationType.MONTHLY:
                result += result * self.percent
            else:
                result += self.amount * self.percent
        return result

    def get_info(self) -> dict:
        """
        Возвращает информацию о вкладе.

        Returns:
            Словарь с информацией о вкладе.
        """
        return {
            "Текущая сумма": f"{self.amount:.2f}",
            "Начальная сумма": f"{self.initial_amount:.2f}",
            "Процент (месячный)": f"{self.percent * 100:.2f}%",
            "Дата открытия": self.start_date.strftime("%d.%m.%Y"),
            "Дата окончания": self.end_date.strftime("%d.%m.%Y"),
            "Срок (месяцев)": self.period_months,
            "Пополнение": "Разрешено" if self.replenishment_allowed else "Запрещено",
            "Автопродление": "Да" if self.auto_prolongation else "Нет",
            "Снятие": self.withdrawal_type.value,
            "Капитализация": self.capitalization.value,
            "Активен": "Да" if self.is_active else "Нет",
        }


def main() -> None:

    # Пример 1: Классический вклад без пополнения и капитализации
    print("1. Классический вклад (без пополнения, без капитализации)")
    deposit1 = Deposit(
        percent=0.5,  # 0.5% в месяц
        amount=100000,
        period_months=12,
        replenishment_allowed=False,
        auto_prolongation=False,
        withdrawal_type=WithdrawalType.FULL_ONLY,
        capitalization=CapitalizationType.NONE
    )

    print("Информация о вкладе:")
    for key, value in deposit1.get_info().items():
        print(f"  {key}: {value}")

    # Ожидание 30 дней
    interest = deposit1.wait(30)
    print(f"\nЧерез 30 дней:")
    print(f"  Начислено процентов: {interest:.2f}")
    print(f"  Сумма на вкладе: {deposit1.amount:.2f}")

    # Ещё 30 дней
    interest = deposit1.wait(30)
    print(f"\nЕщё через 30 дней:")
    print(f"  Начислено процентов: {interest:.2f}")
    print(f"  Сумма на вкладе: {deposit1.amount:.2f}")

    # Закрытие вклада
    final_amount = deposit1.close()
    print(f"\nЗакрытие вклада:")
    print(f"  Итоговая сумма: {final_amount:.2f}")
    print()

    # Пример 2: Вклад с капитализацией и пополнением
    print("2. Вклад с ежемесячной капитализацией и возможностью пополнения")
    deposit2 = Deposit(
        percent=0.5,
        amount=50000,
        period_months=6,
        start_date=datetime(2024, 1, 1),
        replenishment_allowed=True,
        auto_prolongation=False,
        withdrawal_type=WithdrawalType.PARTIAL,
        capitalization=CapitalizationType.MONTHLY
    )

    print("Информация о вкладе:")
    for key, value in deposit2.get_info().items():
        print(f"  {key}: {value}")

    # Имитация нескольких месяцев
    print("\nИмитация 3 месяцев:")
    for month in range(1, 4):
        interest = deposit2.wait(30)
        print(f"  Месяц {month}: начислено {interest:.2f}, сумма {deposit2.amount:.2f}")

    # Пополнение
    print(f"\nПополнение на 20000:")
    deposit2.replenish(20000)
    print(f"  Сумма после пополнения: {deposit2.amount:.2f}")

    # Ещё 2 месяца
    for month in range(4, 6):
        interest = deposit2.wait(30)
        print(f"  Месяц {month}: начислено {interest:.2f}, сумма {deposit2.amount:.2f}")

    # Частичное снятие
    withdrawn = deposit2.withdraw(30000)
    print(f"\nЧастичное снятие 30000: получено {withdrawn:.2f}")
    print(f"  Остаток на вкладе: {deposit2.amount:.2f}")
    print()

    # Пример 3: Расчёт на период
    print("3. Расчёт на будущий период")
    deposit3 = Deposit(
        percent=0.5,
        amount=100000,
        period_months=12,
        capitalization=CapitalizationType.MONTHLY
    )

    for months in [3, 6, 12]:
        future = deposit3.calculate_for_period(months)
        print(f"  Через {months} месяцев: {future:.2f}")

    # Пример с запрещённым пополнением
    print("\nПопытка пополнить вклад без права пополнения:")
    deposit_no_replenish = Deposit(
        percent=0.5,
        amount=100000,
        period_months=6,
        replenishment_allowed=False
    )
    try:
        deposit_no_replenish.replenish(10000)
    except RuntimeError as e:
        print(f"  Ошибка: {e}")

    # Пример с запрещённым снятием
    print("\nПопытка частичного снятия с запретом:")
    deposit_no_withdrawal = Deposit(
        percent=0.5,
        amount=100000,
        period_months=6,
        withdrawal_type=WithdrawalType.NONE
    )
    try:
        deposit_no_withdrawal.withdraw(10000)
    except RuntimeError as e:
        print(f"  Ошибка: {e}")


if __name__ == "__main__":
    main()
def count_full_check(account_sum: int, service_charge_percent: int) -> str:
    service_charge = (account_sum * service_charge_percent) / 100
    check_with_charge = account_sum + service_charge

    account_sum_string = "Счет: " + f"{account_sum} руб. "
    service_charge_string = "Чаевые (" + f"{service_charge_percent}%): {service_charge} руб. "
    full_check_string = "Итого: " + f"{check_with_charge} руб."

    return account_sum_string + service_charge_string + full_check_string


def main():
    account_sum = int(input("Во сколько вам обошелся чек? "))
    service_charge_percent = int(input("Сколько процентов чаевых вы хотите заплатить? "))
    
    print(count_full_check(account_sum, service_charge_percent))


if __name__ == "__main__":
    main()
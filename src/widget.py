from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает её с замаскированным номером."""
    space_count = info.count(" ")

    if space_count == 0:
        return "Ошибка: некорректный формат ввода!"

    name, number = info.rsplit(" ", 1)

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
        return f"Счет {masked_number}"

    elif space_count > 1 and "счет" in name.lower():
        return "Ошибка: для счета должно быть передано строго два слова!"

    else:
        masked_number = get_mask_card_number(number)
        return f"{name.title()} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку с датой и возвращает её в формате ДД.ММ.ГГГГ."""
    only_date = date_str.split("T")[0]
    date_obj = datetime.fromisoformat(only_date)

    return date_obj.strftime("%d.%m.%Y")

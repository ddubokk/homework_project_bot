from src.widget import mask_account_card

if __name__ == "__main__":
    while True:
        user_input = input(
            "\nВведите данные (В формате: Visa 1234567812345678, Счет 1234567890... или введите exit для выхода): "
        ).strip()

        if user_input.lower() == "exit":
            print("Программа завершена.")
            break

        if user_input == "":
            print("Строка не должна быть пустой. Попробуйте еще раз.")
            continue

        result = mask_account_card(user_input)
        if result.startswith("Ошибка:"):
            print(result)
        else:
            print(f"Результат: {result}")
            break

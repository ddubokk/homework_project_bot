from src.widget import get_date

if __name__ == "__main__":
    sample_date = input("Входная строка: ")

    formatted_result = get_date(sample_date)

    print(f"Вывод функции:  {formatted_result}")

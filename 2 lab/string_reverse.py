def main():
    text = input("Введите три слова через пробел: ")
    
    words = text.split()
    
    reversed_words = words[::-1]
    
    print("Разные способы соединения слов:")
    print("1. Через join:", '_'.join(reversed_words))
    print("2. Через f-строку:", f"{reversed_words[0]}_{reversed_words[1]}_{reversed_words[2]}")
    print("3. Через ручную конкатенацию:", reversed_words[0] + '_' + reversed_words[1] + '_' + reversed_words[2])


if __name__ == "__main__":
    main()
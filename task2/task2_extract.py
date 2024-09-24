# Модуль 2: Извлечение информации
def bits_to_text(bits):
    """Преобразование битовой строки обратно в текст."""
    chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)


def extract_data(container_with_secret_file):
    # Массивы соответствия русских и английских букв
    rus_to_eng = {'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
                  'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X'}
    eng_to_rus = {v: k for k, v in rus_to_eng.items()}

    # Чтение контейнера с секретом
    with open(container_with_secret_file, 'r', encoding='utf-8') as container:
        container_text = container.read()

    # Извлечение битов из контейнера
    secret_bits = []
    for char in container_text:
        if char in rus_to_eng:  # Если это русская буква
            secret_bits.append('0')
        elif char in eng_to_rus:  # Если это англ. аналог
            secret_bits.append('1')

    # Преобразуем биты в текст
    print(''.join(secret_bits))
    secret_text = bits_to_text(''.join(secret_bits))

    return secret_text


# Пример использования
container_with_secret_file = './container.txt'
secret_message = extract_data(container_with_secret_file)
print(f"Скрытое сообщение: {secret_message}")

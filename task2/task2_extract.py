from letter_map import letter_map


def bits_to_text(bits):
    """Преобразование битовой строки обратно в текст."""
    # Разбиваем биты на байты по 8 бит
    byte_array = bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    # Декодируем байты в текст с кодировкой cp1251
    return byte_array.decode('cp1251', errors='ignore')


def extract_data(container_with_secret_file):
    rus_to_eng = letter_map
    eng_to_rus = {v: k for k, v in rus_to_eng.items()}

    with open(container_with_secret_file, 'r', encoding='utf-8') as container:
        container_text = container.read()

    secret_bits = []
    for char in container_text:
        if char in rus_to_eng:  # Если это русская буква
            secret_bits.append('0')
        elif char in eng_to_rus:  # Если это англ. аналог
            secret_bits.append('1')

        # Проверка на конец скрытого сообщения
        if len(secret_bits) >= 8 and ''.join(secret_bits[-8:]) == '00000000':
            # Удаляем маркер окончания
            secret_bits = secret_bits[:-8]
            break

    print(''.join(secret_bits))
    secret_text = bits_to_text(''.join(secret_bits))

    with open('message.txt', 'w', encoding='utf-8') as message_file:
        message_file.write(secret_text)

    return secret_text


container_with_secret_file = './container.txt'
secret_message = extract_data(container_with_secret_file)
print(f"Скрытое сообщение: {secret_message}")

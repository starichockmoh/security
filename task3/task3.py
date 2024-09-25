ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


# генерация таблицы сдвигом
def get_table():
    table = []
    for i in range(len(ALPHABET)):
        table.append(ALPHABET[i:] + ALPHABET[:i])
    return table


def encrypt(secret_text, key):
    table = get_table()
    print(table)
    # под каждой буквой шифруемого текста записываются буквы ключа.
    # Ключ при этом повторяется необходимое число раз
    key = key * (len(secret_text) // len(key)) + key[:len(secret_text) % len(key)]
    result = ''

    for i in range(len(secret_text)):
        if secret_text[i] in ALPHABET:
            row = ALPHABET.index(key[i])  # Буква ключа
            col = ALPHABET.index(secret_text[i])  # Буква секретного текста
            result += table[row][col]
        else:
            result += secret_text[i]  # Если символ не в алфавите, оставляем его

    return result


def decrypt(result, key):
    table = get_table()
    # над буквами зашифрованного текста последовательно надписываются буквы ключа,
    # причем ключ повторяется необходимое количество раз
    key = key * (len(result) // len(key)) + key[:len(result) % len(key)]
    secret_text = ''

    for i in range(len(result)):
        if result[i] in ALPHABET:
            row = ALPHABET.index(key[i])  # Буква ключа
            col = table[row].index(result[i])  # Колонка с буквой зашифрованного текста
            secret_text += ALPHABET[col]
        else:
            secret_text += result[i]  # Если символ не в алфавите, оставляем его

    return secret_text


secret_text = input("Текст: ").upper()
key = input("Ключ: ").upper()

result = encrypt(secret_text, key)
print("Зашифрованный текст:", result)

result_text = decrypt(result, key)
print("Расшифрованный текст:", result_text)

# with open("./result_text.txt", "w", encoding="utf-8") as f:
#     f.write(result_text)

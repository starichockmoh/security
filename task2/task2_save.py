from functools import reduce
from letter_map import letter_map


def save_container(container_path, message):
    binary_data = message.encode('cp1251')
    secret_bits = reduce(lambda acc, bit_item: acc + bin(bit_item)[2:].rjust(8, '0'), binary_data, '')
    secret_bits = secret_bits + '00000000'
    print(secret_bits)

    with open(container_path, "r", encoding="utf-8") as f:
        container_content = f.read()

    bit_index = 0
    container_list = list(container_content)

    # Проход по тексту контейнера
    for i, char in enumerate(container_list):
        if char in letter_map:  # Если символ контейнера имеет аналог
            if bit_index < len(secret_bits):
                bit = secret_bits[bit_index]
                if bit == '1':  # Если бит 1, заменяем на англ. аналог
                    container_list[i] = letter_map[char]
                # Если бит 0, оставляем русскую букву без изменений
                bit_index += 1
            else:
                break  # Если все биты были скрыты, завершаем цикл

    with open(container_path, "w", encoding="utf-8") as f:
        f.write(''.join(container_list))


message = "Aвг"

container_path = "./container.txt"

save_container(container_path, message)

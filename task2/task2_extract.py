from letter_map import letter_map


def extract_message(container_path):
    reverse_letter_map = {v: k for k, v in letter_map.items()}
    END = "0010000000101110"
    # Читаем содержимое файла
    with open(container_path, "r", encoding="utf-8") as f:
        content = f.read()
    bin_message = ""
    for char in content:
        if char in letter_map:
            bin_message += '0'
        if char in reverse_letter_map:
            bin_message += '1'
        if len(bin_message) > 16:
            if bin_message[-16:] == END:
                break
    bits = bin_message[:-16]
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        byte_array.append(int(byte, 2))

    return byte_array.decode('cp1251')


# Пример использования
container_path = "./container.txt"
extracted_message = extract_message(container_path)
print(f"Извлеченное сообщение: {extracted_message}")

with open("extracted_message.txt", "w", encoding="utf-8") as f:
    f.write(extracted_message)

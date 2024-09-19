import os

def calculate_xor_checksum(file_path):
    checksum = 0

    with open(file_path, 'rb') as file:
        while True:
            # Читаем 2 байта (16 бит)
            chunk = file.read(2)

            if len(chunk) == 0:
                break

            # Если последний отрезок меньше 2 байт, дополняем его нулями
            if len(chunk) < 2:
                # Дополнение нулями, если chunk содержит меньше 16 бит (менее 2 байт)
                chunk = chunk.ljust(2, b'\x00')

            # Преобразуем байты в 16-битное целое число
            segment = int.from_bytes(chunk, byteorder='big')
            # Применяем XOR
            checksum ^= segment

    return checksum

# Устанавливаем текущую директорию
current_directory = os.getcwd()

# Обход всех подкаталогов и файлов
for root, dirs, files in os.walk(current_directory):
    for file in files:
        file_path = os.path.join(root, file)
        result = calculate_xor_checksum(file_path)
        print(f"ХЭШ-сумма (XOR): {result}")
        print(f"Файл: {file_path}")
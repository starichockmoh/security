import os

HASH_FILE = 'hashes.txt'  # Имя файла для сохранения хэш-сумм


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


def save_hashes(directory, hash_file=HASH_FILE):
    """Сохраняет хэш-суммы всех файлов в каталоге."""
    with open(os.path.join(directory, hash_file), 'w') as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == hash_file:
                    continue  # Пропускаем файл с хэшами
                file_path = os.path.join(root, file)
                hash_value = calculate_xor_checksum(file_path)
                # Сохраняем относительный путь и хэш-сумму
                f.write(f"{os.path.relpath(file_path, directory)}:{hash_value}\n")
    print(f"Хэш-суммы сохранены в файл {hash_file}")


def load_hashes(directory, hash_file=HASH_FILE):
    """Загружает хэш-суммы из файла."""
    hash_map = {}
    try:
        with open(os.path.join(directory, hash_file), 'r') as f:
            for line in f:
                rel_path, hash_value = line.strip().split(':')
                hash_map[rel_path] = int(hash_value)
    except FileNotFoundError:
        print(f"Файл {hash_file} не найден.")
    return hash_map


def check_integrity(directory, hash_file=HASH_FILE):
    """Проверяет целостность файлов в каталоге на основе сохраненных хэш-сумм."""
    stored_hashes = load_hashes(directory, hash_file)
    current_hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == hash_file:
                continue  # Пропускаем файл с хэшами
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            current_hashes[rel_path] = calculate_xor_checksum(file_path)

    changed_files = []
    for rel_path, stored_hash in stored_hashes.items():
        current_hash = current_hashes.get(rel_path)
        if current_hash is None:
            print(f"Файл {rel_path} был удален.")
        elif stored_hash != current_hash:
            changed_files.append(rel_path)
            print(f"Файл {rel_path} был изменен.")

    for rel_path in current_hashes.keys() - stored_hashes.keys():
        print(f"Новый файл {rel_path} был добавлен.")

    if not changed_files:
        print("Все файлы на месте и не изменялись.")


def check_file_exists(file_path):
    return os.path.isfile(file_path)


# if __name__ == "__main__":
#     directory = input("Введите путь к каталогу для контроля целостности: ")
#
#     hashFilePath = os.path.join(directory, HASH_FILE)
#     if not check_file_exists(hashFilePath):
#         save_hashes(directory)
#     else:
#         check_integrity(directory)
#         save_hashes(directory)


if __name__ == "__main__":
    directory = input("Введите путь к каталогу для контроля целостности: ")

    hashFilePath = os.path.join(directory, HASH_FILE)
    if not check_file_exists(hashFilePath):
        action = input("Выберите действие - [1] Сохранить хэши: ")
        if action == '1':
            save_hashes(directory)
        else:
            print("Неверный выбор.")
    else:
        action = input("Выберите действие - [1] Сохранить хэши, [2] Проверить целостность: ")
        if action == '1':
            save_hashes(directory)
        elif action == '2':
            check_integrity(directory)
        else:
            print("Неверный выбор.")


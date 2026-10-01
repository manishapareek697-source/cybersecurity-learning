import hashlib
import os


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


file_path = input("Enter file path: ")

if os.path.exists(file_path):
    file_hash = calculate_hash(file_path)

    print("\nSHA-256 Hash:")
    print(file_hash)

else:
    print("File not found!")
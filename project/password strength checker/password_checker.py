import re

password = input("Enter a password to check: ")

score = 0

if len(password) >= 8:
    score += 1

if re.search(r"[A-Z]", password):
    score += 1

if re.search(r"[a-z]", password):
    score += 1

if re.search(r"[0-9]", password):
    score += 1

if re.search(r"[^A-Za-z0-9]", password):
    score += 1

if score <= 2:
    print("Weak password")
elif score <= 4:
    print("Medium password")
else:
    print("Strong password")
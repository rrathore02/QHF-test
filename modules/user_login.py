import os
from datetime import datetime

def get_user_info():
    print("\nWelcome to the QHF Tool!")
    name = input("Enter your name or organization (optional): ").strip()
    email = input("Enter your email (optional, for updates): ").strip()

    # Create log directory if it doesn't exist
    if not os.path.exists("user_logs"):
        os.makedirs("user_logs")

    # Save login info locally
    with open("user_logs/logins.csv", "a") as f:
        f.write(f"{datetime.now()}, {name}, {email}\n")

    print(f"\nThanks, {name or 'user'}! Your login has been recorded.\n")
    return name, email

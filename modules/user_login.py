import os
import csv
import json
from datetime import datetime
from modules.email_sender import send_welcome_email

MODULE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(MODULE_DIR, "user_logs.csv")
CACHE_FILE = os.path.join(MODULE_DIR, ".user_cache.json")

def load_cached_user():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None

def save_user_to_cache(name, email):
    with open(CACHE_FILE, "w") as f:
        json.dump({"name": name, "email": email}, f)

def get_user_info():
    cached_user = load_cached_user()

    if cached_user:
        name = cached_user["name"]
        email = cached_user["email"]
        print(f"\n👋 Welcome back, {name}!\n")
    else:
        print("\nWelcome to the QHF Tool!")
        name = input("Enter your name or organization (optional): ").strip() or "Anonymous"
        email = input("Enter your email (optional, for updates): ").strip() or "Anonymous"
        save_user_to_cache(name, email)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users = []
    is_new_user = True

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            users = list(reader)

    for user in users:
        if user["Name"] == name and user["Email"] == email:
            user["Login Count"] = str(int(user["Login Count"]) + 1)
            user["Last Access"] = timestamp
            is_new_user = False
            break

    if is_new_user:
        users.append({
            "Name": name,
            "Email": email,
            "Login Count": "1",
            "Last Access": timestamp
        })

        if email != "Anonymous":
            send_welcome_email(email, name)

    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Email", "Login Count", "Last Access"])
        writer.writeheader()
        writer.writerows(users)

    print(f"📅 Last Access: {timestamp} | Total Logins: {[u for u in users if u['Name'] == name and u['Email'] == email][0]['Login Count']}\n")

    return name, email

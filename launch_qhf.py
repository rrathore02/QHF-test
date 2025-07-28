from modules.version_checker import check_for_update
from modules.user_login import get_user_info
import os

def main():
    print("="*50)
    print("        QHF TOOL LAUNCHER")
    print("="*50)

    # Step 1: Version check
    check_for_update()

    # Step 2: Optional login
    name, email = get_user_info()

    # Step 3: Launch main QHF logic
    print(f"\nStarting simulation for {name or 'anonymous user'}...\n")

    # Replace this with the actual entry point or command to launch QHF.py
    os.system("python QHF.py")

if __name__ == "__main__":
    main()

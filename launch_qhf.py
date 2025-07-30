# launch_qhf.py

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

    # Step 3: Launch QHF with config file
    config_path = "Configs/europa.cfg"  # or change this to another .cfg if needed
    print(f"\nStarting simulation for {name or 'anonymous user'} using config: {config_path}...\n")

    os.system(f"python QHF.py {config_path}")

if __name__ == "__main__":
    main()

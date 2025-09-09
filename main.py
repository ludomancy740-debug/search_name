from storage import load_accounts, save_accounts
from menus import main_menu


def main():
    accounts = load_accounts()
    try:
        main_menu(accounts)
    finally:
        save_accounts(accounts)


if __name__ == "__main__":
    main()

'''
Main function of the system :D
'''

# import function from other file yiz
# from [filename] import [yung function]

from auth import login, register
from listings import listing_menu

def main_menu():
    while True:
        print("\n=== LOST & FOUND SYSTEM ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            user = login()
            if user:
                print("Welcome to User Dashboard")
                listing_menu(user)
        elif choice == '2':
            user = register()
            if user:
                listing_menu(user)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
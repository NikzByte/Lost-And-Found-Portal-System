'''
used for handling login and registration
'''
import hashlib

def read_logins():
    with open('logins.txt', 'r') as f: #reads(r) the content inside 'logins.txt'
        contents = f.readlines()

        new_contents = []
        
        for line in contents:
            clean_line = line.strip() 
            if clean_line: # This ignores empty lines
                fields = clean_line.split(',')
                new_contents.append(fields)
        
        return new_contents
logins = read_logins()

def register():
    print("\nCreate New Account")
    new_username = input("Enter a Username: ").lower()
    new_gsuiteEmail = input("Enter Your Gsuite Email: ")
    new_password = input("Enter a Password: ") 
    # include strong password logic in the future
    
    # hash the password before saving it on logins.txt
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    
    with open('logins.txt', 'a') as f:
        f.write(f"{new_username},{new_gsuiteEmail},{hashed_password}\n")
        
        print("Registration Successful! You can now log in.")

        logins = read_logins()

def login():
    while True:
        print("\nLog Into Your Account")
        ask_userName = input("Enter username: ").lower()
        ask_gsuiteEmail = input("Enter your Gsuite Email: ")
        ask_password = input("Enter password: ")
        hashed_input = hashlib.sha256(ask_password.encode()).hexdigest() # Hash the input so we can compare it to the stored version
        
        logged_in = False

        for user_data in read_logins():
            if (user_data[0] == ask_userName and user_data[1] == ask_gsuiteEmail and user_data[2]  == hashed_input): 
                logged_in = True
                break
                    
        if logged_in:
            print("Successfully Logged In!")
            return True
        else:
            print("Username/Gsuite/Password Is Incorrect. Try again.\n")    

def main_menu():
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            if login():
                print("\nWelcome to User Dashboard!")
                # user_dashboard
                break
        elif choice == '2':
            register()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            
if __name__ == "__main__":
    main_menu()

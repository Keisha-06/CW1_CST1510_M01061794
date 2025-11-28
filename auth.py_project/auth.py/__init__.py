import bcrypt
import os
USER_DATA_FILE = "users.txt"

user = input('Provide a password: ')
def hash_password(text): 
    bytes = text.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    userpass = hash.decode('utf-8')
    with open('User-data.txt', 'w') as f:
        f.write(userpass)
    return(hash)
hash_password(user)
with open('User-data.txt', 'r') as f:
    data = f.read()
#print(data)
def verify_password(text: str) -> bool:
    with open('User-data.txt', 'r') as f:
        stored = f.read().strip()
        if not stored:
            raise ValueError("No password stored in txt")
        plain = text.encode('utf-8')
        hash = stored.encode('utf-8')
        return bcrypt.checkpw(plain, hash) 

result = verify_password(user)
print(result)
hashed = hash_password(user)
print(f"Original password: {user}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")


def register_user(username, password):
    with open('users.txt', 'r') as f:
        for line in f:
            line  = line.strip()
            existing = line.split(',')[0].strip()
            if username == existing: 
                print(f'User name {username} is taken. Try again.')
                return (False, 'User name is taken. Try again.')
        localhash = hash_password(password)
        localhashed = localhash.decode('utf-8')
        entry = f'{username}, {localhashed}\n'
        with open('users.txt', 'a') as f_append:
            f_append.write(entry)
        return (True, 'User registered successfully')
username_input = input('Enter a Username: ')
password_input = input('Enter Password: ')
hashedpass = register_user(username_input, password_input)
hashedpass

def user_exists(username):
    try:
        with open('users.txt', 'r') as f:
        # File exists, do something
            pass
    except FileNotFoundError:
        print("File doesn't exist")
    with open('users.txt', 'r') as f:
        for line in f:
            line = line.strip()
            exists = line.split(',')[0].strip()
            if username == exists:
                print(f'{username} already exists')
                return False
#user_exists('Zkhan')

import bcrypt

def login_user(username, password):
    try:
        # Check if user exists and verify password
        with open('users.txt', 'r') as f:
            for line in f:
                line = line.strip()
                stored_username, stored_password_hash = line.split(',')
                stored_username = stored_username.strip()
                stored_password_hash = stored_password_hash.strip()
                
                if username == stored_username:
                    # Convert stored hash string to bytes for bcrypt
                    stored_hash_bytes = stored_password_hash.encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash_bytes):
                        print(f'Login successful! Welcome {username}')
                        return True
                    else:
                        print('Incorrect password')
                        return False
            
            # If we get here, no matching username was found
            print(f'User {username} not found')
            return False
            
    except FileNotFoundError:
        print("User database not found. No users registered yet.")
        return False
            
def validate_username(username):
    if isinstance(username, str):
        return True, ""  # (is_valid, error_message)
    else:
        return False, f"'{username}' is not in correct format - expected string"

def validate_password(password):
    if isinstance(password, str):
        return True, ""  # (is_valid, error_message)
    else:
        return False, f"'{password}' is not in correct format - expected string"
    

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            
            # Validate Password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
                
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard)")
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
                
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
pip3 install bcrypt

import bcrypt
import os

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def verify_password(plain_text_password, hashed password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

test_password = "SecurePassword123"
hashed = hash_password(test_password) 
print(f"Original password: {test_password}") 
print(f"Hashed password: {hashed}") 
print(f"Hash length: {len(hashed)} characters")

is_valid = verify_password(test_password, hashed) 
print(f"\nVerification with correct password: {is_valid}")

is_invalid = verify_password("WrongPassword", hashed) 
print(f"Verification with incorrect password: {is_invalid}")

USER_DATA_FILE = "users.txt"

def register_user(username, password):
    if user_exists(username):
        print("Username already exists. Please choose a different username.")
        return False
    hashed_password = hash_password(password).decode('utf-8')
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print("User registered successfully.")
    return True
    
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username, _ = line.strip().split(",", 1)
            if stored_username == username:
                return True
    return False

def login_user(username, password):
    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines():
            user, hash = line.strip().split(",", 1)
            if user == username:
                return verify_password(password, hash)
    return False

def validate_username(username):
    pass

def validate_password(password):
    pass
    
def display_menu():    
    """Displays the main menu options."""    
    print("\n" + "="*50)    
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")    
    print("  Secure Authentication System")    
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
            print("\n--- USER REGISTRATION ---")            
            username = input("Enter a username: ").strip()                                    
            
            is_valid, error_msg = validate_username(username)            
            if not is_valid:                
                print(f"Error: {error_msg}")                
                continue                        
            password = input("Enter a password: ").strip()

            is_valid, error_msg = validate_password(password)            
            if not is_valid:                
                print(f"Error: {error_msg}")                
                continue
                
            password_confirm = input("Confirm password: ").strip()           
            if password != password_confirm:                
                print("Error: Passwords do not match.")                
                continue
                
            register_user(username, password)

        elif choice == '2':                       
            print("\n--- USER LOGIN ---")            
            username = input("Enter your username: ").strip()            
            password = input("Enter your password: ").strip()                                    
            
            if login_user(username, password):                
                print("\nYou are now logged in.")                
                print("In a real application, you would now access the d ")                               
                                     
                input("\nPress Enter to return to main menu...")                
                
        elif choice == '3':                       
            print("\nThank you for using the authentication system.")            
            print("Exiting...")            
            break                
        
        else:            
            print("\nError: Invalid option. Please select 1, 2, or 3.") 
            
            
if __name__ == "__main__":    
    main()
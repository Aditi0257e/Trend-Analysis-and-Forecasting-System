import csv
import os

def register():
    file_exists = os.path.isfile("User_Pass.csv")
    
    with open("User_Pass.csv", mode="a", newline='') as f:
        fieldnames = ['Customer Name', 'Ph no', 'username', 'password']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write header if file does not exist
        if not file_exists:
            writer.writeheader()
        
        CustomerName = input("Please enter the name: ")
        Phone = input("Please enter the phone No.: ")
        password = input("Enter a password: ")
        password2 = input("Please rewrite the password: ")
        
        if password == password2:
            username = Phone
            writer.writerow({'Customer Name': CustomerName, 'Ph no': Phone, 'username': username, 'password': password})
            print("Registration is successful")
        else:
            print("Passwords do not match. Please try again.")
        
def login():
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        username = input("Please enter username: ")
        password = input("Please enter your password: ")
        
        with open("User_Pass.csv", mode="r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    print("You are logged in!")
                    return True
        
        attempts += 1
        if attempts < max_attempts:
            print(f"Login failed. You have {max_attempts - attempts} attempt(s) left. Please try again.")
        else:
            print("Login failed. No attempts left.")
    
    return False

def forgot_password():
    username = input("Please enter your username: ")
    new_password = input("Please enter your new password: ")
    new_password2 = input("Please rewrite the new password: ")
    
    if new_password != new_password2:
        print("Passwords do not match. Please try again.")
        return
    
    updated = False
    rows = []
    
    with open("User_Pass.csv", mode="r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                row["password"] = new_password
                updated = True
            rows.append(row)
    
    if updated:
        with open("User_Pass.csv", mode="w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Customer Name', 'Ph no', 'username', 'password'])
            writer.writeheader()
            writer.writerows(rows)
        print("Password has been reset successfully.")
    else:
        print("Username not found. Please try again.")

# Main Menu
def main_menu():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            if login():
                break
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main menu
main_menu()

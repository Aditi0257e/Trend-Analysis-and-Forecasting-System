import csv
import os
import json

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}

def get_recommendations(user_search_history, trending_hashtags):
    recommendations = [hashtag for hashtag in trending_hashtags if hashtag in user_search_history]
    print(f"User search history: {user_search_history}")
    print(f"Trending hashtags: {trending_hashtags}")
    print(f"Recommendations: {recommendations}")
    return recommendations

def search_nested_dict(search_term, data, results=None):
    if results is None:
        results = []
    for key, value in data.items():
        if search_term in key:
            results.append((key, value))
        if isinstance(value, dict):
            search_nested_dict(search_term, value, results)
    return results

def search_products(search_term, hashtags_data):
    search_term = f"#{search_term.lower()}"
    found = False

    # Direct and partial matches
    results = search_nested_dict(search_term, hashtags_data)

    if results:
        found = True
        for key, related_products in results:
            print(f"Related products for '{key}':")
            if isinstance(related_products, dict):
                for related_hashtag, products in related_products.items():
                    print(f"{related_hashtag}: {products}")
            elif isinstance(related_products, list):
                print(f"{key}: {related_products}")

    if not found:
        print(f"No related products found for '{search_term}'")

def register():
    file_exists = os.path.isfile("User_Pass.csv")
    
    with open("User_Pass.csv", mode="a", newline='') as f:
        fieldnames = ['Customer Name', 'Ph no', 'username', 'password']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        customer_name = input("Please enter the name: ")
        phone = input("Please enter the phone No.: ")
        password = input("Enter a password: ")
        password2 = input("Please rewrite the password: ")
        
        if password == password2:
            username = phone
            writer.writerow({'Customer Name': customer_name, 'Ph no': phone, 'username': username, 'password': password})
            print("Registration is successful")
        else:
            print("Passwords do not match. Please try again.")
        
def login(trending_hashtags, hashtags_data):
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        username = input("Please enter username: ")
        password = input("Please enter your password: ")
        
        with open("User_Pass.csv", mode="r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    full_name = row["Customer Name"]
                    first_name = full_name.split()[0]  # Get only the first name
                    print(f"You are logged in as {first_name}!")
                    user_data_path = f'myntra_search_history_{first_name}.json'
                    user_data = load_json(user_data_path)
                    user_search_history = user_data.get(username, [])
                    if user_search_history:
                        recommendations = get_recommendations(user_search_history, trending_hashtags)
                        print(f"Recommendations for you: {recommendations}")
                    else:
                        print(f"No search history found. Trending hashtags for you: {trending_hashtags}")
                    search_bar(trending_hashtags, hashtags_data)
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

def search_bar(trending_hashtags, hashtags_data):
    while True:
        search_term = input("Search for a product (type 'exit' to quit): ")
        if search_term.lower() == 'exit':
            break
        search_products(search_term, hashtags_data)

def main_menu():
    trending_hashtags_path = r'E:\Gui_myntra\all_hastags_post_counts_new.json'  # Adjust path to your JSON file location
    hashtags_data_path = r'feasible_hashtag_pairs_with_products.json'
    
    trending_hashtags_data = load_json(trending_hashtags_path)
    trending_hashtags = list(trending_hashtags_data.keys())
    
    hashtags_data = load_json(hashtags_data_path)
    
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            if login(trending_hashtags, hashtags_data):
                break
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main menu
main_menu()
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

def get_search_queries(user_search_history_data):
    search_queries = []
    for entry in user_search_history_data.get('searchHistory', []):
        search_queries.append(entry.get('searchQuery', '').lower())
    return search_queries

def get_recommendations(user_search_queries, trending_hashtags):
    recommendations = set()  # Use a set to automatically handle duplicates
    
    for query in user_search_queries:
        for hashtag in trending_hashtags:
            if hashtag in query:
                recommendations.add(hashtag)
    
    return list(recommendations)  # Convert set back to list before returning

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
        
def login(trending_hashtags):
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
                    first_name = full_name.split()[0].lower()  # Get only the first name and convert to lower case
                    print(f"You are logged in as {first_name}!")
                    user_data_path = f'E:\\Gui_myntra\\myntra_search_history_{first_name}.json'
                    user_search_history_data = load_json(user_data_path)
                    user_search_queries = get_search_queries(user_search_history_data)
                    recommendations = get_recommendations(user_search_queries, trending_hashtags)
                    print(f"Recommendations for you: {recommendations}")
                    
                    search_bar(recommendations, trending_hashtags, user_search_history_data)
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

def search_products(search_term, product_data):
    matching_products = []
    for key, value in product_data.items():
        if search_term in key:
            matching_products.append((key, value))
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                if search_term in subkey:
                    matching_products.append((key, {subkey: subvalue}))
                elif any(search_term in item.lower() for item in subvalue):
                    matching_products.append((key, {subkey: subvalue}))
    return matching_products

def display_products(products):
    grouped_products = {}
    for superkey, subvalue in products:
        if superkey not in grouped_products:
            grouped_products[superkey] = {}
        if isinstance(subvalue, dict):
            for subkey, subval in subvalue.items():
                if subkey not in grouped_products[superkey]:
                    grouped_products[superkey][subkey] = []
                grouped_products[superkey][subkey].extend(subval)
        elif isinstance(subvalue, list):
            if "Others" not in grouped_products[superkey]:
                grouped_products[superkey]["Others"] = []
            grouped_products[superkey]["Others"].extend(subvalue)
    
    for superkey, subgroups in grouped_products.items():
        print(f"\n{superkey.capitalize()}:")
        for subkey, items in subgroups.items():
            print(f"  {subkey.capitalize()}: {', '.join(items)}")
        print()  # Add space between product groups

def search_bar(recommendations, trending_hashtags, user_search_history_data):
    product_data = load_json('feasible_hashtag_pairs_with_products.json')
    
    while True:
        search_query = input("Enter your search query (or type 'exit' to return to the main menu): ").lower()
        if search_query == 'exit':
            break
        
        matching_recommendations = list(set(tag for tag in recommendations if search_query in tag))
        matching_trending = list(set(tag for tag in trending_hashtags if search_query in tag))
        
        combined_matches = list(set(matching_recommendations + matching_trending))
        
        if combined_matches:
            print(f"Matching Recommendations and Trending Hashtags: {combined_matches}")
            
            print("\nProducts:")
            displayed_products = set()
            for query in combined_matches:
                matching_products = search_products(query, product_data)
                display_products(matching_products)
        
        # Display user search history products
        print("\nUser Search History Products:")
        history_displayed = False
        for entry in user_search_history_data.get('searchHistory', []):
            if search_query in entry['searchQuery'].lower():
                if not history_displayed:
                    print(f"\n{entry['searchQuery']}:")
                    history_displayed = True
                for product in entry.get('productResults', []):
                    print(f"  {product['productName']} - {product['productId']}")
        
        if not combined_matches and not history_displayed:
            print("No matching recommendations, trending hashtags, or search history products found.")

def main_menu():
    trending_hashtags_path = r'E:\\Gui_myntra\\all_hastags_post_counts_new.json'
    trending_hashtags_data = load_json(trending_hashtags_path)
    
    # Aggregate trending hashtags
    trending_hashtags = list(trending_hashtags_data.keys())
    
    print(f"Trending hashtags: {trending_hashtags}")
    
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            if login(trending_hashtags):
                break
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main menu
main_menu()

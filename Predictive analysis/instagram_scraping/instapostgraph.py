from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from collections import defaultdict
import json
import matplotlib.pyplot as plt

# Set up the WebDriver
chrome_driver_path = r'E:\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Adjust path to your ChromeDriver executable
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Log in to Instagram (replace with your username and password)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)

username.send_keys("USERNAME")
password.send_keys("PASSWORD")
password.send_keys(Keys.RETURN)
time.sleep(5)

# Handle the "Save Your Login Info?" dialog if it appears
try:
    not_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
    )
    not_now_button.click()
except:
    print("Save your login info dialog not found")

time.sleep(2)

# Handle the "Turn on Notifications" dialog if it appears
try:
    not_now_button_notifications = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
    )
    not_now_button_notifications.click()
except:
    print("Turn on notifications dialog not found")

# Define the hashtags to search
hashtags = ['saree', 'blackdress', 'floralprint', 'beachy', 'tropicalprints']  # Add your desired hashtags here

# Define the date threshold (5 days ago from today)
date_threshold = datetime.now() - timedelta(days=5)

# Dictionary to store the count of posts per date for each hashtag
hashtag_data = {hashtag: defaultdict(int) for hashtag in hashtags}

for hashtag in hashtags:
    # Navigate to the hashtag page
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    time.sleep(5)

    # Scroll down to load more posts
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all posts
    posts = soup.find_all('a', href=lambda x: x and x.startswith("/p/"))

    for post in posts:
        post_url = "https://www.instagram.com" + post['href']
        driver.get(post_url)
        time.sleep(2)

        post_soup = BeautifulSoup(driver.page_source, 'html.parser')
        time_element = post_soup.find('time')

        if time_element:
            post_date_str = time_element['datetime']
            
            try:
                post_date = datetime.strptime(post_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                post_date = datetime.strptime(post_date_str, "%Y-%m-%dT%H:%M:%SZ")
            
            if post_date > date_threshold:
                post_date_formatted = post_date.strftime('%Y-%m-%d')
                hashtag_data[hashtag][post_date_formatted] += 1

# Save the hashtag data to a JSON file
with open('hashtag_data.json', 'w') as f:
    json.dump(hashtag_data, f, indent=4, default=str)

# Print the dates and counts of recent posts for each hashtag
for hashtag, date_post_count in hashtag_data.items():
    print(f"Number of posts under #{hashtag} in the last 5 days:")
    for date, count in date_post_count.items():
        print(f"{date}: {count} posts")

# Close the driver
driver.quit()

# Load data from JSON file
with open('hashtag_data.json', 'r') as f:
    hashtag_data = json.load(f)

# Convert date strings back to datetime objects for sorting
for hashtag, date_post_count in hashtag_data.items():
    for date_str in date_post_count:
        date_post_count[date_str] = int(date_post_count[date_str])

# Plot the data
plt.figure(figsize=(12, 8))

for hashtag, date_post_count in hashtag_data.items():
    dates = sorted(date_post_count.keys())
    counts = [date_post_count[date] for date in dates]
    
    plt.plot(dates, counts, marker='o', label=f'#{hashtag}')

plt.xlabel('Date')
plt.ylabel('Number of Posts')
plt.title('Number of Instagram Posts with Specific Hashtags Over the Last 5 Days')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

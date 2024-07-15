from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import datetime
import json

# Specify the correct path to your WebDriver
chrome_driver_path = r'E:\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Adjust path to your ChromeDriver executable
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Navigate to login page
    driver.get("https://x.com/i/flow/login")
    sleep(3)

    # Login process
    username_input = "YOUR_USERNAME"
    email_or_phone = "YOUR_REGISTERED_MAIL"
    password_input = "YOUR_PASSWORD"

    username = driver.find_element(By.XPATH, "//input[@name='text']")
    username.send_keys(username_input)
    next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
    next_button.click()

    # Check if email/phone step is required
    sleep(3)
    try:
        email_phone = driver.find_element(By.XPATH, "//input[@name='text']")
        email_phone.send_keys(email_or_phone)
        next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        next_button.click()
        sleep(3)
    except:
        pass  # If the email/phone step is not required, proceed

    password = driver.find_element(By.XPATH, "//input[@name='password']")
    password.send_keys(password_input)
    log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
    log_in.click()

    # Search for the subject and fetch it
    search_query = "until:2024-07-12 since:2024-07-08 #sneakers"
    sleep(10)
    search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)

    sleep(3)
    media_tab = driver.find_element(By.XPATH, "//span[contains(text(),'Media')]")
    media_tab.click()

    sleep(15)

    # Dictionary to store dates and post counts
    date_post_count = {}

    # Click on the first tweet under the Media tab
    first_tweet = driver.find_element(By.XPATH, "//*[@id='verticalGridItem-0-search-grid-0']")
    first_tweet.click()

    sleep(5)  # Adjust as needed to allow time for the tweet to open

    # Extract date and time of the first tweet
    first_tweet_time = driver.find_element(By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time").get_attribute('datetime')
    first_tweet_date = datetime.fromisoformat(first_tweet_time[:-1]).strftime('%Y-%m-%d')

    # Initialize count for the first date
    date_post_count[first_tweet_date] = 1

    sleep(2)
    close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
    close_button.click()
    sleep(3)

    # Open next 6 tweets and extract date and time
    for i in range(1, 28):
        try:
            next_tweet_xpath = f"//*[@id='verticalGridItem-{i}-search-grid-{0}']"
            next_tweet = driver.find_element(By.XPATH, next_tweet_xpath)
            next_tweet.click()
            sleep(5)  # Adjust as needed to allow time for the tweet to open

            next_tweet_time = driver.find_element(By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time").get_attribute('datetime')
            next_tweet_date = datetime.fromisoformat(next_tweet_time[:-1]).strftime('%Y-%m-%d')

            # Increment count for the date or initialize if not present
            if next_tweet_date in date_post_count:
                date_post_count[next_tweet_date] += 1
            else:
                date_post_count[next_tweet_date] = 1

            sleep(2)
            close_button = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
            close_button.click()
            sleep(3)
        except Exception as e:
            print(f"Error occurred while fetching {i+1}nd tweet:", str(e))

    # Save data to a JSON file
    with open('post_counts.json', 'w') as json_file:
        json.dump(date_post_count, json_file, indent=4)

finally:
    # Close the driver
    driver.quit()

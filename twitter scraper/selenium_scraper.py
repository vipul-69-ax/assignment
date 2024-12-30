from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymongo
import uuid
import datetime
import os

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_trends"]
collection = db["trending_topics"]

# ProxyMesh setup (Replace with your proxy)
proxy = "vipull.69:Vipu2004@@us-ca.proxymesh.com:31280"  # Replace with your credentials

# Selenium setup
options = Options()
options.add_argument("--start-maximized")
options.add_argument(f"--proxy-server=http://{proxy}")  # Add proxy with authentication

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

def scrape_twitter_trends(username, password):
    try:
        # Step 1: Open Twitter and log in
        driver.get("https://x.com/i/flow/login")

        # Wait for username field and enter username
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        ).send_keys(username + Keys.RETURN)
        time.sleep(3)

        # Wait for password field and enter password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password + Keys.RETURN)
        time.sleep(5)

        # Step 2: Scrape trending topics
        trends_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//section[@aria-labelledby]"))
        )
        trends = trends_section.find_elements(By.XPATH, ".//span[contains(@dir, 'ltr')]")
        top_5_trends = [trend.text for trend in trends[:5]]

        # Step 3: Save data to MongoDB
        unique_id = str(uuid.uuid4())
        end_time = datetime.datetime.now()
        ip_address = proxy.split(":")[0]

        record = {
            "_id": unique_id,
            "trend1": top_5_trends[0] if len(top_5_trends) > 0 else "",
            "trend2": top_5_trends[1] if len(top_5_trends) > 1 else "",
            "trend3": top_5_trends[2] if len(top_5_trends) > 2 else "",
            "trend4": top_5_trends[3] if len(top_5_trends) > 3 else "",
            "trend5": top_5_trends[4] if len(top_5_trends) > 4 else "",
            "date_time": end_time,
            "ip_address": ip_address
        }
        collection.insert_one(record)

        return record

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    # Avoid hardcoding sensitive information
    username = os.getenv("TWITTER_USERNAME", "your_email@example.com")
    password = os.getenv("TWITTER_PASSWORD", "your_password")
    result = scrape_twitter_trends(username, password)
    if result:
        print("Scraped Data:", result)
    else:
        print("Failed to scrape data.")

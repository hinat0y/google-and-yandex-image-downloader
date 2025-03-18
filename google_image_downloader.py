import time
import os
import requests
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_setup import init_webdriver  # Import WebDriver setup

def search_google_images(driver, query, num_images=5):
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?tbm=isch&tbs=qdr:w,isz:l&q={encoded_query}"
    driver.get(search_url)
    time.sleep(3)

    image_urls = set()

    image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.YQ4gaf')

    for img in image_elements:
        try:
            img.click()
            time.sleep(2)

            big_img = driver.find_element(By.CSS_SELECTOR, 'img.sFlh5c.FyHeAf.iPVvYb')
            img_url = big_img.get_attribute('src')

            if img_url and "http" in img_url:
                image_urls.add(img_url)
                print(f"URL: {img_url}")

            if len(image_urls) >= num_images:
                break

            ActionChains(driver).send_keys('\ue00c').perform()
            time.sleep(1)

        except Exception as e:
            print(f"Error retrieving image: {e}")

    return list(image_urls)[:num_images]

def download_images(image_urls, folder="images"):
    os.makedirs(folder, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    success_count = 0

    for i, url in enumerate(image_urls):
        image_path = f"{folder}/image_{i+1}.jpg"

        try:
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            if response.status_code == 200:
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {image_path}")
                success_count += 1
            else:
                print(f"Failed to download image (Status Code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")
    return success_count
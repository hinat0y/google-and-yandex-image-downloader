import time
import os
import requests
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_setup import init_webdriver  # Import WebDriver setup

def search_yandex_images(driver, query, num_images=5):
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://yandex.com/images/search?isize=large&recent=7D&text={encoded_query}"
    driver.get(search_url)
    time.sleep(3)

    image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.ImagesContentImage-Image_clickable')[:num_images]
    image_urls = []

    for index, image in enumerate(image_elements):
        try:
            driver.execute_script("arguments[0].click();", image)
            time.sleep(2)

            try:
                open_button = driver.find_element(By.CSS_SELECTOR, 'a.MMViewerButtons-OpenButton')
                img_url = open_button.get_attribute('href')
            except:
                img_element = driver.find_element(By.CSS_SELECTOR, 'img.MMImage-Origin')
                img_url = img_element.get_attribute('src')

            if img_url:
                image_urls.append(img_url)
                print(f"Image {index+1} URL: {img_url}")

            ActionChains(driver).send_keys('\ue00c').perform()
            time.sleep(1)

            if len(image_urls) >= num_images:
                break

        except Exception as e:
            print(f"Error retrieving image {index+1}: {e}")

    return image_urls[:num_images]

def download_images(image_urls, folder="images"):
    os.makedirs(folder, exist_ok=True)

    headers = {"User-Agent": "Mozilla/5.0"}
    success_count = 0
    for i, url in enumerate(image_urls):
        image_path = f"{folder}/image_{i+1}.jpg"

        try:
            response = requests.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {image_path}")
                success_count += 1
            else:
                print(f"Failed to download image {i+1}")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")

    return success_count

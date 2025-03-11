from google_image_downloader import search_google_images, download_images
from yandex_image_downloader import search_yandex_images
from webdriver_setup import init_webdriver

def main():
    driver = init_webdriver()
    search_query = "sunset"  # Change this to any search term

    source = input("Search images from Google or Yandex? (g/y): ").strip().lower()

    if source == "g":
        image_links = search_google_images(driver, search_query)
    else:
        image_links = search_yandex_images(driver, search_query)

    if image_links:
        download_images(image_links)

    driver.quit()

if __name__ == "__main__":
    main()


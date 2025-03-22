import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--disable-dev-shm-usage")  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://in.pinterest.com/ideas/apple-images/925763766497/"
driver.get(url)
time.sleep(5) 

soup = BeautifulSoup(driver.page_source, "html.parser")

img_tags = soup.find_all("img")

os.makedirs("images", exist_ok=True)

downloaded = 0
for img in img_tags:
    img_url = img.get("data-src") or img.get("src")  

    if img_url and img_url.startswith("http"):
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                img_name = img_url.split("/")[-1].split("?")[0]
                img_path = os.path.join("images", img_name)

                with open(img_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

                print(f"Downloaded: {img_path}")
                downloaded += 1
        except Exception as e:
            print(f" Error downloading {img_url}: {e}")

driver.quit()

if downloaded == 0:
    print("No images downloaded. Check if the website structure has changed.")
else:
    print(f"Successfully downloaded {downloaded} images.")

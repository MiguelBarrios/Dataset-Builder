import os, os.path
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

# get all img links in page
def get_links(soup, images):
    image_containers = soup.find_all('img')
    for container in image_containers:
        url = container['src']
        if is_image(url) and url not in images:
            images.add(url)

def is_image(url):
    extention = url[-3:]
    return extention == 'jpg' or extention == 'png'

def save_images(img_urls, output_directory):
    print("Saving Images")
    # create directory if DNE
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    num_files = len(os.listdir(output_directory)) + 1
    images_saved = 0
    for img_url in tqdm(img_urls):
        file_name = "{}/{}.png".format(output_directory, num_files)
        if download_image(img_url, file_name, output_directory):
            num_files = num_files + 1
            images_saved = images_saved + 1
    return images_saved

def download_image(image_url, file_name, output_directory):
    try:
        response = requests.get(image_url)
        file = open(file_name, "wb")
        file.write(response.content)
        file.close()
        return True
    except Exception as e:
        print("invalid link: {}".format(image_url))
        return False
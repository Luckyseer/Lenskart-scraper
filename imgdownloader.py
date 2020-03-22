from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import os
from tqdm import tqdm

firefox = webdriver.Firefox()
num = 1
with open('links.txt', 'r') as f:
    links = f.readlines()
    num_links = len(links)
    print("No. of links: %d" % num_links)


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(file_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


for i in range(0, num_links):
    firefox.get(links[i])

    images = firefox.find_elements_by_tag_name('img')
    new_images = []
    imglen = 0
    for image in images:

        if 'thumbnail' in image.get_attribute('src') and imglen <= 6:
            hover = ActionChains(firefox).move_to_element(image)
            hover.perform()
            time.sleep(2.5)
            img2 = firefox.find_elements_by_tag_name('img')
            for image2 in img2:
                try:
                    if image2 not in images and 'bat.bing' not in image2.get_attribute('src'):
                            download(image2.get_attribute('src'), 'images')
                            imglen += 1
                except:
                        print('Exception at: %d'%num)
        if imglen > 6:  # downloads only 6 images
            pass
    print('Completed (%d/%d)' % (num, num_links))
    num += 1
firefox.close()

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import os
import csv
from tqdm import tqdm

pause = False  # Set to false to create csv file

firefox = webdriver.Firefox()
num = 1
with open('links2.txt', 'r') as f:
    links = f.readlines()
    num_links = len(links)
    print("No. of links: %d" % num_links)

image_list = []


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


for i in range(num - 1, num_links):
    firefox.get(links[i])
    images = firefox.find_elements_by_tag_name('img')
    imglen = 0
    image_dict = {'num': i}  # dictionary to keep track of filenames in order of download
    for image in images:

        if 'thumbnail' in image.get_attribute('src') and imglen <= 6:
            hover = ActionChains(firefox).move_to_element(image)
            hover.perform()
            time.sleep(2.5)
            img2 = firefox.find_elements_by_tag_name('img')
            for image2 in img2:
                try:
                    if imglen > 4:  # downloads only 5 images
                        pass
                    elif image2 not in images and 'bat.bing' not in image2.get_attribute('src'):
                            download(image2.get_attribute('src'), 'sunglass_images')
                            image_dict['img%d' % imglen] = image2.get_attribute('src').split("/")[-1]
                            imglen += 1
                except:
                        print('Exception at: %d' % num)
    image_list.append(image_dict)
    print('Completed (%d/%d)' % (num, num_links))
    num += 1
firefox.close()
filename = 'sunglass_image.csv'
if not pause:
    num2 = 1
    with open(filename, 'w', newline='') as f:
        w = csv.DictWriter(f, ['num', 'img0', 'img1', 'img2', 'img3', 'img4'])
        w.writeheader()
        for image_name in image_list:
            w.writerow(image_name)
            print('Entered (%d/%d) Entries' % (num2, num_links))
            num2 += 1

#   scrapes info of eyeglasses on lenskart
import requests
from bs4 import BeautifulSoup
import csv
with open('links.txt', 'r') as f:
    links = f.readlines()
    num_links = len(links)
    print("No. of links: %d" % num_links)
infos = []
num = 1  # Num of elements processed
pause = False  # Set to false to create CSV file
for URL in links:
    shape = ''
    price = ''
    deal_price = ''
    f_width = ''
    f_height = ''
    gender = ''
    model = ''
    info = {}
    r = requests.get(URL.rstrip('\n'))
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('div', attrs={'id': 'uncontrolled-tab-example'})
    table2 = soup.find('div', attrs={'id': 'content'})
    for row in table2.findAll('div', attrs={'class': 'text-right'}):
        if 'Price:' in row.text and 'Lenses' not in row.text:
            break
    price = row.text[8:]
    for row in table2.findAll('div', attrs={'class': 'price fs20 text-link nowrap'}):
            deal_price = row.text
    deal_price = deal_price.lstrip('₹')
    deal_price = deal_price.rstrip(' with Lenses ')
    for row in table.findAll('div', attrs={'class': 'product-name'}):
        info['name'] = row.text
    i = 0
    colour = ""
    for row in table.findAll('div', attrs={'class': 'tech-information'}):
        if 'Brand Name' in row.text:
            info['brand'] = row.text[10:]
        elif 'Product Type' in row.text:
            info['att_set'] = row.text[12:]
        elif 'Frame Type' in row.text:
            info['style'] = row.text[10:]
        elif 'Frame Shape' in row.text:
            shape = row.text[11:]
            if shape == 'quare':
                shape = 'Square'
            info['shape'] = shape
        elif 'Model No.' in row.text:
            model = row.text.lstrip('generalModel No.')
        elif 'Frame Width' in row.text:
            f_width = row.text[11:].rstrip(' mm')
            info['frame_width'] = f_width
        elif 'Height' in row.text:
            f_height = row.text[6:].rstrip(' mm')
            info['frame_height'] = f_height
        elif 'Gender' in row.text:
            gender = row.text[6:]
            info['gender'] = gender
        elif 'Temple Colour' in row.text:
            colour = row.text[13:]
            info['frame_colour'] = colour
        elif 'Frame colour' in row.text:
            colour = row.text[12:]
            info['frame_colour'] = colour
    sku = model + colour
    info['sku'] = sku
    string = ""
    for row in table.findAll('div', attrs={'class': 'content'}):
        string += row.text
    string = string.encode('UTF-8')

    info['description'] = string
    if info:
        infos.append(info)
    info['num'] = num
    info['price'] = price
    info['deal_price'] = deal_price
    print('Completed (%d/%d)' % (num, num_links))
    num += 1
filename = 'lens_info.csv'
if not pause:
    num2 = 1
    with open(filename, 'w', newline='') as f:
        w = csv.DictWriter(f, ['num', 'sku', 'name', 'brand', 'att_set', 'price', 'deal_price', 'style', 'gender', 'shape', 'description', 'frame_height', 'frame_width', 'frame_colour'])
        w.writeheader()
        for information in infos:
            w.writerow(information)
            print('Entered (%d/%d) Entries' % (num2, num_links))
            num2 += 1


import requests
from bs4 import BeautifulSoup


def get_ad_data(item):
    response = requests.get(item[2])
    soup = BeautifulSoup(response.content, 'html.parser')
    description = soup.select('#homepage > div.container.body-container > div.content-wrapper > div.main-content > div.details-main > div.right > div.description > p')
    description_text = [p.get_text(strip=True) for p in description]
    info_rows = soup.find_all('div', class_='info-row')
    info_data = {row.find('div', class_='label').get_text(strip=True): row.find('div', class_='info').get_text(strip=True) for row in info_rows}
    images = soup.find_all('div', class_='fotorama__thumb fotorama__loaded fotorama__loaded--img')
    image_urls = [image.find('img')['src'] for image in images]

    return item[0], item[1], description_text, info_data, image_urls

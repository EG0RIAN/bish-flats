import requests
from bs4 import BeautifulSoup
from config import BASE_LINK, ROOM_ARGS


def get_pages(pg_num=3,
              rooms="",
              floor_from="",
              floor_to="",
              price_from="",
              price_to=""):
    url = BASE_LINK
    if rooms != "":
        url += f"&rooms={ROOM_ARGS.get(rooms)}"
    if floor_from != "":
        url += f"&floor_from={floor_from}"
    if floor_to != "":
        url += f"&floor_to={floor_to}"
    if price_from != "":
        url += f"price_from={price_from}"
    if price_to != "":
        f"&price_to={price_to}"
    url += "&currency=1" + "&is_owner=1&sort_by=upped_at+desc"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find_all('div', {'itemscope': '', 'itemtype': 'https://schema.org/Apartment', 'class': 'listing'})
    ads = []
    for page in divs[:pg_num]:
        name_tag = page.find('p', class_='title').find('a')
        name = name_tag.text.strip() if name_tag else 'No title'
        price_tag = page.find('div', class_='price-addition')
        som_price = price_tag.text.strip() if price_tag else 'No price'
        link_tag = page.find('a', href=True)
        link = "https://www.house.kg/" + link_tag['href'] if link_tag else 'No link'
        ads.append((name, som_price, link))
    return ads

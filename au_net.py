import requests
from bs4 import BeautifulSoup

def load_au_page(page:int=1):

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    all_cards = []

    response = requests.get(f'https://1.au.ru/?sort=date&landmark=2&page={page}', headers=headers)
    send = BeautifulSoup(response.text, "lxml")
    data = send.find_all("div", class_="au-card-list-item")

    for i in data:
        card_dict = {}
        # НАЗВАНИЕ ЛОТА
        try:
            card_dict["name"] = i.find("div", class_="au-lot-list-card-title").text
        except Exception as msg:
            print("[NAME]", msg)
            continue
        # ССЫЛКА НА ЛОТ
        try:
            link = i.find("div", class_="au-lot-list-card-title").find("a", class_="au-lot-list-card-title-link").get("href")
            card_dict["link"] = "https:" + link
        except Exception as msg:
            print("[LINK]", msg)
            continue
        # ВРЕМЯ ДО ОКОНЧАНИЯ ТОРГОВ
        try:
            card_dict["time"] = i.find("span", class_="au-date-marker__item").text
        except:
            try:
                card_dict["time"] = i.find("div", class_="au-date-marker__item").text
            except Exception as msg:
                print("[TIME]", msg)
                continue
        # ЦЕНА
        try:
            coast = i.find("span", class_="au-price__value").text
            coast = coast.replace("\xa0", " ")
            currency = i.find("span", class_="au-price__currency").text
            card_dict["price"] = coast + " " + currency
        except Exception as msg:
            print("[PRICE]", msg)
            continue
        # БЛИЦ-ЦЕНА
        try:
            bl_price = i.find("a", class_="au-lot-list-card-price__blitz")
            coast = bl_price.find("span", class_="au-price__value").text
            coast = coast.replace("\xa0", " ")
            currency = bl_price.find("span", class_="au-price__currency").text
            card_dict["blits"] = coast + " " + currency
        except:
            card_dict["blits"] = "None"
        # МЕСТО НАХОЖДЕНИЯ ЛОТА
        try:
            card_dict["place"] = i.find("span", class_ ="au-geo-mark__name").text
        except Exception as msg:
            print("[PLACE]", msg)
            continue
        # КАТЕГОРИЯ
        try:
            card_dict["category"] = i.find("div", class_="au-lot-list-card__breadcrumbs").text
        except Exception as msg:
            print("[CATEGORY]", msg)
            continue
        # ФОТОГРАФИИ
        try:
            links_photos_soup = i.find_all("img", class_="au-image-preview__image--preload")
            links_photos = []
            for img_soup in links_photos_soup:
                links_photos.append("https:" + img_soup.get("src"))
            card_dict["photos"] = links_photos
        except Exception as msg:
            print("[PHOTOS]", msg)

        all_cards.append(card_dict)

    return all_cards

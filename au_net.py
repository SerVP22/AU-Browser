import os.path

import requests
from bs4 import BeautifulSoup

class AUNet():

    def load_au_page(self, page:int=1):

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
            # КОЛИЧЕСТВО КОММЕНТАРИЕВ
            try:
                card_dict["comment_count"] = i.find("span", class_="au-actions-count__value").text
            except Exception as msg:
                print("[COMMENT_COUNT]", msg)

            # ПОЛУЧАЕМ СЛОВАРЬ С ДАННЫМИ
            try:
                data_div = i.find("div", class_="au-lot-list-card")
                data_dict_str = data_div.get("data-lamber-object")
                # card_dict["data_dict"] = data_dict
            except Exception as msg:
                print("[DATA_DICT]", msg)
                continue

            data_dict_str = data_dict_str.replace("false", "False") # замена в полученной строке false на False
            data_dict = eval(data_dict_str) # преобразуем строку в словарь

            # ID КАТЕГОРИИ
            card_dict["cat_id"] = data_dict["itemCategoryId"]

            # ID лота
            card_dict["lot_id"] = data_dict["item"]

            # НОМЕР КАРТОЧКИ НА СТРАНИЦЕ
            card_dict["position"] = data_dict["position"]

            all_cards.append(card_dict)

        return all_cards

    def load_photo(self, lot_id, name, path, url):

        def save_photo():
            dir_path = os.path.join(path, lot_id)
            full_path = os.path.join(dir_path, name)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            with open(f"{full_path}", "wb+") as f:
                f.write(response.content)
            return full_path

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

        response = requests.get(url, headers=headers)
        if response:
            return save_photo()

if __name__ == "__main__":
    print(AUNet.load_au_page())
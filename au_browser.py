from au_net import AUNet
from au_GUI import AuCard, AuBrowser, os, json
from PIL import Image, ImageTk
from const import *


class AUApp(AuCard, AuBrowser, AUNet):

    def __init__(self):

        # ПОДГРУЖАЕМ ЧЁРНЫЙ ЛИСТ ЛОТОВ
        path_lot_BL = os.path.join(CONFIG_FOLDER, FILE_NAME_BL_LST_LOT)
        if os.path.exists(path_lot_BL):
            with open(path_lot_BL, "r") as f:
                self.app_bl_list_lots = json.load(f)

        # ПОДГРУЖАЕМ ЧЁРНЫЙ ЛИСТ КАТЕГОРИЙ
        path_cat_BL = os.path.join(CONFIG_FOLDER, FILE_NAME_BL_LST_CAT)
        if os.path.exists(path_cat_BL):
            with open(path_cat_BL, "r") as f:
                self.app_bl_list_cats = json.load(f)

        # СОЗДАЁМ ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ
        self.app = AuBrowser(title="AU Browser")  # themename="morph"

        # ПОЛУЧАЕМ ПЕРВУЮ СТРАНИЦУ
        self.page_data = self.load_au_page(self.app.current_page)

        # РАЗМЕЩАЕМ ЛОТЫ НА ОКНЕ ПРИЛОЖЕНИЯ
        for lot in self.page_data:
            # obj_photos_list = load_images(i["photos"])

            # ФИЛЬТР ПО КАТЕГОРИИ
            if str(lot["cat_id"]) in self.app_bl_list_cats:
                print("[CAT EXCEPTION]", f"({lot['position']})", lot["name"])
                continue

            # ФИЛЬТР ПО ЛОТУ
            if str(lot["lot_id"]) in self.app_bl_list_lots:
                print("[LOT EXCEPTION]", f"({lot['position']})", lot["name"])
                continue

            # ПОДГОТОВКА ФОТОГРАФИЙ
            self.list_of_image_obj = []
            for photo in lot["photos"]:
                with Image.open(f"pic1.png") as img:
                    new_img = img.resize((150, 120))
                    rez_img = ImageTk.PhotoImage(new_img)
                self.list_of_image_obj.append(rez_img)
            self.rez_page_data = lot.copy()
            self.rez_page_data.pop("photos")
            self.rez_page_data["photos_obj"] = self.list_of_image_obj

            # РАЗМЕЩЕНИЕ ЛОТА
            AuCard(self.app.bottom_frame, self.rez_page_data)

        self.app.mainloop()


def main():

    AUApp()

if __name__ == "__main__":
    main()
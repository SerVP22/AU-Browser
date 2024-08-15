from au_net import AUNet
from au_GUI import AuCard, AuBrowser, os, json
from PIL import Image, ImageTk
from const import *
from ttkbootstrap.toast import ToastNotification


class AUApp():

    def start_app(self):



        self.app_bl_list_cats = self.app_bl_list_lots = None

        # ПОДГРУЖАЕМ ЧЁРНЫЙ ЛИСТ ЛОТОВ
        self.path_lot_BL = os.path.join(CONFIG_FOLDER, FILE_NAME_BL_LST_LOT)
        if os.path.exists(self.path_lot_BL):
            with open(self.path_lot_BL, "r") as f:
                self.app_bl_list_lots = json.load(f)

        # ПОДГРУЖАЕМ ЧЁРНЫЙ ЛИСТ КАТЕГОРИЙ
        self.path_cat_BL = os.path.join(CONFIG_FOLDER, FILE_NAME_BL_LST_CAT)
        if os.path.exists(self.path_cat_BL):
            with open(self.path_cat_BL, "r") as f:
                self.app_bl_list_cats = json.load(f)

        # СОЗДАЁМ ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ
        if self.first_start:
            self.app = AuBrowser(app=self, title="AU Browser")  # themename="morph"

        # start_toast = ToastNotification(
        #     title="AU Browser",
        #     message="Идёт загрузка данных",
        #     duration=None,
        # )
        # start_toast.show_toast()

        # ПОЛУЧАЕМ ПЕРВУЮ СТРАНИЦУ
        self.page_data = AUNet.load_au_page(page=self.app.current_page)

        message_text = ""

        # РАЗМЕЩАЕМ ЛОТЫ НА ОКНЕ ПРИЛОЖЕНИЯ
        for lot in self.page_data:
            # obj_photos_list = load_images(i["photos"])

            # ФИЛЬТР ПО КАТЕГОРИИ
            if self.app_bl_list_cats and str(lot["cat_id"]) in self.app_bl_list_cats:
                text = "[CAT EXC]" + f" ({lot['position']}) " + lot["name"]
                print(text)
                message_text += text + "\n"
                continue

            # ФИЛЬТР ПО ЛОТУ
            if self.app_bl_list_lots and str(lot["lot_id"]) in self.app_bl_list_lots:
                text = "[LOT EXC]" + f" ({lot['position']}) " + lot["name"]
                print(text)
                message_text += text + "\n"
                continue

            # ПОДГОТОВКА ФОТОГРАФИЙ
            self.list_of_image_obj = []
            for photo in lot["photos"]:
                count = 1
                photo_path = AUNet.load_photo(self,
                                              path=FOLDER_LOT_PHOTOS,
                                              lot_id=str(lot["lot_id"]),
                                              name=str(lot["lot_id"]) + f"_{count}.jpg",
                                              url=photo
                                              )
                count += 1
                if not photo_path:
                    photo_path = os.path.join(CONFIG_FOLDER, NO_PHOTO_PIC)
                with Image.open(photo_path) as img:
                    new_width = int(150*img.width/img.height)
                    if new_width>150:
                        new_width = 150
                    new_img = img.resize((new_width, 120))
                    rez_img = ImageTk.PhotoImage(new_img)

                self.list_of_image_obj.append(rez_img)
            self.rez_page_data = lot.copy()
            self.rez_page_data.pop("photos")
            self.rez_page_data["photos_obj"] = self.list_of_image_obj

            # РАЗМЕЩЕНИЕ ЛОТА
            AuCard(self.app.bottom_frame, #РОДИТЕЛЬСКИЙ ФРЭЙМ
                   self.rez_page_data,    #ДАННЫЕ ЛОТА
                   self.path_cat_BL,
                   self.path_lot_BL)

        # start_toast.hide_toast()

        if len(message_text) > 0:
            toast = ToastNotification(
                title="AU Browser. Некоторые лоты не отобразились",
                message=message_text,
                duration=10000,
            )
            toast.show_toast()

    def __init__(self):

        self.first_start = True
        self.start_app()
        self.first_start = False
        self.app.mainloop()


def main():

    AUApp()

if __name__ == "__main__":
    main()
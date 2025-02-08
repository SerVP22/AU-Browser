from au_net import AUNet
from au_GUI import AuCard, AuBrowser, os, json, ttk_bs
from PIL import Image, ImageTk
from const import *
from ttkbootstrap.toast import ToastNotification


class AUApp():

    def load_and_return_config(self):
        self.full_path_conf = os.path.join(CONFIG_FOLDER, FILE_CNF)

        if os.path.exists(self.full_path_conf):
            with open(self.full_path_conf, "r") as f:
                data = json.load(f)
            try:
                return data[SHOW_EXCLUDED_LOTS_KEY], data[EXCLUDE_LOTS_KEY], data[RELOAD_PHOTOS_KEY]
            except Exception as msg:
                print('[EXC ERROR]:', msg)
                return False, False, False  # self.show_excluded_lots, self.exclude_lots
        else:
            print("[Ошибка доступа к файлу конфигурации]")
            return False, False, False #self.show_excluded_lots, self.exclude_lots

    def start_app(self):

        self.show_excluded_lots, self.exclude_lots, self.reload_photos = self.load_and_return_config()
        AUNet._param_set(bool(self.reload_photos))

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
            self.app = AuBrowser(app=self,
                                 title="AU Browser",
                                 sh=self.show_excluded_lots,
                                 ex=self.exclude_lots,
                                 rl=self.reload_photos)  # themename="morph"

        self.app.title("AU Browser [ЗАГРУЗКА...]")

        # ПОЛУЧАЕМ ПЕРВУЮ СТРАНИЦУ
        self.page_data = AUNet.load_au_page(page=self.app.current_page)

        message_text = ""

        # РАЗМЕЩАЕМ ЛОТЫ НА ОКНЕ ПРИЛОЖЕНИЯ
        for lot in self.page_data:
            # obj_photos_list = load_images(i["photos"])

            # ФИЛЬТР ЗАВЕРШЁННЫХ ЛОТОВ
            if lot["time"] == "Торги завершены":
                text = "[END TIME]" + f" ({lot['position']}) " + lot["name"]
                message_text += text + "\n"
                continue

            # ФИЛЬТР ПО КАТЕГОРИИ
            if self.app_bl_list_cats and str(lot["cat_id"]) in self.app_bl_list_cats:
                text = "[CAT EXC]" + f" ({lot['position']}) " + lot["name"]
                # print(text)
                message_text += text + "\n"
                if self.exclude_lots:
                    continue
            # ФИЛЬТР ПО ЛОТУ
            if self.app_bl_list_lots and str(lot["lot_id"]) in self.app_bl_list_lots:
                text = "[LOT EXC]" + f" ({lot['position']}) " + lot["name"]
                # print(text)
                message_text += text + "\n"
                if self.exclude_lots:
                    continue

            # ПОДГОТОВКА ФОТОГРАФИЙ
            self.list_of_image_obj = []
            count = 1

            for photo in lot["photos"]:
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
                    # new_width = int(150*img.width/img.height)
                    # if new_width>150:
                    #     new_width = 150
                    if img.width >= img.height:
                        new_width = 150
                        new_height = int(150 * img.height / img.width)
                        if (new_width / new_height) > 2:
                            new_height = 75
                    else:
                        new_width = int(120 * img.width / img.height)
                        new_height = 120
                        if (new_height / new_width) > 2:
                            new_width = 60
                    new_img = img.resize((new_width, new_height))
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

        # НИЖНЯЯ КНОПКА "СЛЕДУЮЩАЯ СТРАНИЦА"
        self.end_frame = ttk_bs.LabelFrame(self.app.bottom_frame, text="Конец списка", bootstyle="primary")
        self.end_frame.pack(fill="x", pady=5, padx=20)
        self.next_page_btn = ttk_bs.Button(master=self.end_frame,
                                     text=" > > > Следующая страница > > >",
                                     command=self.app.forward_btn_press,
                                     bootstyle="success-outline")
        self.next_page_btn.pack(expand=True, fill="both", pady=10, padx=10)

        # start_toast.hide_toast()

        self.app.title("AU Browser")

        if len(message_text) > 0 and self.show_excluded_lots and self.exclude_lots: # ОТОБРАЖЕНИЕ ИСКЛЮЧЕНИЙ:
            toast = ToastNotification(
                title="AU Browser. Некоторые лоты не отобразились",
                message=message_text,
                duration=10000,
            )
            toast.show_toast()

        # self.app.bottom_frame.vscroll.focus_force()
        self.next_page_btn.focus_force()

    def __init__(self):

        self.first_start = True
        self.start_app()
        self.first_start = False
        self.app.mainloop()


def main():

    AUApp()

if __name__ == "__main__":
    main()
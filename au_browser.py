from au_net import load_au_page
import ttkbootstrap as ttk_bs # Современная надстройка над ttk и tkinter
# from tkinter import messagebox as mes_box
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter.ttk as ttk
from tkinter import IntVar, BooleanVar
# import tkinter as tk
from PIL import Image, ImageTk
from ttkbootstrap.tooltip import ToolTip

class AuCard:
    def __init__(self, parent_frame, page_data):

        global rez_img

        self.lot_name = page_data["name"]
        self.lot_link = page_data["link"]
        self.lot_time = page_data["time"]
        self.lot_photos = page_data["photos_obj"]
        self.lot_price = page_data["price"]
        self.lot_place = page_data["place"]
        self.lot_category = page_data["category"]
        if page_data["blits"] != "None":
            self.lot_blits = page_data["blits"]
        else:
            self.lot_blits = "-"

        self.cat_bl_list_flag = BooleanVar(value=False)
        self.lot_bl_list_flag = IntVar(value=0)

        # ПАНЕЛЬ С РАМКОЙ ДЛЯ ЛОТА
        self.card_frame = ttk_bs.LabelFrame(parent_frame, text=f"№{id(self)}", bootstyle="primary")

        # НАЗВАНИЕ ЛОТА
        self.card_title = ttk_bs.Label(self.card_frame,
                                       cursor="hand2",
                                       text=self.lot_name,
                                       width=35,
                                       background="white",
                                       font=('Arial', '18', 'bold'),)
        self.card_title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=25)
        ToolTip(self.card_title, self.lot_name, bootstyle="info-inverse")


        # ГАЛКА "ДОБАВИТЬ В ИСКЛЮЧЕНИЯ (КАРТОЧКА)"
        self.exception_check_box = ttk_bs.Checkbutton(self.card_frame,
                                             text='Добавить лот в "Чёрный лист"',
                                             variable=self.lot_bl_list_flag,
                                             # compound="left",
                                             width=40,
                                             offvalue=0,
                                             onvalue=1,
                                             padding=5,
                                             bootstyle="danger-round-toggle",
                                             # style="TCheckbutton-mini",

                                             )
        self.exception_check_box.grid(row=0, column=3, columnspan=1, padx=25, pady=5, sticky="e")
        # self.exception_check_box.invoke()
        # self.exception_check_box.invoke()


        ### ПАНЕЛЬ ИЗОБРАЖЕНИЯ И КНОПОК

        # FRAME
        self.image_area_frame = ttk_bs.Frame(self.card_frame)
        self.image_area_frame.grid(row=1, column=0, columnspan=1, rowspan=3, padx=15, pady=5, sticky="ew")

        # КНОПКА НАЗАД
        self.arrow_back_button = ttk_bs.Button(self.image_area_frame, text="<", bootstyle="dark-outline", )
        self.arrow_back_button.grid(row=1, column=0, columnspan=1, rowspan=3, sticky="ns")

        # РАЗМЕЩЕНИЕ ФОТОГРАФИИ
        # img = Image.open("pic.png")
        # new_img = img.resize((150, 120))
        # rez_img = ImageTk.PhotoImage(new_img)
        # img.close()

        # with Image.open(self.lot_photos[0]) as img:
        #     new_img = img.resize((150, 120))
        #     rez_img = ImageTk.PhotoImage(new_img)

        # print(img)

        self.image_label = ttk_bs.Label(self.image_area_frame,
                                        background="black",
                                        image=self.lot_photos[0],
                                        borderwidth=1
                                        )
        self.image_label.grid(row=1, column=1, columnspan=10, rowspan=3)

        # КНОПКА ВПЕРЁД
        self.arrow_forward_button = ttk_bs.Button(self.image_area_frame, text=">", bootstyle="dark-outline")
        self.arrow_forward_button.grid(row=1, column=11, columnspan=1, rowspan=3, sticky="ns")
        ###

        ### ПАНЕЛЬ ОПИСАНИЯ
        self.description_frame = ttk_bs.Frame(self.card_frame)
        self.description_frame.grid(row=1, column=1, columnspan=2, rowspan=3, padx=15, pady=5, sticky="ew")

        # ЦЕНА
        self.price_frame = ttk_bs.LabelFrame(self.description_frame, text=" Текущая цена ")
        self.price_frame.grid(row=0, column=0, columnspan=1, sticky="w")
        self.card_price = ttk_bs.Label(self.price_frame,
                                       text=self.lot_price,
                                       width=10,
                                       anchor="center",
                                       bootstyle="success",
                                       font=('Arial', '14', 'bold')
                                       )
        self.card_price.pack(anchor="center")

        # БЛИЦ-ЦЕНА
        self.blits_frame = ttk_bs.LabelFrame(self.description_frame, text=" Блиц-цена ")
        self.blits_frame.grid(row=0, column=1, columnspan=1, sticky="w")
        self.card_blits = ttk_bs.Label(self.blits_frame,
                                       text=self.lot_blits,
                                       width=10,
                                       anchor="center",
                                       bootstyle="warning",
                                       font=('Arial', '14', 'bold')
                                       )
        self.card_blits.pack()

        # МЕСТОРАСПОЛОЖЕНИЕ
        self.place_frame = ttk_bs.LabelFrame(self.description_frame, text=" Расположение ")
        self.place_frame.grid(row=0, column=2, columnspan=1, sticky="n")
        ttk_bs.Label(self.place_frame, text=" ", font=('Arial', '14', 'bold')).pack(side="right")

        self.card_place = ttk_bs.Label(self.place_frame,
                                       text=self.lot_place,
                                       width=30,
                                       anchor="center",
                                       bootstyle="info",

                                       )
        self.card_place.pack(expand=True)


        # КАТЕГОРИЯ
        self.category_frame = ttk_bs.LabelFrame(self.description_frame, text=" Категория ")
        self.category_frame.grid(row=1, column=0, columnspan=10, pady=5, )
        self.card_category = ttk_bs.Label(self.category_frame,
                                       text=self.lot_category,
                                       bootstyle="danger-secondary")
        self.card_category.pack()

        # ВРЕМЯ
        self.time_frame = ttk_bs.LabelFrame(self.description_frame, text=" До конца торгов ")
        self.time_frame.grid(row=2, column=0, columnspan=1, sticky="w")
        self.card_time = ttk_bs.Label(self.time_frame,
                                       text=self.lot_time,
                                       width=10,
                                       anchor="center",
                                       bootstyle="primary",
                                       font=('Arial', '14', 'bold'))
        self.card_time.pack()

        # ДОБАВЛЕНИЕ КАТЕГОРИИ В ЧЁРНЫЙ СПИСОК
        self.category_black_list_frame = ttk_bs.LabelFrame(self.description_frame, text="Чёрный лист")
        self.category_black_list_frame.grid(row=2, column=1, columnspan=2, sticky="e")
        self.cat_exception_check_box = ttk_bs.Checkbutton(self.category_black_list_frame,
                                                          text="Исключить категорию",
                                                          variable=self.cat_bl_list_flag,
                                                          compound="left",
                                                          width=45,
                                                          offvalue=0,
                                                          onvalue=1,
                                                          padding=5,
                                                          bootstyle="danger-square-toggle"
                                                          )
        self.cat_exception_check_box.pack()
        self.cat_exception_check_box.invoke()
        self.cat_exception_check_box.invoke()
        ###



        self.card_frame.pack(fill="x", pady=5, padx=20) # РАЗМЕЩЕНИЕ ПАНЕЛИ ДЛЯ ЛОТА

class AuBrowser(ttk_bs.Window):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.current_page = 1
        self.geometry("1000x800")
        self.main_black_list_flag = IntVar()



        self.style1 = ttk.Style()
        self.style1.configure("TCheckbutton", font=("Arial", 14, "normal"), background="darkgrey")
        # print(self.style1.layout("TCheckbutton"))
        new_style = [('Checkbutton.padding', {'sticky': 'nswe', 'children': [('Checkbutton.indicator', {'side': 'left', 'sticky': ''}), ('Checkbutton.focus', {'side': 'left', 'sticky': 'w', 'children': [('Checkbutton.label', {'sticky': 'nswe'})]})]})]
        self.style1.layout(("TCheckbutton"), new_style)
        # self.style2 = ttk.Style(self)
        # self.style1.configure("TCheckbutton-mini", font=("Arial", 12, "normal"), background="white")


        self.build_top_frame()
        self.build_bottom_frame()


        # toast = ToastNotification(
        #     title="ttkbootstrap toast message",
        #     message="This is a toast message",
        #     duration=10000,
        # )
        # toast.show_toast()

    def build_top_frame(self):
        self.top_frame = ttk_bs.Frame(self, padding=15, bootstyle=DARK)
        self.top_frame.pack(fill=X)

        self.btn_back = ttk_bs.Button(self.top_frame, text="Назад", bootstyle=INFO, width=15)
        self.btn_back.pack(side=LEFT, pady=5, padx=5)

        self.page_label = ttk_bs.Label(self.top_frame,
                                       text=self.current_page,
                                       width=5,
                                       bootstyle=SUCCESS,
                                       anchor=N,
                                       background="white",
                                       font=("Arial", 18, "bold"),
                                       )
        self.page_label.pack(side=LEFT, pady=5, padx=5)

        self.btn_forward = ttk_bs.Button(self.top_frame, text="Вперёд", bootstyle=SUCCESS, width=15)
        self.btn_forward.pack(side=LEFT, pady=5, padx=5)

        self.btn_update = ttk_bs.Button(self.top_frame, text="Обновить страницу", bootstyle=WARNING, width=25)
        self.btn_update.pack(side=LEFT, pady=5, padx=25)

        self.bl_lst_button = ttk.Checkbutton(self.top_frame,
                                             text='Учитывать "Черный лист"',
                                             variable=self.main_black_list_flag,
                                             style="TCheckbutton",
                                             offvalue=0,
                                             onvalue=1,
                                             padding=5
                                             )

        self.bl_lst_button.pack(side="left", expand=1, anchor=E)
        self.bl_lst_button.invoke()

    def build_bottom_frame(self):
        self.bottom_frame = ScrolledFrame(self)
        self.bottom_frame.pack(expand=True, fill=ttk_bs.BOTH)
        #

def get_page_data(page_num:int):

    # all_cards = load_au_page(page=page_num)
    #
    # for i in all_cards:
    #     print(i)
    #
    # print(len(all_cards))
    return load_au_page(page=page_num)

def main():

    # def load_images(links:list) -> list:
    #     global list_of_image_obj
    #     list_of_image_obj = []
    #     for i in links:
    #         with Image.open(f"pic1.png") as img:
    #             new_img = img.resize((150, 120))
    #             rez_img = ImageTk.PhotoImage(new_img)
    #         list_of_image_obj.append(rez_img)
    #     return list_of_image_obj


    app = AuBrowser(title="AU Browser")  # themename="morph"
    # add_card_widgets(app)
    # pictures = []
    # for i in range(1, 7):
    #     with Image.open(f"pic{i}.png") as img:
    #         new_img = img.resize((150, 120))
    #         rez_img = ImageTk.PhotoImage(new_img)
    #     pictures.append(rez_img)
    # card1 = AuCard(app.bottom_frame, pictures[0])
    # card2 = AuCard(app.bottom_frame, pictures[1])
    # card3 = AuCard(app.bottom_frame, pictures[2])
    # card4 = AuCard(app.bottom_frame, pictures[3])
    # card5 = AuCard(app.bottom_frame, pictures[4])
    # card6 = AuCard(app.bottom_frame, pictures[5])

    page_data = get_page_data(app.current_page)

    for lot in page_data:
        # obj_photos_list = load_images(i["photos"])

        list_of_image_obj = []
        for photo in lot["photos"]:
            with Image.open(f"pic1.png") as img:
                new_img = img.resize((150, 120))
                rez_img = ImageTk.PhotoImage(new_img)
            list_of_image_obj.append(rez_img)

        rez_page_data = lot.copy()
        rez_page_data.pop("photos")
        rez_page_data["photos_obj"] = list_of_image_obj
        AuCard(app.bottom_frame, rez_page_data)


    app.mainloop()


if __name__ == "__main__":
    main()
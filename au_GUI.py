import json
from tkinter import IntVar, BooleanVar
import tkinter.ttk as ttk
import ttkbootstrap as ttk_bs # Современная надстройка над ttk и tkinter
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import os
from const import *

class AuCard():

    def __init__(self, parent_frame, page_data, path_cat_BL, path_lot_BL):

        self.lot_comment_count = page_data["comment_count"]
        self.cat_id = page_data["cat_id"]
        self.lot_id = page_data["lot_id"]
        self.lot_position = page_data["position"]
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
        self.path_cat_BL = path_cat_BL
        self.path_lot_BL = path_lot_BL

        # ПАНЕЛЬ С РАМКОЙ ДЛЯ ЛОТА
        name_text = f" №{self.lot_position} / Лот ID: {self.lot_id} "
        self.card_frame = ttk_bs.LabelFrame(parent_frame, text=name_text, bootstyle="primary")

        # НАЗВАНИЕ ЛОТА
        self.card_title = ttk_bs.Label(self.card_frame,
                                       cursor="hand2",
                                       text=self.lot_name,
                                       width=35,
                                       background="white",
                                       font=('Arial', '18', 'bold'),)
        self.card_title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=25)
        ToolTip(self.card_title, self.lot_name, bootstyle="info-inverse")
        self.card_title.bind("<1>", self.name_click)


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
        self.exception_check_box.grid(row=0, column=2, columnspan=1, padx=25, pady=5, sticky="e")
        self.exception_check_box.bind("<1>", self.exc_lot_click)
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
                                       width=15,
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
                                       width=15,
                                       anchor="center",
                                       bootstyle="warning",
                                       font=('Arial', '14', 'bold')
                                       )
        self.card_blits.pack()

        # МЕСТОРАСПОЛОЖЕНИЕ
        self.place_frame = ttk_bs.LabelFrame(self.description_frame, text=" Расположение ")
        self.place_frame.grid(row=0, column=2, columnspan=1, sticky="n")
        ttk_bs.Label(self.place_frame, text=" ", font=('Arial', '14', 'bold')).pack(side="right") # ЗАГЛУШКА ДЛЯ ВЫРАВНИВАНИЯ ВЫСОТЫ

        self.card_place = ttk_bs.Label(self.place_frame,
                                       text=self.lot_place,
                                       width=30,
                                       anchor="center",
                                       bootstyle="info",

                                       )
        self.card_place.pack(expand=True)
        ToolTip(self.card_place, self.lot_place, bootstyle="info-inverse")


        # КАТЕГОРИЯ
        self.category_frame = ttk_bs.LabelFrame(self.description_frame, text=" Категория ")
        self.category_frame.grid(row=1, column=0, columnspan=10, pady=5, )
        self.card_category = ttk_bs.Label(self.category_frame,
                                          width=89,
                                          text=self.lot_category,
                                          bootstyle="danger-secondary")
        self.card_category.pack()
        ToolTip(self.card_category, self.lot_category, bootstyle="info-inverse")

        # ВРЕМЯ
        self.time_frame = ttk_bs.LabelFrame(self.description_frame, text=" До конца торгов ")
        self.time_frame.grid(row=2, column=0, columnspan=1, sticky="w")
        self.card_time = ttk_bs.Label(self.time_frame,
                                       text=self.lot_time,
                                       width=15,
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
                                                          offvalue=False,
                                                          onvalue=True,
                                                          padding=5,
                                                          bootstyle="danger-square-toggle"
                                                          )
        self.cat_exception_check_box.pack()
        self.cat_exception_check_box.invoke()
        self.cat_exception_check_box.invoke()
        self.cat_exception_check_box.bind("<1>", self.exc_cat_click)
        ###



        self.card_frame.pack(fill="x", pady=5, padx=20) # РАЗМЕЩЕНИЕ ПАНЕЛИ ДЛЯ ЛОТА

    def name_click(self, event):
        os.system('start ' + self.lot_link)

    def add_cat_black_list_to_JSON(self):
        if os.path.exists(self.path_cat_BL):
            with open(self.path_cat_BL, "r") as f:
                data = json.load(f)
            # data.append({str(self.cat_id):self.lot_category})
            data[str(self.cat_id)] = self.lot_category
            with open(self.path_cat_BL, "w") as f:
                json.dump(data, f)
            print("Категория добавлена в чёрный лист")
        else:
            with open(self.path_cat_BL, "w") as f:
                # json.dump([{str(self.cat_id):self.lot_category}], f)
                json.dump({str(self.cat_id): self.lot_category}, f)
            print("Создан чёрный лист категорий")

    def del_cat_from_black_list_JSON(self):
        if os.path.exists(self.path_cat_BL):
            with open(self.path_cat_BL, "r") as f:
                data = json.load(f)
            # index = data.index({str(self.cat_id):self.lot_category})
            # data.pop(index)
            data.pop(str(self.cat_id))
            with open(self.path_cat_BL, "w") as f:
                json.dump(data, f)
            print("Отмена добавления категории в чёрный лист")

    def add_lot_black_list_to_JSON(self):
        if os.path.exists(self.path_lot_BL):
            with open(self.path_lot_BL, "r") as f:
                data = json.load(f)
            # data.append(self.lot_link)
            data[str(self.lot_id)] = self.lot_name
            with open(self.path_lot_BL, "w") as f:
                json.dump(data, f)
            print("Лот добавлен в чёрный лист")
        else:
            with open(self.path_lot_BL, "w") as f:
                # json.dump([self.lot_link], f)
                json.dump({str(self.lot_id): self.lot_name}, f)
            print("Создан чёрный лист лотов")

    def del_lot_from_black_list_JSON(self):
        if os.path.exists(self.path_lot_BL):
            with open(self.path_lot_BL, "r") as f:
                data = json.load(f)
            # data.remove(self.lot_link)
            data.pop(str(self.lot_id))
            with open(self.path_lot_BL, "w") as f:
                json.dump(data, f)
            print("Отмена добавления лота в чёрный лист")

    def exc_lot_click(self, event):
        if self.lot_bl_list_flag.get() == 0:
            self.add_lot_black_list_to_JSON()
            txt = "Lot OFF"
        else:
            self.del_lot_from_black_list_JSON()
            txt = "Lot ON"
        print(txt, self.lot_link)

    def exc_cat_click(self, event):
        if self.cat_bl_list_flag.get():
            self.del_cat_from_black_list_JSON()
            txt = "Cat ON"
        else:
            self.add_cat_black_list_to_JSON()
            txt = "Cat OFF"
        print(txt, self.lot_category)

class AuBrowser(ttk_bs.Window):


    def __init__(self, app, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.current_page = 1
        self.geometry("1000x800")
        self.main_black_list_flag = IntVar()
        self.reload_app = app.start_app
        self.app = app


        self.style1 = ttk.Style()
        self.style1.configure("TCheckbutton", font=("Arial", 14, "normal"), background="darkgrey")
        # print(self.style1.layout("TCheckbutton"))
        new_style = [('Checkbutton.padding', {'sticky': 'nswe', 'children': [('Checkbutton.indicator', {'side': 'left', 'sticky': ''}), ('Checkbutton.focus', {'side': 'left', 'sticky': 'w', 'children': [('Checkbutton.label', {'sticky': 'nswe'})]})]})]
        self.style1.layout(("TCheckbutton"), new_style)
        # self.style2 = ttk.Style(self)
        # self.style1.configure("TCheckbutton-mini", font=("Arial", 12, "normal"), background="white")


        self.build_top_frame()
        self.bottom_frame = self.build_bottom_frame()

    def clear_frame(self):
        for child in self.bottom_frame.winfo_children():
            child.destroy()

    def reload_btn_press(self):
        self.clear_frame()
        self.reload_app()

    def forward_btn_press(self):
        self.current_page += 1
        self.page_label.configure(text=self.current_page)
        self.clear_frame()
        self.reload_app()

    def back_btn_press(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.page_label.configure(text=self.current_page)
            self.clear_frame()
            self.reload_app()

    def build_top_frame(self):

        self.top_frame = ttk_bs.Frame(self, padding=15, bootstyle=DARK)
        self.top_frame.pack(fill=X)

        self.btn_back = ttk_bs.Button(self.top_frame,
                                      text="Назад",
                                      command=self.back_btn_press,
                                      bootstyle=INFO,
                                      width=15)
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

        self.btn_forward = ttk_bs.Button(self.top_frame,
                                         text="Вперёд",
                                         command=self.forward_btn_press,
                                         bootstyle=SUCCESS,
                                         width=15)
        self.btn_forward.pack(side=LEFT, pady=5, padx=5)

        self.btn_update = ttk_bs.Button(self.top_frame,
                                        text="Обновить страницу",
                                        bootstyle=WARNING,
                                        command=self.reload_btn_press,
                                        width=25)
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
        return self.bottom_frame
        #

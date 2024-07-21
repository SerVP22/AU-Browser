from au_net import AUNet
from au_GUI import AuCard, AuBrowser
from PIL import Image, ImageTk


class AUApp(AuCard, AuBrowser, AUNet):

    def __init__(self):
        # def load_images(links:list) -> list:
        #     global list_of_image_obj
        #     list_of_image_obj = []
        #     for i in links:
        #         with Image.open(f"pic1.png") as img:
        #             new_img = img.resize((150, 120))
        #             rez_img = ImageTk.PhotoImage(new_img)
        #         list_of_image_obj.append(rez_img)
        #     return list_of_image_obj

        self.app = AuBrowser(title="AU Browser")  # themename="morph"
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

        self.page_data = self.get_page_data(self.app.current_page)

        for lot in self.page_data:
            # obj_photos_list = load_images(i["photos"])


            self.list_of_image_obj = []
            for photo in lot["photos"]:
                with Image.open(f"pic1.png") as img:
                    new_img = img.resize((150, 120))
                    rez_img = ImageTk.PhotoImage(new_img)
                self.list_of_image_obj.append(rez_img)

            self.rez_page_data = lot.copy()
            self.rez_page_data.pop("photos")
            self.rez_page_data["photos_obj"] = self.list_of_image_obj
            AuCard(self.app.bottom_frame, self.rez_page_data)

        self.app.mainloop()

    def get_page_data(self, page_num: int):

        # all_cards = load_au_page(page=page_num)
        #
        # for i in all_cards:
        #     print(i)
        #
        # print(len(all_cards))
        return self.load_au_page(page=page_num)




def main():

    AUApp()

if __name__ == "__main__":
    main()
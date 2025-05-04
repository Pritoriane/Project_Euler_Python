import customtkinter as CTk
import math



class ToplevelWindow(CTk.CTkToplevel):
    """
    open an additional answer window\n
    :param:
    CTkToplevel - additional window opening
    :return:
    Closed additional window
    """

    def __init__(self, *args, closing_event=None, rezult, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Decision output")
        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.resizable(False, False)
        self.closing_event = closing_event
        self.rezult = rezult
        print(self.rezult)

        self.label = CTk.CTkLabel(
            self,
            text=f"Answer: {self.rezult}.",
            text_color="#DAA520",
            font=CTk.CTkFont(family="Times New Roman", size=20),
            width=400,
        )
        self.label.grid(row=0, column=0, pady=110)

        self.btn_closed = CTk.CTkButton(
            master=self, text="Close..", command=self.closing
        )
        self.btn_closed.grid(row=2, column=0, pady=10)

    def closing(self):
        """
        Function closes the window when the button is clicked.\n
        :param: self
        :return: Not
        """
        self.withdraw()
        self.destroy()
        if self.closing_event is not None:
            self.closing_event()


class App(CTk.CTk):
    def __init__(self, *args, **kwargs):
        """
        The main body of the program is a function.\n
        :param: None
        :return: None
        """
        super().__init__(*args, **kwargs)

        # ----Customizing the appearance and theme of the GUI window---------
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("blue")

        # CTk.FontManager.load_font("Fonts/MV Boli Cyrillic/MVBOLICY.ttf")
        # CTk.FontManager.load_font("Fonts/Goznak/Gosznak-Semi Bold Oblique.otf")
        # CTk.FontManager.load_font("Fonts/Poppins-BlackItalic.ttf")
        # CTk.FontManager.load_font('Fonts/Transforma Mix/TransformaMix_Trial-Light.ttf')
        # CTk.FontManager.load_font('Fonts/CeraRoundPro/CeraRoundProDEMO-Thin.otf')

        self.width = 800
        self.height = 400

        # ----Creating and customizing the main window ---------
        self.title("Project Euler. Task 6.")

        self.res_width = self.winfo_screenwidth()  # window center calculation
        self.res_height = self.winfo_screenheight()  # window center calculation

        self.x = (self.res_width // 2) - (self.width // 2)  # window center calculation
        self.y = (self.res_height // 2) - (
            self.height // 2
        )  # window center calculation

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)

        self.my_font_Times = CTk.CTkFont(family="Times New Roman", size=23)
        # self.my_font_CeraRound = CTk.CTkFont(family='CeraRoundProDEMO-Thin', size=23)
        # self.my_font_MV = CTk.CTkFont(family="MV Boli Cyrillic", size=23)
        # self.my_font_Goznak = CTk.CTkFont(family="Goznak", size=25)
        # self.my_font_Poppins = ("Poppins-BlackItalic", 23)
        # self.my_font_Transforma_Mix = CTk.CTkFont(family='TransformaMix_Trial-Light', size=22)
        # self.my_font_Transforma_Mix = ('TransformaMix_Trial-Light', 20)

        # ----Widgets----------

        self.frame = CTk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0)

        self.toplevel_window = None

        self.lbn = CTk.CTkLabel(
            master=self.frame,
            text="Find the difference between the sum of the squares of the first \none hundred natural numbers and the square of the sum.",
            font=self.my_font_Times,
            text_color="#DAA520",
            width=800,
        )
        self.lbn.grid(row=0, column=0, pady=50)

        self.frame_radio_button = CTk.CTkFrame(master=self.frame)
        self.frame_radio_button.grid(row=1, column=0)

        self.radio_var = CTk.IntVar()

        self.radio_but = CTk.CTkRadioButton(
            master=self.frame_radio_button,
            text="- numbers from 1 to 10",
            font=self.my_font_Times,
            text_color="#DAA520",
            command=self.answer,
            variable=self.radio_var,
            value=11,
        )
        self.radio_but2 = CTk.CTkRadioButton(
            master=self.frame_radio_button,
            text="- numbers from 1 to 100",
            font=self.my_font_Times,
            text_color="#DAA520",
            command=self.answer,
            variable=self.radio_var,
            value=101,
        )
        self.radio_but.grid(row=0, column=0, padx=50)
        self.radio_but2.grid(row=0, column=1, padx=50)

        self.frame_button = CTk.CTkFrame(master=self.frame, width=self.width)
        self.frame_button.grid(row=2, column=0, pady=20)

        self.btn_rashet = CTk.CTkButton(
            master=self.frame_button,
            text="Calculate",
            command=self.open_toplevel,
            text_color="#DAA520",
        )
        self.btn_rashet.grid(row=0, column=0)

        self.btn = CTk.CTkButton(
            master=self.frame_button,
            text="ExiT",
            text_color="#DAA520",
            command=self.finish,
            hover_color="#04396C",
        )
        self.btn.grid(row=1, column=0, pady=130)

        self.toplevel_window = None

    # ----Functions-------------------------------------
    def open_toplevel(self):
        """
        start opening an additional window with an answer\n
        """
        if self.toplevel_window is None:
            self.toplevel_window = ToplevelWindow(
                self, closing_event=self.toplevel_close_event, rezult=self.answer()
            )  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def toplevel_close_event(self):
        self.toplevel_window = None

    def answer(self):
        print(f"{self.radio_var.get()}")
        self.radio = self.radio_var.get()
        print(self.radio)
        i = (
            math.trunc(math.pow((sum(a for a in range(1, (self.radio_var.get())))), 2))
        ) - (math.trunc(sum(math.pow(i, 2) for i in range(1, (self.radio_var.get())))))
        # i = math.pow(i, 2)
        # i = math.trunc(i)
        # a = math.trunc(math.pow((sum(a for a in range(1, 11))),2))
        # a = math.pow(a, 2)
        # a = math.trunc(a)
        # it = a - i
        print(i)
        return i

    def finish(self):
        """
        Function closes the window when the button is clicked.\n
        :param: self
        :return: Not
        """
        self.withdraw()  # closing the active window
        self.destroy()  # application closing
        print("Closed")


if __name__ == "__main__":
    app = App()
    app.mainloop()

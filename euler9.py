import customtkinter as CTk


class App(CTk.CTk):
    def __init__(self):
        """
        The main body of the program is a function.\n
        :param: None
        :return: None
        """
        super().__init__()

        # ----Customizing the appearance and theme of the GUI window---------
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("dark-blue")

        self.width = 800
        self.height = 500

        # ----Creating and customizing the main window ---------
        self.title("Project Euler. Task 9.")

        self.res_width = self.winfo_screenwidth()  # window center calculation
        self.res_height = self.winfo_screenheight()  # window center calculation

        self.x = (self.res_width // 2) - (self.width // 2)  # window positioning
        self.y = (self.res_height // 2) - (self.height // 2)  # window positioning

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)
        
        #----Font-----------------------------

        self.my_font_Times = CTk.CTkFont(family="Times New Roman", size=23)
        self.my_font_Futura = CTk.CTkFont(family="Futura", size=25)
        self.my_font_Luminari = CTk.CTkFont(family="Luminari", size=26)
        self.my_font_Cochin = CTk.CTkFont(family='Cochin', size=14)
        self.my_font_Cochin_25 = CTk.CTkFont(family='Cochin', size=25)
        # Luminari, Futura, Kokonor, Gharter, Cochin,  Ayuthaya
        # Kailiasa


        # ----Widgets---------------

        self.frame = CTk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0)

        self.btn_change = CTk.CTkButton(
            master=self.frame,
            text="Change Light/Dark",
            font=self.my_font_Cochin,
            text_color="#DAA520",
            command=self.change)
        self.btn_change.grid(row=0, column=0, sticky='e')

        self.lbn = CTk.CTkLabel(
            master=self.frame,
            text="There is only one Pythagoras triple for which a + b + c = 1000.",
            font=self.my_font_Futura,
            text_color="#FFBC00",
            width=self.width,
        )
        self.lbn.grid(row=1, column=0, pady=80)

        self.calculation()

        self.lbn_triple = CTk.CTkLabel(
            master=self.frame,
            text=f"{self.abc}",
            font=self.my_font_Futura,
            text_color="#FFBA00",
        )
        self.lbn_triple.grid(row=2, column=0)

        self.lbn_calculation = CTk.CTkLabel(
            master=self.frame,
            text=f"Answer: (a * b * c) = {self.calculation()}.",
            font=self.my_font_Futura,
            text_color="#FFBA00",
        )
        self.lbn_calculation.grid(row=3, column=0)

        self.progressbar = CTk.CTkProgressBar(
            master=self.frame,
            width=550,
        )
        self.progressbar.grid(row=4, column=0, pady=15)

        self.btn = CTk.CTkButton(
            master=self.frame,
            text="Exit",
            font=self.my_font_Cochin_25,
            text_color="#DAA520",
            command=self.finish,
            hover_color="#04396C",
        )
        self.btn.grid(row=5, column=0, pady=110)

        # ----set default values-----------------

        self.progressbar.configure(mode="indeterminnate")
        self.progressbar.start()
        self.node = 'dark'

        # ----Functions-------------------------------------

    def change(self):
        '''
        change of topics\n
        :param: None
        :rutern: None
        '''
        if self.node == "dark":
            CTk.set_appearance_mode("light")
            self.node = "light"
            self.lbn.configure(text_color='#9303A7')
            self.lbn_triple.configure(text_color='#9303A7')
            self.lbn_calculation.configure(text_color='#9303A7')
        else:
            CTk.set_appearance_mode("dark")
            self.node = "dark"
            self.lbn.configure(text_color='#FFBA00')
            self.lbn_triple.configure(text_color='#FFBA00')
            self.lbn_calculation.configure(text_color='#FFBA00')


    def calculation(self):
        """
        The selection of numbers goes: (a and b) - to increase the value
        (c) - for decreasing value\n
        :param:
        self
        :return:
        multiplication result line
        """
        for a in range(1, 1001):
            for b in range(a + 1, 1001):
                c = 1000 - a - b
                if a * a + b * b == c * c:
                    self.abc = str(f"(a = {a}) + (b = {b}) + (c = {c}) = 1000")
                    return str(a * b * c)

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

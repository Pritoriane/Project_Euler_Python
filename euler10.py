import customtkinter as CTk
import sys

class Calculation(CTk.CTkBaseClass):
    """
    Mathematical calculations of the answer to the problem
    """

    def __init__(self, master, *args, **kwards):
        super().__init__(master, *args, **kwards)

    def is_prime(self, number):
        """
        Сheck if the number is prime.\n
        :param: number- test number.
        :return: boolian
        """
        if number <= 1:
            return False
        for i in range(2, int(number**0.5) + 1):
            if number % i == 0:
                return False
        return True

    def calculate(self):
        result = []
        for number in range(2, 2_000):
            if self.is_prime(number):
                result.append(number)
        result = sum(result)

        return format(result, ",d").replace(",", ".")


class MyFont(CTk.CTkBaseClass):
    """
    Fonts\n
    :param: None
    :return: None
    """

    def __init__(self, master, *args, **kwards):
        super().__init__(master, *args, **kwards)

        self.my_font_Times = CTk.CTkFont(family="Times New Roman", size=23)
        self.my_font_Futura = CTk.CTkFont(family="Futura", size=25)
        self.my_font_Luminari = CTk.CTkFont(family="Luminari", size=26)
        self.my_font_Cochin = CTk.CTkFont(family="Cochin", size=14)
        self.my_font_Cochin_25 = CTk.CTkFont(family="Cochin", size=25)
        # Luminari, Futura, Kokonor, Gharter, Cochin,  Ayuthaya
        # Kailiasa


class App(CTk.CTk):
    '''
    Parental class.
    '''
    def __init__(self, *args, **kwards):
        """
        The main body of the program is a function.\n
        :param: None
        :return: None
        """
        super().__init__(*args, **kwards)

        # ----Customizing the appearance and theme of the GUI window---------
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("dark-blue")
        # CTk.enable_macos_darkmode()  # get darkmode window style

        self.width = 800
        self.height = 500

        # ----Creating and customizing the main window ---------
        self.title("Project Euler. Task 10.")

        self.res_width = self.winfo_screenwidth()  # window center calculation
        self.res_height = self.winfo_screenheight()  # window center calculation

        self.x = (self.res_width // 2) - (self.width // 2)  # window positioning
        self.y = (self.res_height // 2) - (self.height // 2)  # window positioning

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.my = MyFont(self)
        self.result = Calculation(self)

        self.frame = CTk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0)

        self.btn_change = CTk.CTkButton(
            master=self.frame,
            text="Change Light/Dark",
            font=self.my.my_font_Cochin,
            text_color="#DAA520",
            command=self.change,
        )
        self.btn_change.grid(row=0, column=0, sticky="e")

        self.lbn = CTk.CTkLabel(
            master=self.frame,
            text="The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.\n"
            "Find the sum of all the primes below two million.",
            font=self.my.my_font_Futura,
            text_color="#FFBC00",
            width=self.width,
        )
        self.lbn.grid(row=1, column=0, pady=80)

        self.btn_test = CTk.CTkButton(
            master=self.frame,
            fg_color="transparent",
            text=f"The sum of all prime numbers less than two million:\n {self.result.calculate()}",
            font=self.my.my_font_Futura,
            text_color="#FFBC00",
            hover_color="#412C84",
        )
        self.btn_test.grid(row=2, column=0, pady=30)

        self.progressbar = CTk.CTkProgressBar(
            master=self.frame,
            width=550,
        )
        self.progressbar.grid(row=4, column=0, pady=15)
        self.progressbar.configure(mode="indeterminnate", indeterminate_speed=1)
        self.progressbar.start()

        # ----set default values-----------------
        self.node = "dark"
        self.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))


        self.btn = CTk.CTkButton(
            master=self.frame,
            text="Exit",
            font=self.my.my_font_Cochin_25,
            text_color="#DAA520",
            command=self.finish,
            hover_color="#04396C",
        )
        self.btn.grid(row=6, column=0, pady=10)

    def change(self):
        """
        change of topics\n
        :param: None
        :rutern: None
        """
        if self.node == "dark":
            CTk.set_appearance_mode("light")
            self.node = "light"
            self.lbn.configure(text_color="#9303A7")

        else:
            CTk.set_appearance_mode("dark")
            self.node = "dark"
            self.lbn.configure(text_color="#FFBA00")

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

import customtkinter as CTk


class MyFrame(CTk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.label = CTk.CTkLabel(
            self,
            text=(
                "73167176531330624919225119674426574742355349194934\n"
                "96983520312774506326239578318016984801869478851843\n"
                "85861560789112949495459501737958331952853208805511\n"
                "12540698747158523863050715693290963295227443043557\n"
                "66896648950445244523161731856403098711121722383113\n"
                "62229893423380308135336276614282806444486645238749\n"
                "30358907296290491560440772390713810515859307960866\n"
                "70172427121883998797908792274921901699720888093776\n"
                "65727333001053367881220235421809751254540594752243\n"
                "52584907711670556013604839586446706324415722155397\n"
                "53697817977846174064955149290862569321978468622482\n"
                "83972241375657056057490261407972968652414535100474\n"
                "82166370484403199890008895243450658541227588666881\n"
                "16427171479924442928230863465674813919123162824586\n"
                "17866458359124566529476545682848912883142607690042\n"
                "24219022671055626321111109370544217506941658960408\n"
                "07198403850962455444362981230987879927244284909188\n"
                "84580156166097919133875499200524063689912560717606\n"
                "05886116467109405077541002256983155200055935729725\n"
                "71636269561882670428252483600823257530420752963450\n"
            ),
            text_color="#FFBC00",
        )
        self.label.grid(row=0, column=0, padx=20)


class App(CTk.CTk):
    def __init__(self):
        """
        The main body of the program is a function.\n
        :param: None
        :return: None
        """
        super().__init__()

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # ----Customizing the appearance and theme of the GUI window---------
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("dark-blue")

        self.width = 800
        self.height = 600

        # ----Creating and customizing the main window ---------
        self.title("Project Euler. Task 8.")

        self.res_width = self.winfo_screenwidth()  # window center calculation
        self.res_height = self.winfo_screenheight()  # window center calculation

        self.x = (self.res_width // 2) - (self.width // 2)  # window center calculation
        self.y = (self.res_height // 2) - (self.height // 2)  # window center calculation

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)

        self.my_font_Times = CTk.CTkFont(family="Times New Roman", size=23)
        self.my_font_Futura = CTk.CTkFont(family="Futura", size=25)
        self.my_font_Luminari = CTk.CTkFont(family="Luminari", size=26)
        # Luminari, Futura, impact

        self.list_of_numbers = list(
            "73167176531330624919225119674426574742355349194934"
            "96983520312774506326239578318016984801869478851843"
            "85861560789112949495459501737958331952853208805511"
            "12540698747158523863050715693290963295227443043557"
            "66896648950445244523161731856403098711121722383113"
            "62229893423380308135336276614282806444486645238749"
            "30358907296290491560440772390713810515859307960866"
            "70172427121883998797908792274921901699720888093776"
            "65727333001053367881220235421809751254540594752243"
            "52584907711670556013604839586446706324415722155397"
            "53697817977846174064955149290862569321978468622482"
            "83972241375657056057490261407972968652414535100474"
            "82166370484403199890008895243450658541227588666881"
            "16427171479924442928230863465674813919123162824586"
            "17866458359124566529476545682848912883142607690042"
            "24219022671055626321111109370544217506941658960408"
            "07198403850962455444362981230987879927244284909188"
            "84580156166097919133875499200524063689912560717606"
            "05886116467109405077541002256983155200055935729725"
            "71636269561882670428252483600823257530420752963450"
        )

        # ----Widgets---------------

        self.frame = CTk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0)

        self.lbn = CTk.CTkLabel(
            master=self.frame,
            text=(
                "The greatest product of four consecutive digits\n"
                "in the 1000-digit number below is 9 × 9 × 8 × 9 = 5832."
            ),
            text_color="#FFBC00",
            font=self.my_font_Futura,
            width=self.width,
        )
        self.lbn.grid(row=0, column=0)

        self.my_frame = MyFrame(
            master=self.frame,
            width=430,
            height=200,
            orientation="vertical",
            label_text="Given number:",
            # label_fg_color="blue",
            label_text_color="#FFBC00",
            label_font=self.my_font_Futura,
            label_anchor="center",  # "w",  # n, ne, e, se, s, sw, w, nw, center
            border_width=3,
            # border_color="green",
            # fg_color="red",
            scrollbar_fg_color="#0F4FA8",
            scrollbar_button_color="#4380D3",
            scrollbar_button_hover_color="#412C84",
            corner_radius=20,
        )
        self.my_frame.grid(row=1, column=0, padx=20, pady=20)

        self.lbn_answer = CTk.CTkLabel(
            master=self.frame,
            text=f"Answer: {self.calculation()}.",
            text_color="#FFBC00",
            font=self.my_font_Futura,
        )
        self.lbn_answer.grid(row=3, column=0, pady=10)

        self.lbn_answer = CTk.CTkLabel(
            master=self.frame,
            text=f"Multiplied sequence: {format(self.sequence_sp).replace(',', '×')}.",
            text_color="#FFBC00",
            font=self.my_font_Futura,
        )
        self.lbn_answer.grid(row=2, column=0, pady=10)

        self.btn = CTk.CTkButton(
            master=self,
            text="Exit",
            font=self.my_font_Luminari,
            text_color="#DAA520",
            command=self.finish,
            hover_color="#04396C",
        )
        self.btn.grid(row=4, column=0, pady=10)

        # ----Functions-------------------------------------

    def calculation(self):
        """
        Basic calculation\n
        :param: self
        :return: sequence - maximum value of multiplied numbers.
        """
        start_cutoff = 0
        end_cutoff = 13
        sequence = 0
        self.sequence_sp = ()

        while end_cutoff <= len(self.list_of_numbers):
            number_multiplication = 1
            for i in self.list_of_numbers[start_cutoff:end_cutoff]:
                number_multiplication *= int(i)
            if number_multiplication > sequence:
                sequence = number_multiplication
                self.sequence_sp = self.list_of_numbers[start_cutoff:end_cutoff]
            start_cutoff += 1
            end_cutoff += 1
            self.sequence_sp = [
                *map(int, self.sequence_sp)
            ]  # from list(str) to list(int)

        return format(sequence, ",d").replace(",", ".")

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

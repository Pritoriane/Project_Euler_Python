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
        self.height = 400

        # ----Creating and customizing the main window ---------
        self.title("Project Euler. Task 7.")

        self.res_width = self.winfo_screenwidth()  # window center calculation
        self.res_height = self.winfo_screenheight()  # window center calculation

        self.x = (self.res_width // 2) - (self.width // 2)  # window center calculation
        self.y = (self.res_height // 2) - (self.height // 2) # window center calculation

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)

        self.my_font_Times = CTk.CTkFont(family="Times New Roman", size=23)
        self.my_font_Futura = CTk.CTkFont(family="Futura", size=25)
        self.my_font_Luminari = CTk.CTkFont(family="Luminari", size=26) 
         # Luminari, Futura, impact

        #----Widgets---------------

        self.frame = CTk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0)

        self.lbn = CTk.CTkLabel(
            master=self.frame,
            text="By listing the first six prime numbers: 2,3,5,7,11 and 13,\n we can see that the 6th prime is 13.\nWhat is the 10001st prime number?",
            text_color="#FFBC00",
            font=self.my_font_Futura,
            width=self.width,
        )
        self.lbn.grid(row=0, column=0, pady=50)

        self.primes = self.calculation(150000)
        self.nth_primes = self.primes[10000]

        self.lbn_answer = CTk.CTkLabel(
            master=self.frame,
            text=f"10001st prime number: {self.nth_primes}.",
            text_color="#FFBC00",
            font=self.my_font_Futura,
        )
        self.lbn_answer.grid(row=1, column=0)

        self.btn = CTk.CTkButton(
            master=self,
            text="Exit",
            font=self.my_font_Luminari,
            text_color="#DAA520",
            command=self.finish,
            hover_color="#04396C",
        )
        self.btn.grid(row=2, column=0, pady=110)

        # ----Functions-------------------------------------

    def calculation(self, n):
        """
        Finds all prime numbers up to n using the Eratosthenes sieve.\n
        :param: n-search limit.
        :return: prime number list.
        """

        primes = [True] * (n + 1)
        primes[0] = primes[1] = False
        for i in range(2, int(n**0.5) + 1):
            if primes[i]:
                for j in range(i * i, n + 1, i):
                    primes[j] = False
        return [i for i, is_prime in enumerate(primes) if is_prime]

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

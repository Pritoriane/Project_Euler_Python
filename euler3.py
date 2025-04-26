import math
import customtkinter as CTk


class App(CTk.CTk):
    def __init__(self):
        '''
        The main body of the program is a function.\n
        :param: None
        :return: None
        '''
        super().__init__()

        self.title("Project Euler. Task 3.")
        self.geometry("700x400")
        self.resizable(False, False)
        self.my_font = CTk.CTkFont(family="Times New Roman", size=24)

        # Customizing the appearance and theme of the GUI window
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("green")

        self.frame1 = CTk.CTkFrame(master=self)
        self.frame1.grid(row=0, column=0)

        self.lbn = CTk.CTkLabel(
            master=self.frame1,
            text="What is the largest prime factor of the number 600851475143 ?",
            font=("Helvetica", 17),
            text_color="#808000",
            width=700,
        )
        self.lbn.grid(row=0, column=0, pady=100)

        self.lbn = CTk.CTkLabel(
            master=self.frame1,
            text=(f"Task response: {max(self.calculation(600851475143))}."),
            font=("Helvetica", 17),
            text_color="#808000",
        )
        self.lbn.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)

        self.btn = CTk.CTkButton(
            master=self.frame1, text="Click me", command=self.finish
        )
        self.btn.grid(row=2, column=0, pady=60)

    def calculation(self, n):
        """
        prime factor.\n
        :param: n - given number
        :return: list of prime divisors
        """
        answer = []
        r = math.ceil(math.sqrt(n))
        for i in range(3, r):
            if n % i == 0:
                if self.calculation(i) == []:
                    answer.append(i)
        print(answer)
        return answer

    def finish(self):
        """
        Function closes the window when the button is clicked.\n
        :param: Not
        :return: Not
        """
        self.withdraw()  # closing the active window
        self.destroy()  # application closing
        print("Closed")


if __name__ == "__main__":
    app = App()
    app.mainloop()

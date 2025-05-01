import customtkinter as CTk
import math


class App(CTk.CTk):
    def __init__(self):
        """
        The main body of the program is a function.\n
        :param: None
        :return: None
        """
        super().__init__()

        # Customizing the appearance and theme of the GUI window
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("green")

        self.title("Project Euler. Task 5.")
        self.geometry("800x400")
        self.resizable(False, False)
        self.my_font = CTk.CTkFont(family="Times New Roman", size=23)

        self.frame = CTk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0)

        self.lbl = CTk.CTkLabel(
            master=self.frame,
            text="What is the smallest positive number that is evenly divisible\n by all of the numbers from 1 to 20?",
            font=self.my_font,
            text_color="#DAA520",
            width=800,
        )
        self.lbl.grid(row=0, column=0, pady=100)

        self.lbl_answer = CTk.CTkLabel(
            master=self.frame,
            text=f"Answer: {self.least_multiple()}.",
            font=self.my_font,
            text_color="#DAA520",
        )
        self.lbl_answer.grid(row=1, column=0, pady=(30, 20))

        self.btn = CTk.CTkButton(
            master=self.frame, text="Click Me.", command=self.finish
        )
        self.btn.grid(row=2, column=0, pady=20)

    def least_multiple(self):
        """
        Сounting.\n
        :param:
        self
        :return:
        answer - minimum number
        """
        answer = 1
        for i in range(1, 21):
            answer *= i // math.gcd(i, answer)
        return answer

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

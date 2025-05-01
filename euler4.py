import customtkinter as CTk



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

        self.title("Project Euler. Task 4.")
        self.geometry("800x400")
        self.resizable(False, False)
        self.my_font = CTk.CTkFont(family="Times New Roman", size=23)

        self.frame1 = CTk.CTkFrame(master=self)
        self.frame1.grid(row=0, column=0)

        self.lbn = CTk.CTkLabel(
            master=self.frame1,
            text="Find the largest palindrome made from the product of two 3-digit numbers.",
            font=self.my_font,
            text_color="#DAA520",
            width=800,
        )
        self.lbn.grid(row=0, column=0, pady=100)

        self.polindrom()

        self.lbn1 = CTk.CTkLabel(
            master=self.frame1,
            text=f"The number {self.max_key} obtained by multiplying: {self.max_key_value}. ",
            font=self.my_font,
            text_color="#DAA520",
        )
        self.lbn1.grid(row=1, column=0, pady=50)

        self.btn = CTk.CTkButton(
            master=self.frame1, text="Click Me", command=self.finish
        )
        self.btn.grid(row=2, column=0, pady=10)

    
    def polindrom(self):
        """
        Searches for all palindromes of three-digit numbers.\n
        :param: self
        :return: 
        max_key - maximum number of palindromes,
        max_key_value - list of products of numbers.
        """
        is_poly = dict()
        for first_three_digit_number in range(100, 999):
            for second_three_digit_number in range(100, 999):
                valye = first_three_digit_number * second_three_digit_number
                poly = str(valye) == str(valye)[::-1]
                if poly is True:
                    print(f"{int(valye)} = {first_three_digit_number} * {second_three_digit_number}")
                    other = [(valye, (first_three_digit_number, second_three_digit_number))]
                    is_poly.update(other)
        print(is_poly)
        print(max(dict.keys(is_poly)))
        self.max_key = int(max(dict.keys(is_poly))) # biggest clue in the dictionary
        self.max_key_value = is_poly[self.max_key] # key values
        print(self.max_key_value)
        return self.max_key, self.max_key_value

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

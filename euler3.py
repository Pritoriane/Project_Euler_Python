import tkinter as tk
import math
from tkinter import *
from typing import Self
import customtkinter as CTk


class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project Euler. Task 3.")
        self.geometry("700x400")
        self.resizable(False, False)
        self.my_font = CTk.CTkFont(family="Times New Roman", size=24)

        # Настройка внешнего вида и темы GUI-окна
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("green")

        # configuring the location of the container using grid
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frame1 = CTk.CTkFrame(
            master=self,
            # font=('Helvetica', 17),
            # text_color='#006400',
            #bg_color="#FF00FF",
            #fg_color="#87CEEB",
        )
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
            text=(f"Task response: {max(self.calculation(600851475143))}"),
            font=("Helvetica", 17),
            text_color="#808000",
        )
        self.lbn.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)

        self.btn = CTk.CTkButton(master=self.frame1,
                                 text='Click me',
                                 command=self.finish)
        self.btn.grid(row=2, column=0, pady=60)

    def calculation(self, n):
        '''
        prime factor.\n
        :param: n - given number
        :return: list of prime divisors 
        '''
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
        self.withdraw() # closing the active window
        self.destroy() # application closing
        print("Closed")

        # self.column_frame1 = CTk.CTkFrame(master=self,
        #                                   border_color='#00BFFF',)
        # self.column_frame1.grid(row=0, column=0)

        # self.label1 = CTk.CTkLabel(master=self.column_frame1,
        #                            text='_1_',
        #                            width=50,
        #                            )
        # self.label1.grid(row=0, column=0,)

        # self.label2 = CTk.CTkLabel(master=self.column_frame1,
        #                            text='_2_',
        #                            width=50,
        #                            fg_color='#808000')
        # self.label2.grid(row=0, column=1)

        # self.label3 = CTk.CTkLabel(master=self.column_frame1, text='_3_', width=50)
        # self.label3.grid(row=0, column=3)

        # self.column_frame2 = CTk.CTkFrame(master=self,
        #                                   fg_color='#00FF00')
        # self.column_frame2.grid(row=1, column=0)

        # self.label4 = CTk.CTkLabel(master=self.column_frame2,
        #                            text='_4_',
        #                            width=50)
        # self.label4.grid(row=0, column=0)

        # self.label5 = CTk.CTkLabel(master=self.column_frame2,
        #                            text='_5_',
        #                            width=50)
        # self.label5.grid(row=0, column=1)

        # self.label6 = CTk.CTkLabel(master=self.column_frame2,
        #                            text='_6_',
        #                            width=50)
        # self.label6.grid(row=0, column=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()

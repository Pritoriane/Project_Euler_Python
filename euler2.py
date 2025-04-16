import tkinter as Tk
from tkinter import *
from tkinter import ttk


def main():
    def finish():
        """
        Function closes the window when the button is clicked.\n
        :param: Not
        :return: Not
        """
        window.destroy()
        print("Closed")

    window = Tk()
    window.title("Project Euler. Task 2.")
    window.geometry("600x200+400+200")

    lbl = Label(
        window,
        text=f"Find the sum of all even elements of the Fibonacci series that do not exceed four million",
    )
    lbl.place(relx=0.5, rely=0.1, anchor=CENTER)

    a = [1, 2]
    b = 0
    while b < 4_000_000:
        b = a[-1] + a[-2]
        a.append(b)

    rez = sum(_ for _ in a if _ % 2 == 0)

    lbl1 = Label(window, text=f"Answer: sum of numbers - {rez}.")
    lbl1.place(relx=0.5, rely=0.3, anchor=CENTER)

    btn = ttk.Button(text="Click Me", command=finish)
    btn.place(relx=0.5, rely=0.8, anchor=CENTER)

    window.mainloop()


if __name__ == "__main__":
    main()

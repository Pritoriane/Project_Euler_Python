import os
import tkinter as Tk
from tkinter import *
from tkinter import ttk


def main():
    def finish():
        window.destroy()
        print("Closed")

    window = Tk()
    window.title("Project Euler")
    window.geometry("350x200+400+200")

    lbl = Label(window, text=f"Find the sum of all the multiples of 3 or 5 below 1000.")
    lbl.place(relx=0.5, rely=0.1, anchor=CENTER)

    n = sum(n for n in range(1000) if (n % 3 == 0 or n % 5 == 0))

    lbl1 = Label(window, text=(f"Sum of all numbers: {n}"))
    lbl1.place(relx=0.5, rely=0.2, anchor=CENTER)

    btn = ttk.Button(text="Click Me", command=finish)
    btn.place(relx=0.5, rely=0.8, anchor=CENTER)

    window.mainloop()


if __name__ == "__main__":
    main()

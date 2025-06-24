import customtkinter as CTk
import sys
import numpy as np

import time


class MyFrameArray(CTk.CTkFrame):
    """
    Calculation of maximum value\n
    """

    def __init__(self, master, *args, **kwards):
        super().__init__(master, *args, **kwards)

        self.my = MyFont(master)
        self.grid_columnconfigure(0, weight=1)

        self.text_tasks = (
            "08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08\n"
            "49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00\n"
            "81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65\n"
            "52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91\n"
            "22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80\n"
            "24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50\n"
            "32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70\n"
            "67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21\n"
            "24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72\n"
            "21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95\n"
            "78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92\n"
            "16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57\n"
            "86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58\n"
            "19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40\n"
            "04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66\n"
            "88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69\n"
            "04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36\n"
            "20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16\n"
            "20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54\n"
            "01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48\n"
        )

        self.list_array()

        self.matrix_Lb()

        self.result = self.callculation()

    def list_array(self):
        """
        20x20 compliance check.\n
        Creating an array.\n
        """
        lines = self.text_tasks.strip().split("\n")
        numbers = [[int(num) for num in line.split()] for line in lines]
        assert len(numbers) == 20 and all(len(row) == 20 for row in numbers), (
            "Array should be 20x20!"
        )
        array_2d = np.array(numbers)
        self.matrix = array_2d

        print(f"Massiv:\n{self.matrix}")

    def matrix_Lb(self):
        """
        Forming an array for display\n
        """
        start_time = time.time()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                cell_value = str(self.matrix[i][j])
                cell_label = CTk.CTkLabel(
                    self,
                    text=cell_value,
                    text_color="#DAA520",
                    font=self.my.my_font_Cochin_14,
                    width=20,
                    height=20,
                    fg_color="transparent",
                    anchor="center",
                )
                cell_label.grid(row=i, column=j, sticky="nsew")
                setattr(self, f"cell_{i}_{j}", cell_label)
        time.sleep(1)
        end_time = time.time()

        elapsed_time = end_time - start_time
        print(f"Run time: {elapsed_time:.4f} seconds")

    def callculation(self):
        """
        Calculation of maximum value\n
        """
        max_product = 0
        best_sequence = []
        rows, cols = self.matrix.shape
        arr = self.matrix

        # Horizontal sequences
        for r in range(rows):
            for c in range(cols - 3):
                current_product = np.prod(arr[r, c : c + 4])
                if current_product > max_product:
                    max_product = current_product
                    best_sequence = [(r, c + k) for k in range(4)]

        # Vertical sequences
        for c in range(cols):
            for r in range(rows - 3):
                current_product = np.prod(arr[r : r + 4, c])
                if current_product > max_product:
                    max_product = current_product
                    best_sequence = [(r + k, c) for k in range(4)]

        # Diagonal (from left to right from top to bottom)
        for r in range(rows - 3):
            for c in range(cols - 3):
                current_product = np.prod([arr[r + k, c + k] for k in range(4)])
                if current_product > max_product:
                    max_product = current_product
                    best_sequence = [(r + k, c + k) for k in range(4)]

        # Reverse diagonals (from right to left from bottom to top)
        for r in range(3, rows):
            for c in range(cols - 3):
                current_product = np.prod([arr[r - k, c + k] for k in range(4)])
                if current_product > max_product:
                    max_product = current_product
                    best_sequence = [(r - k, c + k) for k in range(4)]

        # Selection of elements
        for r, c in best_sequence:
            getattr(self, f"cell_{r}_{c}").configure(text_color="red")

        print(f"Maximum product: {max_product}, sequence: {best_sequence}")
        return max_product


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
        self.my_font_Cochin_14 = CTk.CTkFont(family="Cochin", size=14)
        self.my_font_Cochin_25 = CTk.CTkFont(family="Cochin", size=25)
        self.my_font_Gharter = CTk.CTkFont(family="Gharter", size=24)
        # Luminari, Futura, Kokonor, Gharter, Cochin,  Ayuthaya
        # Kailiasa


class App(CTk.CTk):
    """
    Parental class.
    """

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

        self.width = 1000
        self.height = 700
        self.node = "dark"

        # ----Creating and customizing the main window ---------
        self.title("Project Euler. Task 11.")

        self.res_width = self.winfo_screenwidth()  # window center calculation
        self.res_height = self.winfo_screenheight()  # window center calculation

        self.x = (self.res_width // 2) - (self.width // 2)  # window positioning
        self.y = (self.res_height // 2) - (self.height // 2)  # window positioning

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.my = MyFont(self)

        self.my_arr = MyFrameArray(self)
        self.max_product = self.my_arr.result

        self.frame = CTk.CTkFrame(
            master=self, height=self.height)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_configure()
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.btn_change = CTk.CTkButton(
            master=self.frame,
            text="Change Light/Dark",
            font=self.my.my_font_Cochin_14,
            text_color="#DAA520",
            command=self.change,
        )
        self.btn_change.grid(row=0, column=0, sticky="e")

        self.lbn = CTk.CTkLabel(
            master=self.frame,
            text="What is the greatest product of four consecutive numbers\n"
            "in a 20×20 table arranged in any direction (up, down, right, left, or diagonal)?",
            font=self.my.my_font_Futura,
            text_color="#FFBC00",
            width=self.width,
        )
        self.lbn.grid(row=1, column=0, pady=(25, 25))
        self.lbn.bind(
            "<Enter>", lambda event: self.lbn.configure(text_color=("#FFF900"))
        )
        self.lbn.bind(
            "<Leave>", lambda event: self.lbn.configure(text_color=("#FFBC00"))
        )

        self.frame_array = MyFrameArray(self.frame)
        self.frame_array.grid(row=2, column=0)

        self.lbn_calculate = CTk.CTkLabel(
            master=self.frame,
            text=f"Maximum product: {format(self.max_product, ',d').replace(',', '.')}",
            font=self.my.my_font_Futura,
            text_color="#DAA520",
            # command=self.my_arr.vid_rez()
        )
        self.lbn_calculate.grid(row=3, column=0, pady=(10, 20))

        self.progressbar = CTk.CTkProgressBar(
            master=self.frame,
            width=550,
        )
        self.progressbar.grid(row=4, column=0, pady=10)
        self.progressbar.configure(mode="indeterminnate", indeterminate_speed=1)
        self.progressbar.start()

        self.btn = CTk.CTkButton(
            master=self.frame,
            text="Exit",
            font=self.my.my_font_Cochin_25,
            text_color="#DAA520",
            command=self.finish,
        )
        self.btn.grid(row=5, column=0, pady=(10, 10))
        self.btn.grid_configure(sticky="s")
        self.btn.bind(
            "<Enter>",
            lambda event: self.btn.configure(border_width=2, border_color="#00BFFF"),
        )
        self.btn.bind(
            "<Leave>",
            lambda event: self.btn.configure(border_width=0, border_color=None),
        )
        # ----set default values-----------------

        self.node = "dark"
        self.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    # ----Functions-------------------------------------

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
            self.lbn.bind(
                "<Enter>", lambda event: self.lbn.configure(text_color=("#9303F7"))
            )
            self.lbn.bind(
                "<Leave>", lambda event: self.lbn.configure(text_color=("#9303A7"))
            )
        else:
            CTk.set_appearance_mode("dark")
            self.node = "dark"
            self.lbn.configure(text_color="#FFBA00")
            self.lbn.bind(
                "<Enter>", lambda event: self.lbn.configure(text_color=("#FFF900"))
            )
            self.lbn.bind(
                "<Leave>", lambda event: self.lbn.configure(text_color=("#FFBC00"))
            )

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

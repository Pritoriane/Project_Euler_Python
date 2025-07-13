import customtkinter as CTk
import sys
import threading
import time


class Calculation(CTk.CTkBaseClass):
    """
    A class for calculating triangular numbers and counting their divisors.
    Inherited from CTkBaseClass for integration with CustomTkinter.
    """
    
    def __init__(self, master, *args, **kwargs):
        """
        Initialization of the computation class.
        
        Attributes:
            triangular_number: triangular number found
            divisor_count: the number of divisors of the found number
            progress_callback: function to update progress in GUI
            current_n: current value of n during calculations
            is_calculating: calculation activity flag
        """
        super().__init__(master, *args, **kwargs)
        self.triangular_number = 0
        self.divisor_count = 0
        self.progress_callback = None
        self.current_n = 0
        self.is_calculating = False
    
    def set_progress_callback(self, callback):
        """
        Sets the callback function to update the progress.
        
        Args:
            callback: function that will be called to update the GUI
        """
        self.progress_callback = callback
    
    def calc(self, target_divisors=500):
        """
        Finds the first triangular number with the number of divisors greater than target_divisors.
        
        Triangular number T(n) = 1 + 2 + 3 + ... + n = n(n+1)/2
        
        Args:
            target_divisors: minimum number of divisors (default 500)
        Returns:
            First triangular number with the right number of divisors
        """
        self.is_calculating = True
        n = 1
        
        while self.is_calculating:
            # Triangular number formula: T(n) = n * (n + 1) / 2
            triangular = n * (n + 1) // 2
            
            # Count the number of divisors
            divisors = self.count_divisors(triangular)
            
            # Update progress every 50 iterations for optimization
            if n % 50 == 0 and self.progress_callback:
                self.current_n = n
                self.progress_callback(n, triangular, divisors)
            
            # Check the problem condition
            if divisors > target_divisors:
                self.triangular_number = triangular
                self.divisor_count = divisors
                self.is_calculating = False
                
                # Final Progress Update
                if self.progress_callback:
                    self.progress_callback(n, triangular, divisors)
                
                return triangular
            
            n += 1
        
        return None  # If the calculation was interrupted
    
    def stop_calculation(self):
        """Stops the current calculation"""
        self.is_calculating = False
    
    def count_divisors(self, number):
        """
        Effectively counts the number of divisors of a number.
        
        Algorithm:
        1. Check the divisors only up to the square root of the number
        2. If i divides number, then number/i is also a divisor
        3. special case: if i = sqrt(number), count only once.
        
        Args:
            number: divisor count
            
        Returns:
            Number of divisors of a number
        """
        count = 0
        sqrt_n = int(number ** 0.5)
        
        for i in range(1, sqrt_n + 1):
            if number % i == 0:
                if i * i == number:
                    # Square root - count only once
                    count += 1
                else:
                    # i and number/i are two different divisors
                    count += 2
        
        return count


class MyFont(CTk.CTkBaseClass):
    """
    A class for managing application fonts.
    Centralized storage of all used fonts.
    """
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # Define all fonts used
        self.my_font_Times = CTk.CTkFont(family="Times New Roman", size=23)
        self.my_font_Futura = CTk.CTkFont(family="Futura", size=25)
        self.my_font_Luminari = CTk.CTkFont(family="Luminari", size=26)
        self.my_font_Cochin_14 = CTk.CTkFont(family="Cochin", size=14)
        self.my_font_Cochin_16 = CTk.CTkFont(family="Cochin", size=16)
        self.my_font_Cochin_20 = CTk.CTkFont(family="Cochin", size=20)
        self.my_font_Cochin_25 = CTk.CTkFont(family="Cochin", size=25)
        self.my_font_Gharter = CTk.CTkFont(family="Gharter", size=24)


class App(CTk.CTk):
    """
    The main class of the application.
    Creates GUI and controls all program components.
    """
    
    def __init__(self, *args, **kwargs):
        """Initializing the main application window"""
        super().__init__(*args, **kwargs)
        
        # ----Customizing the appearance---------
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("dark-blue")
        
        # Window parameters
        self.width = 1000
        self.height = 550
        self.node = "dark"  # Current topic
        
        # ----Customizing the main window---------
        self.title("Project Euler - Task 12: Triangular numbers")
        
        # Centering the window on the screen
        self.res_width = self.winfo_screenwidth()
        self.res_height = self.winfo_screenheight()
        self.x = (self.res_width // 2) - (self.width // 2)
        self.y = (self.res_height // 2) - (self.height // 2)
        
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(False, False)
        
        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initializing components
        self.my = MyFont(self)
        self.my_calc = Calculation(self)
        self.my_calc.set_progress_callback(self.update_progress)
        
        # Variables to control calculations
        self.calculation_thread = None
        self.start_time = None
        
        # Spinner animation
        self.spinner_phases = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.spinner_index = 0
        
        # Interface creation
        self.create_widgets()
        
        # Window closing handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Creating all interface widgets"""
        
        # Main Frame
        self.frame = CTk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Theme button
        self.btn_change = CTk.CTkButton(
            master=self.frame,
            text="🌓 Change Light/Dark",
            font=self.my.my_font_Cochin_14,
            text_color="#DAA520",
            command=self.change,
            width=150
        )
        self.btn_change.grid(row=0, column=0, sticky="e", padx=10, pady=5)
        
        # Header with the task question
        self.lbn = CTk.CTkLabel(
            master=self.frame,
            text="Which first triangular number has more than 500 divisors?",
            font=self.my.my_font_Futura,
            text_color="#FFBC00",
            wraplength=900
        )
        self.lbn.grid(row=1, column=0, pady=(20, 10))
        
        # Task Description
        self.description_label = CTk.CTkLabel(
            master=self.frame,
            text="Triangular numbers: T(n) = 1 + 2 + 3 + ... + n = n(n+1)/2",
            font=self.my.my_font_Cochin_16,
            text_color="#888888"
        )
        self.description_label.grid(row=2, column=0, pady=(0, 20))
        
        # Label for result
        self.lbn2 = CTk.CTkLabel(
            master=self.frame,
            text='Click “Start Calculation” to start the calculation',
            font=self.my.my_font_Cochin_20,
            text_color='#00FF00'
        )
        self.lbn2.grid(row=3, column=0, pady=(10, 10))
        
        # Label for current progress
        self.progress_label = CTk.CTkLabel(
            master=self.frame,
            text="",
            font=self.my.my_font_Cochin_16,
            text_color='#FFD700'
        )
        self.progress_label.grid(row=4, column=0, pady=(5, 10))
        
        # Time stamp
        self.time_label = CTk.CTkLabel(
            master=self.frame,
            text="",
            font=self.my.my_font_Cochin_14,
            text_color='#87CEEB'
        )
        self.time_label.grid(row=5, column=0, pady=(5, 10))
        
        # Button to start calculations
        self.btn_start = CTk.CTkButton(
            master=self.frame,
            text="▶️ Start calculation",
            font=self.my.my_font_Cochin_20,
            text_color="#DAA520",
            command=self.start_calculation,
            width=250,
            height=40
        )
        self.btn_start.grid(row=6, column=0, pady=(15, 10))
        
        # Progress bar
        self.progressbar = CTk.CTkProgressBar(
            master=self.frame,
            width=600,
            height=20,
            progress_color="#00FF00"
        )
        self.progressbar.grid(row=7, column=0, pady=(10, 20))
        self.progressbar.set(0)
        
        # Information panel
        self.info_frame = CTk.CTkFrame(master=self.frame, fg_color="transparent")
        self.info_frame.grid(row=8, column=0, pady=(10, 20))
        
        self.info_label = CTk.CTkLabel(
            master=self.info_frame,
            text="💡 Hint: The answer is among the first 15,000 triangular numbers",
            font=self.my.my_font_Cochin_14,
            text_color="#666666"
        )
        self.info_label.pack()
        
        # Exit button
        self.btn = CTk.CTkButton(
            master=self.frame,
            text="❌ Exit",
            font=self.my.my_font_Cochin_25,
            text_color="#DAA520",
            command=self.finish,
            width=150,
            height=40
        )
        self.btn.grid(row=9, column=0, pady=(10, 20))
        
        # Targeting effects
        self._setup_hover_effects()
    
    def _setup_hover_effects(self):
        """Customizing hover effects for widgets"""
        # Effect for header
        self.lbn.bind(
            "<Enter>", lambda e: self.lbn.configure(text_color="#FFF900")
        )
        self.lbn.bind(
            "<Leave>", lambda e: self.lbn.configure(
                text_color="#FFBC00" if self.node == "dark" else "#9303A7"
            )
        )
        
        # Effect for the exit button
        self.btn.bind(
            "<Enter>", lambda e: self.btn.configure(
                border_width=2, border_color="#FF0000"
            )
        )
        self.btn.bind(
            "<Leave>", lambda e: self.btn.configure(
                border_width=0
            )
        )
        
        # Effect for the calculation start button
        self.btn_start.bind(
            "<Enter>", lambda e: self.btn_start.configure(
                border_width=2, border_color="#00FF00"
            ) if self.btn_start.cget("state") != "disabled" else None
        )
        self.btn_start.bind(
            "<Leave>", lambda e: self.btn_start.configure(
                border_width=0
            )
        )
        
        # Effect for theme button
        self.btn_change.bind(
            "<Enter>", lambda e: self.btn_change.configure(
                border_width=2, border_color="#FFD700"
            )
        )
        self.btn_change.bind(
            "<Leave>", lambda e: self.btn_change.configure(
                border_width=0
            )
        )
    
    def start_calculation(self):
        """
        Starts the calculation in a separate thread.
        Prevents restarting if the calculation is already in progress.
        """
        # Check for active calculation
        if self.calculation_thread and self.calculation_thread.is_alive():
            return
        
        # Resetting and preparing the UI
        self.btn_start.configure(text="⏸️ Calculated...", state="disabled")
        self.lbn2.configure(text="🔍 Finding the triangular number...")
        self.progress_label.configure(text="Let the calculations begin...")
        self.info_label.configure(text="🔄 It may take a few seconds...")
        self.progressbar.set(0)
        self.start_time = time.time()
        
        # Starting the calculation flow
        self.calculation_thread = threading.Thread(target=self.run_calculation)
        self.calculation_thread.daemon = True
        self.calculation_thread.start()
        
        # Starting animations
        self.update_animation()
        self.update_time()
    
    def run_calculation(self):
        """
        Executes the calculation in a separate thread.
        Calls calculation_complete in the main thread after completion.
        """
        try:
            result = self.my_calc.calc(500)  # Looking for a number with more than 500 divisors
            
            # Plan to update the UI in the main thread
            self.after(0, self.calculation_complete, result)
        except Exception as e:
            self.after(0, self.calculation_error, str(e))
    
    def calculation_complete(self, result):
        """
        Called after successful completion of calculations.
        Updates the UI with the results.
        """
        if result is None:
            self.lbn2.configure(text="❌ The calculation was interrupted")
            self.btn_start.configure(text="▶️ Start calculation", state="normal")
            return
        
        divisors = self.my_calc.divisor_count
        elapsed_time = time.time() - self.start_time
        
        # Formatting the result with thousands separators
        formatted_result = format(result, ",d").replace(",", " ")
        
        self.lbn2.configure(
            text=f'✅ Found it! Triangular number: {formatted_result}'
        )
        self.progress_label.configure(
            text=f"Number of divisors: {divisors} | "
                 f"It's a {self.my_calc.current_n} triangular number"
        )
        self.time_label.configure(
            text=f"⏱️ Execution time: {elapsed_time:.2f} seconds"
        )
        self.info_label.configure(
            text=f"✨ Problem solved! Checked {self.my_calc.current_n} triangular numbers"
        )
        
        self.progressbar.set(1.0)
        self.btn_start.configure(text="🔄 Recalculate", state="normal")
    
    def calculation_error(self, error_msg):
        """Handling calculation errors"""
        self.lbn2.configure(text=f"❌ Error:{error_msg}")
        self.btn_start.configure(text="▶️ Start calculation", state="normal")
        self.progressbar.set(0)
    
    def update_progress(self, n, triangular, divisors):
        """
        Updates the display of calculation progress.
        Called from the calculation thread via callback.
        """
        # Progress estimate (empirical formula)
        # We know that the answer is about n=12375
        progress = min(n / 13000, 0.95)
        
        # Formatting large numbers
        formatted_triangular = format(triangular, ",d").replace(",", " ")
        
        # Plan to update the UI in the main thread
        self.after(0, lambda: self.progressbar.set(progress))
        self.after(0, lambda: self.progress_label.configure(
            text=f"Check: n = {n} | T({n}) = {formatted_triangular} | "
                 f"Dividers:{divisors}"
        ))
    
    def update_animation(self):
        """
        Updates the spinner animation during computation.
        Recursively invokes itself every 100ms.
        """
        if self.calculation_thread and self.calculation_thread.is_alive():
            # Upgrading the spinner
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_phases)
            spinner = self.spinner_phases[self.spinner_index]
            
            current_text = self.lbn2.cget("text")
            if "Search" in current_text:
                self.lbn2.configure(text=f"🔍 Finding a triangular number {spinner}")
            
            # We are planning the next update
            self.after(100, self.update_animation)
    
    def update_time(self):
        """
        Updates the runtime display.
        Recursively calls itself every 100ms.
        """
        if self.calculation_thread and self.calculation_thread.is_alive():
            elapsed = time.time() - self.start_time
            self.time_label.configure(text=f"⏱️ Time: {elapsed:.1f} sec.")
            
            # We are planning the next update
            self.after(100, self.update_time)
    
    def change(self):
        """
        Switches the application theme between light and dark.
        Updates the colors of all interface elements.
        """
        if self.node == "dark":
            # Shifting to a lighter theme
            CTk.set_appearance_mode("light")
            self.node = "light"
            self.lbn.configure(text_color="#9303A7")
            self.description_label.configure(text_color="#666666")
            
            # Update the hover effects for the light theme
            self.lbn.bind(
                "<Enter>", lambda e: self.lbn.configure(text_color="#9303F7")
            )
            self.lbn.bind(
                "<Leave>", lambda e: self.lbn.configure(text_color="#9303A7")
            )
        else:
            # Switching to a dark theme
            CTk.set_appearance_mode("dark")
            self.node = "dark"
            self.lbn.configure(text_color="#FFBC00")
            self.description_label.configure(text_color="#888888")
            
            # Update the hover effects for the dark theme
            self.lbn.bind(
                "<Enter>", lambda e: self.lbn.configure(text_color="#FFF900")
            )
            self.lbn.bind(
                "<Leave>", lambda e: self.lbn.configure(text_color="#FFBC00")
            )
    
    def on_closing(self):
        """
        Window closing handler.
        Safely stops calculations and closes the application.
        """
        # Stop calculations if they are active
        if self.my_calc:
            self.my_calc.stop_calculation()
        
        # Wait for the stream to complete (maximum 1 second)
        if self.calculation_thread and self.calculation_thread.is_alive():
            self.calculation_thread.join(timeout=1.0)
        
        # Closing the application
        self.destroy()
        sys.exit(0)
    
    def finish(self):
        """
        Exit button handler.
        Causes safe closing of the application.
        """
        self.on_closing()


# ----Program entry point----
if __name__ == "__main__":
    app = App()
    app.mainloop()
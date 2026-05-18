import sys
import math
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QPlainTextEdit,
    QPushButton
)
from PySide6.QtCore import Qt, Signal, Slot, QObject, QThread
from PySide6.QtGui import QPixmap
from pathlib import Path

#--*-- Main Window --*--
class MainWindow(QMainWindow):
    """ Главное окно приложения """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Euler. Task 15")
        self.resize(700,500)

        self.thread = None

        self.setup_central_widget()
        self.setup_pages()
        self.setup_signals()
        self.apply_styles()



    def setup_central_widget(self):
        """Создаём центральный виджет и основной layout"""
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)
        self.stacked = QStackedLayout()
        self.main_layout.addLayout(self.stacked)
        self.statusBar().showMessage("What ?")

    def setup_pages(self):
        """Создаём две страницы: условие и не вычисления"""
        #--*-- page 1 --*--
        self.page_task = QWidget()
        task_layout = QVBoxLayout(self.page_task)

        self.label_title = QLabel("Task 15. Lattice Paths")
        self.label_title.setObjectName('task_title')
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        task_layout.addWidget(self.label_title)
        
        #--*-- HTML --*--
        html = """
            <h4>Начиная в левом верхнем углу сетки 2×2 и имея возможность двигаться только вниз или вправо, 
            существует ровно 6 маршрутов до правого нижнего угла сетки.</h4>


            <p>Сколько существует таких маршрутов в сетке 20×20?</p>            
        """

        #--*--  Виджет для текста HTML --*--
        self.label_task = QLabel()
        self.label_task.setObjectName('task_description')
        self.label_task.setText(html)
        self.label_task.setTextFormat(Qt.RichText)
        self.label_task.setWordWrap(True)
        self.label_task.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_layout.addWidget(self.label_task)

        self.label_pix = QLabel()
        self.label_pix.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_path = Path(__file__).parent / "Images" /"p015.png"

        pixmap = QPixmap(str(image_path))


        if pixmap.isNull():
            print(f"Image not loaded {image_path}")
        else:
            scaled = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            self.label_pix.setPixmap(scaled)

        task_layout.addWidget(self.label_pix)

        task_layout.addStretch()

        self.button_calc = QPushButton('Do the calculation ...  \U00002705')
        task_layout.addWidget(self.button_calc)

        #--*-- page 2 --*--
        self.page_calc = QWidget()
        calc_layout = QVBoxLayout(self.page_calc)

        self.calc_title = QLabel('Calculation')
        self.calc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calc_layout.addWidget(self.calc_title)

        #--*-- information display field --*--
        self.result_box = QPlainTextEdit()
        self.result_box.setReadOnly(True)
        calc_layout.addWidget(self.result_box)

        #--*-- button panel --*--
        button_layout = QHBoxLayout()

        self.button_start = QPushButton('Start      \U00002705')
        button_layout.addWidget(self.button_start)

        self.button_cancel = QPushButton('Cancel   \U0000274C')
        self.button_cancel.setEnabled(False)
        button_layout.addWidget(self.button_cancel)

        self.button_back = QPushButton('\U00002B05  Back')
        button_layout.addWidget(self.button_back)

        calc_layout.addLayout(button_layout)
        calc_layout.addStretch()

        #--*-- Add both pages to the stacked layout --*--
        self.stacked.addWidget(self.page_task)
        self.stacked.addWidget(self.page_calc)


    def setup_signals(self):
        """Connecting buttons to methods"""

        self.button_calc.clicked.connect(self.switch_to_calculator)
        self.button_start.clicked.connect(self.start_calculation)
        self.button_cancel.clicked.connect(self.cancel_computation)
        self.button_back.clicked.connect(self.switch_to_task)




    def apply_styles(self):
        #--*-- Стили приложения --*--
        self.setStyleSheet('''
            QWidget {
                font-family: Times;
                font-size: 20pt;
                font-weight: bold;
                font-style: italic;
            }

            QLabel#task_title {
                font-size: 24pt;
                font-weight: bold;
                color: #2c3e50;
            }

            QLabel#task_description {
                font-size: 19pt;
                font-weight: normal;
                color: #555;
                font-style: italic;
            }
            QPushButton {
                background-color: #8FBC8F;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 18pt;
                font-style: normal;
            }

            QPushButton:hover {
                background-color: #9ACD32;
            }

            QPushButton:pressed {
                background-color: #004085;
            }  
        ''')

    @Slot()
    def switch_to_task(self):
        """ Go to the Terms and Conditions page """
        self.stacked.setCurrentIndex(0)
        self.statusBar().showMessage('Ready')

    @Slot()
    def switch_to_calculator(self):
        """Go to the calculations page""" 

        self.result_box.clear()

        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)
           
        self.stacked.setCurrentIndex(1)
        self.statusBar().showMessage('Calculator opened')


    @Slot()
    def start_calculation(self):
        """ Start calculations """

        if self.thread and self.thread.isRunning():
            return
        
        self.result_box.clear()

        self.result_box.appendPlainText('Starting calculation...')
        self.result_box.appendPlainText('We count the number of paths in a 20x20 grid...')
        self.result_box.appendPlainText('')

        self.button_start.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.button_back.setEnabled(False)

        self.statusBar().showMessage('Working...')

        # Создаём поток
        self.thread = WorkerThread(limit=20)

        # Подключаем сигналы worker к методам GUI
        self.thread.worker.finished.connect(self.computation_finished)
        self.thread.worker.error.connect(self.computation_error)

        # Когда поток завершится, освобождаем ресурсы
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.finished.connect(self.thread_finished_cleanup)

        # Запускаем поток
        self.thread.start()
        
       

    @Slot()
    def cancel_computation(self):
        """ Cancellation of calculations """

        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.result_box.appendPlainText("Cancellation requested...")
            self.statusBar().showMessage("Cancelling...")

        self.button_cancel.setEnabled(False)


    @Slot(str)
    def computation_error(self, message):
        """Если в worker произошла ошибка"""

        self.result_box.appendPlainText("")
        self.result_box.appendPlainText(f"Error: {message}")

        self.statusBar().showMessage("Error")

        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)

        self.thread = None

    @Slot(object)
    def computation_finished(self, number):
        """Вызывается, когда вычисление завершено"""

        self.result_box.appendPlainText("")
        self.result_box.appendPlainText("Calculation completed.")
        
        #--*-- Разделитель числа --*--
        formatted = f"{number:,}".replace(",", ". ") 
        self.result_box.appendPlainText(f"Number of paths: {formatted}")
        
        self.statusBar().showMessage("Done")

        # Возвращаем кнопки в нормальное состояние
        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)

        
    @Slot()
    def thread_finished_cleanup(self):
     self.thread = None

class  WaysWorker(QObject):
    finished = Signal(object)

    error = Signal(str)

    def __init__(self, limit=20):
        super().__init__()
        
        self.limit = limit
        self._is_cancelled = False

    def stop(self):
         # Этот метод вызывается из GUI, если пользователь нажал Cancel
        self._is_cancelled = True
    
    @Slot()
    def run(self):
        """
        Этот метод будет выполнен в отдельном потоке.
        Здесь нельзя трогать GUI напрямую.
        """

        try:
            self.number_of_tracks = math.comb(2 * self.limit, self.limit)

            self.finished.emit(self.number_of_tracks)

        except Exception as e:
            self.error.emit(str(e))



#--*-- ПОТОК: оболочка вокруг worker --*--
class WorkerThread(QThread):
    """
    Отдельный QThread нужен, чтобы GUI не зависал.
    """

    def __init__(self, limit=20 ):
        super().__init__()

        # Создаём worker
        self.worker = WaysWorker(limit)
        self.worker.moveToThread(self)

        # Когда поток запускается, вызывается run()
        self.started.connect(self.worker.run)

        # Когда worker заканчивает, поток можно завершить
        self.worker.finished.connect(self.quit)
        self.worker.error.connect(self.quit)

        self.finished.connect(self.worker.deleteLater)

    def stop(self):
        # Проксируем остановку внутрь worker
        self.worker.stop()

        







if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

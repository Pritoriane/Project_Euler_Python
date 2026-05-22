import sys
import socket
import struct
import time
from datetime import datetime, timezone, timedelta
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QPlainTextEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal, Slot, QObject, QThread
from PySide6.QtWidgets import QGraphicsDropShadowEffect


# --*-- Main Window --*--
class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Euler. Task 16")
        self.resize(700, 500)

        self.thread = None
        self.worker = None
        self.time_thread = None
        self.time_worker = None
        self.utc_now = None
        self.utc_timer = QTimer(self)

        self.setup_central_widget()
        self.setup_pages()
        self.setup_signals()
        self.apply_styles()
        self.start_utc_sync()

    def setup_central_widget(self):
        """Создаём центральный виджет и основной layout"""

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.main_layout = QVBoxLayout(self.central)

        self.utc_label = QLabel("UTC: synchronizing...")
        self.utc_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.utc_label.setObjectName('utc_label')
        self.main_layout.addWidget(self.utc_label)

        self.stacked = QStackedLayout()
        self.main_layout.addLayout(self.stacked)

        self.statusBar().showMessage("Ready")

    def setup_pages(self):
        """Создаём две страницы: условие и вычисления"""

        # --*-- Page 1 --*--
        self.page_task = QWidget()
        task_layout = QVBoxLayout(self.page_task)

        self.label_title = QLabel("Task 16. Power Digit Sum.")
        self.label_title.setObjectName("task_title")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_layout.addWidget(self.label_title)

        # --*-- HTML --*--
        html = """
            <h4>2<sup>15</sup> = 32768, сумма цифр этого числа равна 3 + 2 + 7 + 6 + 8 = 26.</h4>


            <p>Какова сумма цифр числа 2<sup>1000</sup>?</p>            
        """

        self.label_task = QLabel()
        self.label_task.setObjectName("task_description")
        self.label_task.setText(html)
        self.label_task.setTextFormat(Qt.RichText)
        self.label_task.setWordWrap(True)
        self.label_task.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_layout.addWidget(self.label_task)

        task_layout.addStretch()

        self.button_calc = GlowButton("Do the calculation...     \U00002705")
        task_layout.addWidget(self.button_calc)

        # --*-- Page 2 --*--
        self.page_calc = QWidget()
        calc_layout = QVBoxLayout(self.page_calc)

        self.calc_title = QLabel("Calculations")
        self.calc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calc_layout.addWidget(self.calc_title)

        # --*-- information display field --*--
        self.result_box = QPlainTextEdit()
        self.result_box.setReadOnly(True)
        calc_layout.addWidget(self.result_box)

        # --*-- button panel --*--
        button_layout = QHBoxLayout()

        self.button_start = GlowButton("Start      \U00002705")
        button_layout.addWidget(self.button_start)

        self.button_cancel = GlowButton("Cancel   \U0000274C")
        self.button_cancel.setEnabled(False)
        button_layout.addWidget(self.button_cancel)

        self.button_back = GlowButton("\U00002B05  Back")
        button_layout.addWidget(self.button_back)

        calc_layout.addLayout(button_layout)
        calc_layout.addStretch()

        # --*-- Add both pages to the stacked layout --*--
        self.stacked.addWidget(self.page_task)
        self.stacked.addWidget(self.page_calc)

    def setup_signals(self):
        """Connecting buttons to methods"""

        self.button_calc.clicked.connect(self.switch_to_calculator)
        self.button_start.clicked.connect(self.start_computation)
        self.button_cancel.clicked.connect(self.cancel_computation)
        self.button_back.clicked.connect(self.switch_to_task)

    def apply_styles(self):
        """Стили приложения"""

        self.setStyleSheet(
            """
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

            QLabel#utc_label {
                color: #52C852	;
                font-family: Menlo;
                font-size: 12pt;
                font-style: normal;
                font-weight: normal;
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
        """
        )

    def start_utc_sync(self):
        self.time_thread = QThread()
        self.time_worker = TimeWorker()

        self.time_worker.moveToThread(self.time_thread)

        self.time_thread.started.connect(self.time_worker.run)

        self.time_worker.finished.connect(self.utc_sync_finished)
        self.time_worker.error.connect(self.utc_sync_error)

        self.time_worker.finished.connect(self.time_thread.quit)
        self.time_worker.error.connect(self.time_thread.quit)

        self.time_thread.finished.connect(self.time_worker.deleteLater)
        self.time_thread.finished.connect(self.time_thread.deleteLater)
        self.time_thread.finished.connect(self.time_sync_cleanup)

        self.time_thread.start()

    @Slot(object)
    def utc_sync_finished(self, utc_time):
        self.utc_now = utc_time

        if not self.utc_timer.isActive():
            self.utc_timer.timeout.connect(self.update_utc_clock)
            self.utc_timer.start(1000)


        self.update_utc_clock()

    @Slot(str)
    def utc_sync_error(self, message):
        # Если интернет-синхронизация не сработала, показываем локальное UTC,
        # чтобы часы всё равно работали, а причину ошибки выводим в терминал.
        self.utc_now = datetime.now(timezone.utc)

        if not self.utc_timer.isActive():
            self.utc_timer.timeout.connect(self.update_utc_clock)
            self.utc_timer.start(1000)

        self.update_utc_clock()
        self.statusBar().showMessage("UTC sync failed. Local UTC fallback is used.")
        print(f"UTC sync error: {message}")



    @Slot()
    def update_utc_clock(self):
        if self.utc_now is None:
            return
        
        self.utc_label.setText("UTC+0: " + self.utc_now.strftime("%Y-%m-%d %H:%M:%S"))

        self.utc_now += timedelta(seconds=1)


    @Slot()
    def time_sync_cleanup(self):
        self.time_thread = None
        self.time_worker = None

    @Slot()
    def switch_to_task(self):
        """Go to the Terms and Conditions page"""

        self.stacked.setCurrentIndex(0)
        self.statusBar().showMessage("Ready")

    @Slot()
    def switch_to_calculator(self):
        """Go to the calculations page"""

        self.result_box.clear()

        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)

        self.stacked.setCurrentIndex(1)
        self.statusBar().showMessage("Calculator opened")

    @Slot()
    def start_computation(self):
        """Start calculations"""

        if self.thread and self.thread.isRunning():
            return

        self.result_box.clear()
        text = f"<p>We calculate the sum of the digits of the number 2<sup>1000</sup> ...</p>"

        self.result_box.appendPlainText("Starting calculation...")
        self.result_box.appendHtml(text)
        self.result_box.appendPlainText("")

        self.button_start.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.button_back.setEnabled(False)

        self.statusBar().showMessage("Working...")

        # Создаём поток
        self.thread = QThread()
        self.worker = WaysWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        # Подключаем сигналы worker к методам GUI
        self.worker.finished.connect(self.computation_finished)
        self.worker.error.connect(self.computation_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        # Когда поток завершится, освобождаем ресурсы
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread_finished_cleanup)

        # Запускаем поток
        self.thread.start()

    def cancel_computation(self):
        """Cancellation of calculations"""

        if self.thread and self.thread.isRunning():
            self.worker.stop()
            self.result_box.appendPlainText("Cancellation requested...")
            self.statusBar().showMessage("Cancelling...")

        self.button_cancel.setEnabled(False)

    @Slot(str)
    def computation_error(self, message):
        """Если в worker произошла ошибка"""

        self.result_box.appendPlainText("")
        self.result_box.appendPlainText(f"Error: {message}.")

        self.statusBar().showMessage("Error.")

        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)

    @Slot(object)
    def computation_finished(self, number):
        """Вызывается, когда вычисление завершено"""

        self.result_box.appendPlainText("")
        self.result_box.appendPlainText("Calculation completed.")
        self.result_box.appendPlainText(f"Sum of numbers: {number}")

        self.statusBar().showMessage("Done")

        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)

    @Slot()
    def thread_finished_cleanup(self):

        self.thread = None
        self.worker = None


class GlowButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)

        self.shadow = QGraphicsDropShadowEffect()
        
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(2, 2)

        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):

        self.shadow.setBlurRadius(40)
        
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow.setBlurRadius(15)

        super().leaveEvent(event)




class WaysWorker(QObject):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self):
        super().__init__()

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
            num = 2**1000
            self.sum_of_numbers = sum(int(digit) for digit in str(num))

            self.finished.emit(self.sum_of_numbers)
        except Exception as e:
            self.error.emit(str(e))


class TimeWorker(QObject):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.ntp_servers = (
            "time.google.com",
            "pool.ntp.org",
            "time.cloudflare.com",
            "time.apple.com",
        )

    def get_ntp_time(self, host):
        """Получаем UTC-время с NTP-сервера через UDP, без HTTPS и SSL."""
        ntp_delta = 2_208_988_800
        packet = b"\x1b" + 47 * b"\0"

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(4)
            sock.sendto(packet, (host, 123))
            data, _ = sock.recvfrom(48)

        if len(data) < 48:
            raise ValueError("Bad NTP response")

        seconds = struct.unpack("!12I", data)[10]
        unix_time = seconds - ntp_delta
        return datetime.fromtimestamp(unix_time, tz=timezone.utc)

    @Slot()
    def run(self):
        errors = []

        for server in self.ntp_servers:
            try:
                utc_time = self.get_ntp_time(server)
                self.finished.emit(utc_time)
                return
            except Exception as e:
                errors.append(f"{server}: {e}")

        self.error.emit("; ".join(errors))


# --*-- ТОЧКА ВХОДА --*--
if __name__ == "__main__":
    # Создаём объект приложения Qt
    app = QApplication(sys.argv)

    # Создаём главное окно
    window = MainWindow()

    # Показываем окно
    window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())

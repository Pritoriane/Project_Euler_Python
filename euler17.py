import sys
import socket
import struct
from datetime import datetime, timezone, timedelta
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
from PySide6.QtCore import (
    Qt, 
    Signal, 
    Slot, 
    QObject, 
    QTimer, 
    QRunnable,
    QThreadPool,
)
from PySide6.QtWidgets import QGraphicsDropShadowEffect

# --*-- ЧАСТЬ 1: СИГНАЛЫ ДЛЯ ЗАДАЧИ --*--

class UTCTaskSignals(QObject):
    """
    Сигналы для передачи данных из потока в главный поток.
    """
    finished = Signal(object)  # Передаёт объект datetime
    error = Signal(str)        # Передаёт сообщение об ошибке


# --*-- ЗАДАЧА ДЛЯ ПОЛУЧЕНИЯ UTC (QRunnable) --*--

class UTCSyncTask(QRunnable):
    """
    Задача для синхронизации UTC-времени через NTP-сервер.
    """ 
   
    
    def __init__(self):
        """
        Конструктор задачи.     
        """
        super().__init__()
        
        self.signals = UTCTaskSignals()
        
        self.ntp_servers = (
            "time.google.com",      # Надёжный сервер Google
            "pool.ntp.org",         # Пул общедоступных NTP-серверов
            "time.cloudflare.com",  # Сервер Cloudflare
            "time.apple.com",       # Сервер Apple
        )
    
    def get_ntp_time(self, host):
        """
        Получает UTC-время с NTP-сервера.
        """
        
        ntp_delta = 2_208_988_800
        packet = b'\x1b' + 47 * b'\0'
        
        # Создаём UDP-сокет
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(4)

            sock.sendto(packet, (host, 123))
            
            data, _ = sock.recvfrom(48)
        
        # Проверяем размер ответа
        if len(data) < 48:
            raise ValueError('Bad NTP response: too short')
        
        seconds = struct.unpack('!12I', data)[10]
        
        # Переводим NTP-время в Unix-время (вычитаем смещение)
        unix_time = seconds - ntp_delta
        
        # Создаём объект datetime с часовым поясом UTC
        return datetime.fromtimestamp(unix_time, tz=timezone.utc)
    
    @Slot()
    def run(self):
        """
        Главный метод, выполняемый в отдельном потоке.
        """
        errors = []  # Список ошибок для каждого сервера
        
        # Пробуем каждый NTP-сервер по очереди
        for server in self.ntp_servers:
            try:
                # Пытаемся получить время с этого сервера
                utc_time = self.get_ntp_time(server)
                
                # Успешно! Отправляем сигнал с временем в главный поток
                self.signals.finished.emit(utc_time)
                
                # Выходим из метода (задача завершена успешно)
                return
                
            except Exception as e:
                # Запоминаем ошибку для этого сервера
                errors.append(f'{server}: {e}')
                # Продолжаем со следующим сервером
        
        # Все серверы не ответили — отправляем сигнал об ошибке
        error_message = '; '.join(errors)
        self.signals.error.emit(error_message)

# ==============================================
# СИГНАЛЫ ДЛЯ ЗАДАЧИ ВЫЧИСЛЕНИЙ
# ==============================================

class EulerTaskSignals(QObject):
    """
    Сигналы для задачи вычисления Project Euler.
    """
    progress = Signal(int)        # Прогресс в процентах (0-100)
    result = Signal(str)          # Готовый результат (строка)
    error = Signal(str)           # Сообщение об ошибке
    finished = Signal()           # Сигнал о завершении


# ==============================================
# ЗАДАЧА ВЫЧИСЛЕНИЙ (QRunnable)
# ==============================================

class EulerTask(QRunnable):
    """
    Задача для вычисления Project Euler #17.
    
    Задача: Сколько букв в английских названиях чисел от 1 до 1000?
    
    Алгоритм:
    1. Функция number_to_words преобразует число в английское слово
    2. Суммируем длины всех слов
    3. Отправляем результат через сигнал
    """
    
    def __init__(self):
        super().__init__()
        self.signals = EulerTaskSignals()
        self.is_cancelled = False  # Флаг для отмены вычислений
    
    def number_to_words(self, n):
        """
        Преобразует число в английское слово.
        
        Например:
        1 → "one"
        21 → "twentyone"
        100 → "onehundred"
        101 → "onehundredandone"
        1000 → "onethousand"
        
        Аргументы:
            n (int): Число от 1 до 1000
            
        Возвращает:
            str: Английское написание числа
        """
        # Особый случай: 1000
        if n == 1000:
            return "onethousand"
        
        # Слова для чисел от 1 до 19
        ones = [
            "", "one", "two", "three", "four", "five", "six", "seven", 
            "eight", "nine", "ten", "eleven", "twelve", "thirteen", 
            "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", 
            "nineteen"
        ]
        
        # Слова для десятков (20, 30, 40, ...)
        tens = [
            "", "", "twenty", "thirty", "forty", "fifty", 
            "sixty", "seventy", "eighty", "ninety"
        ]
        
        words = ""
        
        # Обработка сотен (100-999)
        if n >= 100:
            # n // 100 — количество сотен (например, 345 // 100 = 3)
            words += ones[n // 100] + "hundred"
            
            # Если есть остаток, добавляем "and"
            if n % 100 != 0:
                words += "and"
        
        # Обработка десятков и единиц
        remainder = n % 100
        
        # Если остаток меньше 20, используем таблицу ones
        if remainder < 20:
            words += ones[remainder]
        else:
            # Иначе: десятки + единицы
            # remainder // 10 — десятки (например, 45 // 10 = 4 → "forty")
            # remainder % 10 — единицы (например, 45 % 10 = 5 → "five")
            words += tens[remainder // 10] + ones[remainder % 10]
        
        return words
    
    def cancel(self):
        """Отменяет выполнение задачи."""
        self.is_cancelled = True
    
    @Slot()
    def run(self):
        """
        Главный метод, выполняемый в отдельном потоке.
        """
        try:
            total_letters = 0
            total_numbers = 1000
            
            # Проходим по всем числам от 1 до 1000
            for i in range(1, total_numbers + 1):
                # Проверяем, не запрошена ли отмена
                if self.is_cancelled:
                    self.signals.error.emit("Вычисления отменены пользователем")
                    self.signals.finished.emit()
                    return
                
                # Получаем английское написание числа
                word = self.number_to_words(i)
                
                # Добавляем длину слова к общей сумме
                total_letters += len(word)
                
                # Каждые 100 чисел отправляем прогресс (10% от общего объёма)
                # 100 чисел = 10% от 1000
                if i % 100 == 0:
                    progress_percent = int((i / total_numbers) * 100)
                    self.signals.progress.emit(progress_percent)
            
            # Отправляем 100% прогресс
            self.signals.progress.emit(100)
            
            # Формируем результат
            result_message = (
                f"Задача 17. Number Letter Counts\n"
                f"{'=' * 40}\n"
                f"Общее количество букв: {total_letters}\n"
                f"{'=' * 40}\n"
                f"Проверка:\n"
                f"1-5: 19 букв\n"
                f"1-1000: {total_letters} букв"
            )
            
            # Отправляем результат
            self.signals.result.emit(result_message)
            
        except Exception as e:
            self.signals.error.emit(f"Ошибка при вычислении: {str(e)}")
        finally:
            self.signals.finished.emit()


# --*-- Main Window --*--
class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Euler. Task 17")
        self.resize(700,500)

        self.thread = None
        self.worker = None
        self.time_thread = None
        self.time_worker = None
        self.utc_now = None
        self.utc_timer = QTimer(self)

        # Для вычислений - ИСПРАВЛЕНО: добавляем все атрибуты
        self.current_task = None      # Текущая задача (EulerTask)
        self.utc_task = None          # Задача для UTC
        self.thread_pool = None       # Пул потоков
        self.is_running = False       # Флаг выполнения вычислений
        self.is_cancelling = False    # Флаг отмены

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

        self.statusBar().showMessage('Ready...')

    def setup_pages(self):
        """Создаём две страницы: условие и вычисления"""

        # --*-- Pages 1 --*--
        self.page_task = QWidget()
        task_layout = QVBoxLayout(self.page_task)

        self.label_title = QLabel('Task 17.Number Letter Counts.')
        self.label_title.setObjectName('tsk_title')
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_layout.addWidget(self.label_title)

        # --*-- HTML --*--
        html = """
            <h4>Если записать числа от 1 до 5 английскими словами (one, two, three, four, five)
            , то используется всего 3 + 3 + 5 + 4 + 4 = 19 букв.</h4>


            <p>Сколько букв понадобится для записи всех чисел
              от 1 до 1000 (one thousand) включительно?</p>            
        """

        self.label_task = QLabel()
        self.label_task.setObjectName('task_description')
        self.label_task.setText(html)
        self.label_task.setTextFormat(Qt.RichText)
        self.label_task.setWordWrap(True)
        self.label_task.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_layout.addWidget(self.label_task)

        task_layout.addStretch()

        self.button_calc = GlowButton("Do the calculation...     \U00002705")
        task_layout.addWidget(self.button_calc)
        #_________________
        # --- Page 2 --*--
        #_________________

        self.page_calc =QWidget()
        calc_layout = QVBoxLayout(self.page_calc)

        self.calc_title = QLabel('Calculations')
        self.calc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calc_layout.addWidget(self.calc_title)

        # --*-- information display field --*--
        self.result_box = QPlainTextEdit()
        self.result_box.setReadOnly(True)
        calc_layout.addWidget(self.result_box)

        # --*-- button panel --*--
        button_layout = QHBoxLayout()

        self.button_start = GlowButton('Start   \U00002705')
        button_layout.addWidget(self.button_start)

        self.button_cancel = GlowButton('Cancel     \U0000274C')
        self.button_cancel.setEnabled(False)
        button_layout.addWidget(self.button_cancel)

        self.button_back = GlowButton('\U00002B05      Back')
        button_layout.addWidget(self.button_back)

        calc_layout.addLayout(button_layout)
        calc_layout.addStretch()

        # --*-- Add both pages to the stacked layout --*--
        self.stacked.addWidget(self.page_task)
        self.stacked.addWidget(self.page_calc)

    def setup_signals(self):
        """Connecting buttons to methods"""

        self.button_calc.clicked.connect(self.switch_to_calculation)
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


    # --*-- ЧАСТЬ 4: УПРАВЛЕНИЕ UTC СИНХРОНИЗАЦИЕЙ --*--
    
    def start_utc_sync(self):
        """
        Запускает синхронизацию UTC-времени в отдельном потоке.
        """
        
        # Получаем глобальный пул потоков
        self.thread_pool = QThreadPool.globalInstance()
        
        # Создаём задачу для синхронизации UTC
        self.current_task = UTCSyncTask()
        
        # Подключаем сигналы задачи к слотам в главном потоке
        self.current_task.signals.finished.connect(self.utc_sync_finished)
        self.current_task.signals.error.connect(self.utc_sync_error)
        
        # Запускаем задачу в пуле потоков
        self.thread_pool.start(self.current_task)
        
        # Логируем в статус-бар
        self.statusBar().showMessage('Синхронизация UTC...')
    
    @Slot(object)
    def utc_sync_finished(self, utc_time):
        """
        Обработчик успешной синхронизации UTC.
        
        Вызывается в ГЛАВНОМ потоке (сигнал автоматически доставляет сюда).
        
        Аргументы:
            utc_time (datetime): Полученное UTC-время
        """
        # Сохраняем полученное время
        self.utc_now = utc_time
        
        # Если таймер ещё не запущен, запускаем его
        if not self.utc_timer.isActive():
            self.utc_timer.timeout.connect(self.update_utc_clock)
            self.utc_timer.start(1000)  # Обновляем каждую секунду
        
        # Обновляем отображение времени
        self.update_utc_clock()
        
        # Показываем статус
        self.statusBar().showMessage('UTC синхронизирован')
    
    @Slot(str)
    def utc_sync_error(self, message):
        """
        Обработчик ошибки синхронизации UTC.
        
        Если не удалось получить время с NTP-серверов,
        используем локальное UTC-время.
        
        Аргументы:
            message (str): Сообщение об ошибке
        """
        # Используем локальное UTC-время как запасной вариант
        self.utc_now = datetime.now(timezone.utc)
        
        # Запускаем таймер для обновления часов
        if not self.utc_timer.isActive():
            self.utc_timer.timeout.connect(self.update_utc_clock)
            self.utc_timer.start(1000)
        
        # Обновляем отображение
        self.update_utc_clock()
        
        # Показываем сообщение об ошибке
        self.statusBar().showMessage('Ошибка синхронизации UTC. Используется локальное время.')
        print(f'Ошибка синхронизации UTC: {message}')
    
    @Slot()
    def update_utc_clock(self):
        """
        Обновляет отображение UTC-часов каждую секунду.
        
        Вызывается по таймеру (каждую секунду).
        """
        if self.utc_now is None:
            return
        
        # Форматируем и отображаем время
        self.utc_label.setText(f'UTC+0: {self.utc_now.strftime("%Y-%m-%d %H:%M:%S")}')
        
        # Увеличиваем время на 1 секунду (для следующего обновления)
        self.utc_now += timedelta(seconds=1)
    

    # ==============================================
    # УПРАВЛЕНИЕ ВЫЧИСЛЕНИЯМИ
    # ==============================================
    
    def switch_to_calculation(self):
        """Переключает на страницу вычислений."""
        self.stacked.setCurrentWidget(self.page_calc)
        self.statusBar().showMessage('Нажмите Start для начала вычислений')
    
    def switch_to_task(self):
        """Возвращает на страницу условия задачи."""
        # Если вычисления ещё выполняются, не даём уйти
        if self.is_running:
            self.result_box.appendPlainText(
                '\n⚠️ Сначала отмените или дождитесь завершения вычислений!'
            )
            return
        
        self.stacked.setCurrentWidget(self.page_task)
        self.statusBar().showMessage('Ready...')
    
    def start_computation(self):
        """
        Запускает вычисления в отдельном потоке.
        """
        # Проверяем, не запущены ли уже вычисления
        if self.is_running:
            self.result_box.appendPlainText('\n⚠️ Вычисления уже запущены!')
            return
        
        # Очищаем поле результатов
        self.result_box.clear()
        self.result_box.appendPlainText('🚀 Запуск вычислений...')
        self.result_box.appendPlainText('-' * 50)
        
        # Блокируем кнопки
        self.button_start.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.button_back.setEnabled(False)
        self.button_calc.setEnabled(False)
        
        # Устанавливаем флаг выполнения
        self.is_running = True
        
        # Создаём задачу вычислений
        self.current_task = EulerTask()
        
        # Подключаем сигналы
        self.current_task.signals.progress.connect(self.on_progress)
        self.current_task.signals.result.connect(self.on_result)
        self.current_task.signals.error.connect(self.on_error)
        self.current_task.signals.finished.connect(self.on_finished)
        
        # Запускаем задачу в ТОМ ЖЕ пуле потоков
        # QThreadPool сам распределит задачи между потоками
        self.thread_pool.start(self.current_task)
        
        self.statusBar().showMessage('Вычисления запущены...')
    
    def cancel_computation(self):
        """Отменяет вычисления."""
        if self.current_task and self.is_running:
            # Вызываем метод отмены
            self.current_task.cancel()
            self.result_box.appendPlainText('\n⏳ Отмена запрошена...')
            self.statusBar().showMessage('Отмена вычислений...')
            self.button_cancel.setEnabled(False)
            self.is_cancelling = True
    
    @Slot(int)
    def on_progress(self, percent):
        """
        Обработчик прогресса вычислений.
        
        Вызывается из потока вычислений через сигнал.
        """
        # Показываем прогресс в статус-баре
        self.statusBar().showMessage(f'Выполняется вычисление... {percent}%')
        
        # Обновляем поле результатов
        self.result_box.appendPlainText(f'Прогресс: {percent}%')
        
        # Прокручиваем вниз (чтобы видеть последние сообщения)
        scrollbar = self.result_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    @Slot(str)
    def on_result(self, result):
        """
        Обработчик получения результата.
        
        Вызывается из потока вычислений через сигнал.
        """
        self.result_box.appendPlainText('\n' + '=' * 50)
        self.result_box.appendPlainText('📊 РЕЗУЛЬТАТ:')
        self.result_box.appendPlainText('=' * 50)
        self.result_box.appendPlainText(result)
        self.statusBar().showMessage('✅ Вычисления завершены!')
    
    @Slot(str)
    def on_error(self, error_message):
        """
        Обработчик ошибок.
        
        Вызывается из потока вычислений через сигнал.
        """
        self.result_box.appendPlainText(f'\n❌ Ошибка: {error_message}')
        self.statusBar().showMessage(f'❌ {error_message}')
    
    @Slot()
    def on_finished(self):
        """
        Обработчик завершения задачи (успешного или с ошибкой).
        
        Всегда вызывается после завершения, даже если была ошибка.
        """
        # Снимаем флаг выполнения
        self.is_running = False
        
        # Разблокируем кнопки
        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)
        self.button_calc.setEnabled(True)
        
        # Очищаем ссылку на задачу
        self.current_task = None
        
        self.is_cancelling = False

        # Обновляем статус-бар, если не было ошибки
        if "Ошибка" not in self.statusBar().currentMessage():
            self.statusBar().showMessage('Готово. Нажмите Start для повторного запуска.')
        
        # Добавляем разделитель в результат
        self.result_box.appendPlainText('\n' + '-' * 50)
        self.result_box.appendPlainText('✅ Задача завершена.')


    
   
    
    def closeEvent(self, event):
        """
        Обработка закрытия окна.
        
        Важно: нужно корректно завершить все потоки.
        """
        # Останавливаем таймер
        if self.utc_timer:
            self.utc_timer.stop()
        
        # Если есть активные задачи, ждём их завершения
        if self.thread_pool and self.thread_pool.activeThreadCount() > 0:
            # Даём потокам время на завершение (2 секунды)
            self.thread_pool.waitForDone(2000)
        
        event.accept()


class GlowButton(QPushButton):
    
    def __init__(self,text):
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



#--*-- Entry Point --*--
if __name__ == "__main__":
    # Создаём объект приложения Qt
    app = QApplication(sys.argv)

    # Создаём главное окно
    window = MainWindow()

    # Показываем окно
    window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())
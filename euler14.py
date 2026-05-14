import sys

# Импортируем основные виджеты Qt:
# QApplication - объект приложения
# QMainWindow - главное окно
# QWidget - базовый виджет
# QLabel - надпись
# QVBoxLayout / QHBoxLayout - вертикальные / горизонтальные layout
# QStackedLayout - "стопка" страниц, где видна только одна
# QPlainTextEdit - простое текстовое поле
# QPushButton - кнопка
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

# Импортируем базовые вещи из QtCore:
# Qt - флаги и настройки
# Signal - сигналы
# Slot - слоты
# QObject - базовый класс для объектов Qt
# QThread - поток
from PySide6.QtCore import Qt, Signal, Slot, QObject, QThread


# ------------------------------------------------------------
# ВОРКЕР: объект, который будет выполнять вычисления в отдельном потоке
# ------------------------------------------------------------
class CollatzWorker(QObject):
    # Сигнал прогресса:
    # current - какое число сейчас проверяется
    # best_start - лучшее стартовое число на данный момент
    # best_length - лучшая длина на данный момент
    progress = Signal(int, int, int)

    # Сигнал завершения:
    # best_start - число, которое дало самую длинную последовательность
    # best_length - длина этой последовательности
    finished = Signal(int, int)

    # Сигнал ошибки
    error = Signal(str)

    def __init__(self, limit=1_000_000):
        # Вызываем конструктор QObject
        super().__init__()

        # Верхняя граница поиска
        self.limit = limit

        # Флаг остановки
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
            # Лучшая найденная длина последовательности
            best_length = 0

            # Стартовое число, давшее лучшую длину
            best_start = 1

            # Кэш:
            # сохраняем уже известные длины последовательностей,
            # чтобы не считать одно и то же много раз
            cache = {1: 1}

            # Перебираем все стартовые числа от 1 до limit-1
            for start in range(1, self.limit):
                # Если пользователь нажал Cancel, прекращаем вычисления
                if self._is_cancelled:
                    return

                # Считаем длину последовательности для текущего start
                length = self.collatz_length(start, cache)

                # Если нашли более длинную последовательность, обновляем рекорд
                if length > best_length:
                    best_length = length
                    best_start = start

                # Не надо слать сигнал на каждый шаг слишком часто,
                # иначе GUI будет лишний раз нагружаться.
                # Поэтому отправляем прогресс, например, каждые 5000 чисел.
                if start % 5000 == 0:
                    self.progress.emit(start, best_start, best_length)

            # Когда всё закончено, отправляем финальный результат
            self.finished.emit(best_start, best_length)

        except Exception as e:
            # Если что-то пошло не так, шлём текст ошибки
            self.error.emit(str(e))

    def collatz_length(self, n, cache):
        """
        Считает длину последовательности Коллатца для числа n.
        Используем cache, чтобы ускорить вычисления.
        """

        # Если длина уже была посчитана раньше, просто возвращаем её
        if n in cache:
            return cache[n]

        # Здесь будем хранить промежуточный путь:
        # например, n -> ... -> число, которое уже есть в cache
        path = []

        current = n

        # Идём по последовательности, пока не попадём в уже известное значение
        while current not in cache:
            path.append(current)

            if current % 2 == 0:
                # Если число чётное, делим на 2
                current = current // 2
            else:
                # Если нечётное, применяем правило 3n + 1
                current = 3 * current + 1

        # Теперь current уже есть в cache,
        # значит длина для него известна
        known_length = cache[current]

        # Идём назад по path в обратном порядке
        # и восстанавливаем длины для всех чисел в пути
        for i, value in enumerate(reversed(path), start=1):
            cache[value] = known_length + i

        # Возвращаем длину для исходного n
        return cache[n]


# ------------------------------------------------------------
# ПОТОК: оболочка вокруг worker
# ------------------------------------------------------------
class WorkerThread(QThread):
    """
    Отдельный QThread нужен, чтобы GUI не зависал.
    """

    def __init__(self, limit=1_000_000):
        super().__init__()

        # Создаём worker
        self.worker = CollatzWorker(limit)

        # Когда поток запускается, вызывается run()
        self.started.connect(self.worker.run)

        # Когда worker заканчивает, поток можно завершить
        self.worker.finished.connect(self.quit)
        self.worker.error.connect(self.quit)

    def stop(self):
        # Проксируем остановку внутрь worker
        self.worker.stop()


# ------------------------------------------------------------
# ГЛАВНОЕ ОКНО
# ------------------------------------------------------------
class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        # Заголовок окна
        self.setWindowTitle("Project Euler. Task 14")

        # Размер окна
        self.resize(700, 550)

        # Переменная для потока
        self.thread = None

        # Создаём центральную часть окна
        self.setup_central_widget()

        # Создаём страницы
        self.setup_pages()

        # Подключаем сигналы кнопок
        self.setup_signals()

        # Применяем стили
        self.apply_styles()

    def setup_central_widget(self):
        """Создаём центральный виджет и основной layout"""

        # Центральный виджет нужен для QMainWindow
        self.central = QWidget()

        # Назначаем его центром окна
        self.setCentralWidget(self.central)

        # Главный layout окна
        self.main_layout = QVBoxLayout(self.central)

        # Здесь будут лежать страницы
        self.stacked = QStackedLayout()

        # Добавляем stacked layout в основной layout
        self.main_layout.addLayout(self.stacked)

        # Статус-бар внизу окна
        self.statusBar().showMessage("Ready")

    def setup_pages(self):
        """Создаём две страницы: условие и вычисления"""

        # ============================================================
        # СТРАНИЦА 1: условие задачи
        # ============================================================
        self.page_task = QWidget()
        task_layout = QVBoxLayout(self.page_task)

        # Заголовок
        self.label_title = QLabel("Task 14. Longest Collatz Sequence.")
        self.label_title.setObjectName("task_title")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_layout.addWidget(self.label_title)

        # HTML-текст условия
        html = """
            <h4 align=center>Следующая повторяющаяся последовательность определена для множества натуральных чисел:</h4>
            <ul>
                <li><b>n → n/2</b> (<i>n</i> - четное)</li>
                <Li><b>n → 3n + 1</b> (<i>n</i> - нечетное)</li>
            </ul>
            
            <p>Используя описанное выше правило и начиная с <b>13</b>, сгенерируется следующая последовательность:</p
            <p align="center" style="font-family:monospace; font-size:14px; margin:10px 0;">
            <b>13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1</b>
            </p>
            <br>
            <p>Получившаяся последовательность (начиная с <b>13</b> и заканчивая <b>1</b>) содержит <b>10</b> элементов.</p>
            <p>Хотя это до сих пор и не доказано (проблема Коллатца (Collatz)), предполагается,</p>
            <p>что все сгенерированные таким образом последовательности оканчиваются на <b>1</b>.</p>
            
            <p>Какой начальный элемент меньше миллиона генерирует самую длинную последовательность?</p>
            
            <p><small>Примечание: Следующие за первым элементы последовательности могут быть больше миллиона.<small/></p>
        """

        # Виджет для текста условия
        self.label_task = QLabel()
        self.label_task.setObjectName("task_description")
        self.label_task.setText(html)
        self.label_task.setTextFormat(Qt.RichText)
        self.label_task.setWordWrap(True)
        self.label_task.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_layout.addWidget(self.label_task)

        # Пустое пространство
        task_layout.addStretch()

        # Кнопка перехода на страницу расчётов
        self.button_calc = QPushButton("Do the calculation...")
        task_layout.addWidget(self.button_calc)

        # ============================================================
        # СТРАНИЦА 2: вычисления
        # ============================================================
        self.page_calc = QWidget()
        calc_layout = QVBoxLayout(self.page_calc)

        self.calc_title = QLabel("Calculations")
        self.calc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calc_layout.addWidget(self.calc_title)

        # Поле вывода информации
        self.result_box = QPlainTextEdit()
        self.result_box.setReadOnly(True)
        calc_layout.addWidget(self.result_box)

        # Блок кнопок
        button_layout = QHBoxLayout()

        self.button_start = QPushButton("Start")
        button_layout.addWidget(self.button_start)

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setEnabled(False)
        button_layout.addWidget(self.button_cancel)

        self.button_back = QPushButton("← Back")
        button_layout.addWidget(self.button_back)

        calc_layout.addLayout(button_layout)
        calc_layout.addStretch()

        # Добавляем обе страницы в stacked layout
        self.stacked.addWidget(self.page_task)
        self.stacked.addWidget(self.page_calc)

    def setup_signals(self):
        """Подключаем кнопки к методам"""

        self.button_calc.clicked.connect(self.switch_to_calculator)
        self.button_start.clicked.connect(self.start_computation)
        self.button_cancel.clicked.connect(self.cancel_computation)
        self.button_back.clicked.connect(self.switch_to_task)

    def apply_styles(self):
        """Стили приложения"""

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
        """Перейти на страницу условия"""

        # Если вычисление идёт, назад не даём уйти
        if self.thread and self.thread.isRunning():
            return

        self.stacked.setCurrentIndex(0)
        self.statusBar().showMessage("Ready")

    @Slot()
    def switch_to_calculator(self):
        """Перейти на страницу вычислений"""

        self.stacked.setCurrentIndex(1)
        self.statusBar().showMessage("Calculator opened")

    @Slot()
    def start_computation(self):
        """Запуск вычислений"""

        # На всякий случай запрещаем повторный запуск,
        # если поток уже работает
        if self.thread and self.thread.isRunning():
            return

        # Очищаем окно результатов
        self.result_box.clear()

        # Пишем стартовое сообщение
        self.result_box.appendPlainText("Starting calculation...")
        self.result_box.appendPlainText("Searching for the longest Collatz sequence under 1,000,000...")
        self.result_box.appendPlainText("")

        # Блокируем / разблокируем кнопки
        self.button_start.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.button_back.setEnabled(False)

        # Обновляем статус-бар
        self.statusBar().showMessage("Working...")

        # Создаём поток
        self.thread = WorkerThread(limit=1_000_000)

        # Подключаем сигналы worker к методам GUI
        self.thread.worker.progress.connect(self.update_progress)
        self.thread.worker.finished.connect(self.computation_finished)
        self.thread.worker.error.connect(self.computation_error)

        # Когда поток завершится, освобождаем ресурсы
        self.thread.finished.connect(self.thread.deleteLater)

        # Запускаем поток
        self.thread.start()

    @Slot()
    def cancel_computation(self):
        """Отмена вычислений"""

        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.result_box.appendPlainText("Cancellation requested...")
            self.statusBar().showMessage("Cancelling...")

        self.button_cancel.setEnabled(False)

    @Slot(int, int, int)
    def update_progress(self, current, best_start, best_length):
        """Обновление прогресса в интерфейсе"""

        # Считаем приблизительный процент
        percent = (current / 999999) * 100

        # Пишем строку в поле результатов
        self.result_box.appendPlainText(
            f"Checked up to: {current:,} | "
            f"Progress: {percent:.1f}% | "
            f"Best start: {best_start:,} | "
            f"Length: {best_length}"
        )

        # Обновляем статус-бар
        self.statusBar().showMessage(
            f"Working... {percent:.1f}% | best start = {best_start}"
        )

    @Slot(int, int)
    def computation_finished(self, best_start, best_length):
        """Вызывается, когда вычисление завершено"""

        self.result_box.appendPlainText("")
        self.result_box.appendPlainText("Calculation completed.")
        self.result_box.appendPlainText(f"Best starting number: {best_start}")
        self.result_box.appendPlainText(f"Sequence length: {best_length}")

        self.statusBar().showMessage("Done")

        # Возвращаем кнопки в нормальное состояние
        self.button_start.setEnabled(True)
        self.button_cancel.setEnabled(False)
        self.button_back.setEnabled(True)

        # Поток больше не нужен
        self.thread = None

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


# ------------------------------------------------------------
# ТОЧКА ВХОДА
# ------------------------------------------------------------
if __name__ == "__main__":
    # Создаём объект приложения Qt
    app = QApplication(sys.argv)

    # Создаём главное окно
    window = MainWindow()

    # Показываем окно
    window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())
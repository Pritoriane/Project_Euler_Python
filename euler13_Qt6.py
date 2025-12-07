import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QStackedLayout, QPushButton, QPlainTextEdit,
                            QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt, Signal, Slot, QThread, QObject


class MainWindow(QWidget):
    '''Главный класс'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Euler. Task 13')
        self.resize(500, 500)

        self.setup_ui()
        self.setup_pages()
        self.setup_signal()
        self.apply_styles()
        self.numbers()

    #--*--    UI     --*--
    def setup_ui(self):
        """Основной layout + стеки страниц"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stacked = QStackedLayout()
        layout.addLayout(self.stacked)


    def setup_pages(self):
        """Создание страницы"""

        #--*-- Страница  задания --*--
        self.page_task = QWidget()
        p_t = QVBoxLayout(self.page_task)

        self.label = QLabel('Task 13. Large sum.')
        self.label.setObjectName("task_title")
        self.label.setAlignment(Qt.AlignCenter)
        p_t.addWidget(self.label)

        self.label_1 = QLabel('Find the first ten digits of the sum of the following one hundred 50-digit numbers.')
        self.label_1.setObjectName('task_description')
        self.label_1.setAlignment(Qt.AlignCenter)
        p_t.addWidget(self.label_1)

        h_layout = QHBoxLayout()
        h_layout.addStretch()  # Растяжка слева
    
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumWidth(550)
        self.output.setMinimumWidth(520)
        self.output.setMaximumHeight(300)
        self.output.setMinimumHeight(285)
        h_layout.addWidget(self.output)
    
        h_layout.addStretch()  # Растяжка справа
        p_t.addLayout(h_layout)

        p_t.addStretch()

        self.button_calc = QPushButton('do the calculation...')
        p_t.addWidget(self.button_calc)

        self.page_calc = CalculatorPage(parent_window=self)

        self.stacked.addWidget(self.page_task)
        self.stacked.addWidget(self.page_calc)

    def setup_signal(self):
        """Соединяем кнопки с переключением страниц"""
        self.button_calc.clicked.connect(self.switch_to_calculator)

    def apply_styles(self):
        '''Все CSS-стили приложения'''
    
        # --*-- Используем CSS для всех стилей --*--
        self.setStyleSheet("""
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

            QPlainTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-size: 16pt;
                font-style: normal;
                font-weight: normal;
                font-family: Courier;
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
        """)
    
        
    def numbers(self):
        self.numbers  = np.array([37107287533902102798797998220837590246510135740250,
                                46376937677490009712648124896970078050417018260538,
                                74324986199524741059474233309513058123726617309629,
                                91942213363574161572522430563301811072406154908250,
                                23067588207539346171171980310421047513778063246676,
                                89261670696623633820136378418383684178734361726757,
                                28112879812849979408065481931592621691275889832738,
                                44274228917432520321923589422876796487670272189318,
                                47451445736001306439091167216856844588711603153276,
                                70386486105843025439939619828917593665686757934951,
                                62176457141856560629502157223196586755079324193331,
                                64906352462741904929101432445813822663347944758178,
                                92575867718337217661963751590579239728245598838407,
                                58203565325359399008402633568948830189458628227828,
                                80181199384826282014278194139940567587151170094390,
                                35398664372827112653829987240784473053190104293586,
                                86515506006295864861532075273371959191420517255829,
                                71693888707715466499115593487603532921714970056938,
                                54370070576826684624621495650076471787294438377604,
                                53282654108756828443191190634694037855217779295145,
                                36123272525000296071075082563815656710885258350721,
                                45876576172410976447339110607218265236877223636045,
                                17423706905851860660448207621209813287860733969412,
                                81142660418086830619328460811191061556940512689692,
                                51934325451728388641918047049293215058642563049483,
                                62467221648435076201727918039944693004732956340691,
                                15732444386908125794514089057706229429197107928209,
                                55037687525678773091862540744969844508330393682126,
                                18336384825330154686196124348767681297534375946515,
                                80386287592878490201521685554828717201219257766954,
                                78182833757993103614740356856449095527097864797581,
                                16726320100436897842553539920931837441497806860984,
                                48403098129077791799088218795327364475675590848030,
                                87086987551392711854517078544161852424320693150332,
                                59959406895756536782107074926966537676326235447210,
                                69793950679652694742597709739166693763042633987085,
                                41052684708299085211399427365734116182760315001271,
                                65378607361501080857009149939512557028198746004375,
                                35829035317434717326932123578154982629742552737307,
                                94953759765105305946966067683156574377167401875275,
                                88902802571733229619176668713819931811048770190271,
                                25267680276078003013678680992525463401061632866526,
                                36270218540497705585629946580636237993140746255962,
                                24074486908231174977792365466257246923322810917141,
                                91430288197103288597806669760892938638285025333403,
                                34413065578016127815921815005561868836468420090470,
                                23053081172816430487623791969842487255036638784583,
                                11487696932154902810424020138335124462181441773470,
                                63783299490636259666498587618221225225512486764533,
                                67720186971698544312419572409913959008952310058822,
                                95548255300263520781532296796249481641953868218774,
                                76085327132285723110424803456124867697064507995236,
                                37774242535411291684276865538926205024910326572967,
                                23701913275725675285653248258265463092207058596522,
                                29798860272258331913126375147341994889534765745501,
                                18495701454879288984856827726077713721403798879715,
                                38298203783031473527721580348144513491373226651381,
                                34829543829199918180278916522431027392251122869539,
                                40957953066405232632538044100059654939159879593635,
                                29746152185502371307642255121183693803580388584903,
                                41698116222072977186158236678424689157993532961922,
                                62467957194401269043877107275048102390895523597457,
                                23189706772547915061505504953922979530901129967519,
                                86188088225875314529584099251203829009407770775672,
                                11306739708304724483816533873502340845647058077308,
                                82959174767140363198008187129011875491310547126581,
                                97623331044818386269515456334926366572897563400500,
                                42846280183517070527831839425882145521227251250327,
                                55121603546981200581762165212827652751691296897789,
                                32238195734329339946437501907836945765883352399886,
                                75506164965184775180738168837861091527357929701337,
                                62177842752192623401942399639168044983993173312731,
                                32924185707147349566916674687634660915035914677504,
                                99518671430235219628894890102423325116913619626622,
                                73267460800591547471830798392868535206946944540724,
                                76841822524674417161514036427982273348055556214818,
                                97142617910342598647204516893989422179826088076852,
                                87783646182799346313767754307809363333018982642090,
                                10848802521674670883215120185883543223812876952786,
                                71329612474782464538636993009049310363619763878039,
                                62184073572399794223406235393808339651327408011116,
                                66627891981488087797941876876144230030984490851411,
                                60661826293682836764744779239180335110989069790714,
                                85786944089552990653640447425576083659976645795096,
                                66024396409905389607120198219976047599490197230297,
                                64913982680032973156037120041377903785566085089252,
                                16730939319872750275468906903707539413042652315011,
                                94809377245048795150954100921645863754710598436791,
                                78639167021187492431995700641917969777599028300699,
                                15368713711936614952811305876380278410754449733078,
                                40789923115535562561142322423255033685442488917353,
                                44889911501440648020369068063960672322193204149535,
                                41503128880339536053299340368006977710650566631954,
                                81234880673210146739058568557934581403627822703280,
                                82616570773948327592232845941706525094512325230608,
                                22918802058777319719839450180888072429661980811197,
                                77158542502016545090413245809786882778948721859617,
                                72107838435069186155435662884062257473692284509516,
                                20849603980134001723930671666823555245252804609722,
                                53503534226472524250874054075591789781264330331690])
        text = '\n'.join(str(n) for n in self.numbers)
        self.output.setPlainText(text)

    #--*-- Навигация --*--
    @Slot()
    def switch_to_task(self):
        self.stacked.setCurrentIndex(0)

    @Slot()
    def switch_to_calculator(self):
        self.stacked.setCurrentIndex(1)


class CalculatorPage(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle('Big sum')

        self._thread = None
        self._worker = None

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel('Calculation')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.label_inf = QLabel('')
        self.label_inf.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_inf)

        self.result_label = QPlainTextEdit()
        self.result_label.setReadOnly(True)
        layout.addWidget(self.result_label)

        btn_layout = QHBoxLayout()
        self.button_start = QPushButton('Start')
        btn_layout.addWidget(self.button_start)

        self.button_back = QPushButton("← Back")
        btn_layout.addWidget(self.button_back)

        self.button_cancel = QPushButton('Cancel')
        self.button_cancel.setEnabled(False)
        btn_layout.addWidget(self.button_cancel)

        layout.addLayout(btn_layout)

        layout.addStretch()

    def setup_signals(self):
        self.button_start.clicked.connect(self.on_start)
        self.button_back.clicked.connect(self.go_back)
        self.button_cancel.clicked.connect(self.on_cancel)

    def go_back(self):
        self.label_inf.setText('')
        self.result_label.setPlainText('')
        self.parent_window.switch_to_task() 

    def on_start(self):
        self.button_start.setEnabled(False)
        self.button_back.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.result_label.setPlainText('')
        self.label_inf.setText('Working....')

        # Создаём поток и worker
        self._thread = QThread()

        # Создаём Worker и передаём в него массив
        self._worker = Worker(self.parent_window.numbers)
        self._worker.moveToThread(self._thread)

       # Соединяем сигналы и слоты (все соединения thread-safe)
        self._thread.started.connect(self._worker.run)
        self._worker.result_ready.connect(self.on_result)
        self._worker.finished.connect(self.on_finished)
        self._worker.error.connect(self.on_error)

        # Когда поток завершится — чистим объекты (безопасно)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        # Аналогично при ошибке — останавливаем поток
        self._worker.error.connect(self._thread.quit)
        self._worker.error.connect(self._worker.deleteLater)

        # Запускаем поток
        self._thread.start()

    @Slot(object)
    def on_result(self, text):
        """Получаем результат из Worker и обновляем интерфейс. """

        self.result_label.setPlainText(f"First 10 digits:\n{text}")
        self.label_inf.setText('Done')
   
    @Slot()
    def on_finished(self):
        self.label_inf.setText('Finished')
        self.button_cancel.setEnabled(False)
        self.button_start.setEnabled(True)
        self.button_back.setEnabled(True)

    @Slot(str)
    def on_error(self, text):
        QMessageBox.critical(self, 'Worker error', text)
        self.label_inf.setText('Error')
        self.button_cancel.setEnabled(False)
        self.button_start.setEnabled(True)
        self.button_back.setEnabled(True)

    def on_cancel(self):
        # корректно останавливаем worker 
        if self._worker:
            self._worker.stop()
        self.button_cancel.setEnabled(False)
        self.button_start.setEnabled(True)
        self.button_back.setEnabled(False)
                 

class Worker(QObject):
    """
    Worker – объект, который будет работать в отдельном QThread.
    Он НЕ должен наследовать QThread.
    """

    # Сигнал, который вернёт результат обратно в GUI-поток
    result_ready = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, numbers: np.ndarray):
        super().__init__()
        self.numbers = numbers

    try:
        def run(self):
            """Метод, который выполняется в отдельном потоке."""
            total = np.sum(self.numbers)
            first_ten_digits = str(total)[:10]

            self.result_ready.emit(first_ten_digits)
            self.finished.emit()

    except Exception as e:
        # Отправляем текст ошибки в GUI
        self.error.emit(str(e)) #type: ignore
        

#--*-- Запуск приложения --*--
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

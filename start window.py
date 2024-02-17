from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6 import QtCore
from gui import DataVisualizer
from venv3.gui2 import DataVisualizer2
from gisto_gui import DataVisualizer3



class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.okno()


    def okno(self):
        self.setWindowTitle("Стартовый экран ")
        self.setGeometry(100, 100, 499, 499)

        self.image_label= QLabel(self)
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.setStyleSheet("QMainWindow{border-image:url('заднийфон.png');}")



        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width())  //2
        y = (screen_geometry.height() - self.height()) //2
        self.setGeometry(x, y, self.width(), self.height())



        #текст
        self.text = QLabel("Какой график хотите построить ? ")
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.text.setMaximumWidth(500)
        self.text.setStyleSheet("font-size: 20px; ")

        layout = QVBoxLayout(self.centralWidget())
        layout.addWidget(self.text)

        self.centralwidget.setLayout(layout)
        def Singlegrapch():
            data_visualizer = DataVisualizer()
            data_visualizer.exec()

        def Twograph():
            data_visualizer2 = DataVisualizer2()
            data_visualizer2.exec()

        def Gisto():
            data_visualizer3 = DataVisualizer3()
            data_visualizer3.exec()
#кнопки
        button1 = QPushButton('Линейный одиночный', self)
        button1.setGeometry(100,70,300,100)
        button1.setStyleSheet("""
                *{background-color: white;
                color: black; 
                border: 0.5px   solid grey;
                border-radius: 10px;} 
                QPushButton:pressed {background-color: #87CEFA;}
                QPushButton:hover {background-color: #B0C4DE;}
                
                """)
        button1.clicked.connect(Singlegrapch)

        button2 = QPushButton('Линейный двойной', self)
        button2.setGeometry(100,180,300,100)
        button2.setStyleSheet("""
                *{background-color: white;
                color: black; 
                border: 0.5px   solid grey;
                border-radius: 10px;} 
                QPushButton:pressed {background-color: #778899;}
                QPushButton:hover {background-color: #B0C4DE;}
                """)
        button2.clicked.connect(Twograph)

        button3 = QPushButton('Гистограмма', self)
        button3.setGeometry(100,290,300,100)
        button3.setStyleSheet("""
                *{background-color: white;
                color: black; 
                border: 0.5px   solid grey;
                border-radius: 10px;} 
                QPushButton:pressed {background-color: #778899;}
                QPushButton:hover {background-color: #B0C4DE;}

                """)
        button3.clicked.connect(Gisto)



if __name__ == '__main__':
    app = QApplication([])
    window = mainwindow()
    window.show()
    app.exec()
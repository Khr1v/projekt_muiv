from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6 import QtCore
from gui2 import DataVisualizer2
from gisto_gui import DataVisualizer3
from diagram import DataVisualizer4


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
        self.setStyleSheet("QMainWindow{border-image:url('backgroundBIG.png');}")



        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width())  //2
        y = (screen_geometry.height() - self.height()) //2
        self.setGeometry(x, y, self.width(), self.height())



        #текст
        self.text = QLabel("Какой график хотите построить ? ")
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.text.setMaximumWidth(500)
        self.text.setStyleSheet("""font-size: 20px; color: black;  """)

        layout = QVBoxLayout(self.centralWidget())
        layout.addWidget(self.text)

        self.centralwidget.setLayout(layout)
        # def Singlegrapch():
        #     data_visualizer = DataVisualizer()
        #     data_visualizer.exec()

        def Twograph():
            data_visualizer2 = DataVisualizer2()
            data_visualizer2.exec()

        def Gisto():
            data_visualizer3 = DataVisualizer3()
            data_visualizer3.exec()

        def Diagram():
            data_visulizer4 = DataVisualizer4()
            data_visulizer4.exec()
#кнопки
        button1 = QPushButton('Линейный' , self)
        button1.setGeometry(100,70,300,100)
        button1.setStyleSheet("""
                *{background-color: rgba(255, 255, 255, 0);
                color: white; 
                border: 0.5px   solid black;
                border-radius: 10px;} 
                QPushButton:hover {background-color: rgba(152, 232, 250, 0.2);}              
                QPushButton:pressed {background-color: rgba(54, 56, 56, 0.2);}            
                
                """)
        button1.clicked.connect(Twograph)

        button2 = QPushButton('Гистограмма', self)
        button2.setGeometry(100,180,300,100)
        button2.setStyleSheet("""
                *{background-color: rgba(255, 255, 255, 0);
                color: white; 
                border: 0.5px   solid black;
                border-radius: 10px;} 
                QPushButton:hover {background-color: rgba(152, 232, 250, 0.4);}              
                QPushButton:pressed {background-color: rgba(54, 56, 56, 0.2);}
                """)
        button2.clicked.connect(Gisto)

        button3 = QPushButton('Диаграмма', self)
        button3.setGeometry(100,290,300,100)
        button3.setStyleSheet("""
                *{background-color: rgba(255, 255, 255, 0);
                color: white; 
                border: 0.5px   solid black;
                border-radius: 10px;} 
                QPushButton:hover {background-color: rgba(152, 232, 250, 0.3);}              
                QPushButton:pressed {background-color: rgba(54, 56, 56, 0.2);}

                """)
        button3.clicked.connect(Diagram)

        button4 = QPushButton("История графиков ", self)
        button4.setGeometry(150,410,200,60)
        button4.setStyleSheet("""
                *{background-color: rgba(255, 255, 255, 0);
                color: white; 
                border: 0.5px   solid grey;
                border-radius: 10px;} 
                QPushButton:pressed {background-color: rgba(54, 56, 56, 0.3);}
                QPushButton:hover {background-color:rgba(54, 56, 56, 0.5);}

                """)

if __name__ == '__main__':
    app = QApplication([])
    window = mainwindow()
    window.show()
    app.exec()
# РАБОЧАЯ ВЕРСИЯ ДЛЯ ОДНОГО ГРАФИКА

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import *
import pandas as pd
import matplotlib.ticker as  ticker



class DataVisualizer(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = None
        self.grid_enabled = False
        self.line_color = 'k'


    def initUI(self):
        self.setWindowTitle("Линейный одиночный ")
        self.setGeometry(100, 100, 1420, 900)
        # self.setStyleSheet("background-color: black")

        # Кнопки
        button = QPushButton("Построить график", self)
        button.setStyleSheet(""" 
        *{background-color: #B22222;
        color: black;
        margin-left: auto;
        margin-right: auto;
        border-radius: 10px;}
        QPushButton:pressed {background-color: #800000;}""")
        button.setGeometry(500, 750, 220, 100)
        button.clicked.connect(self.plotGraph)

        button2 = QPushButton("Загрузить данные", self)
        button2.setStyleSheet("""
        *{background-color: grey;
        color: black; 
        margin-left: auto;
        margin-right: auto; 
        border-radius: 10px;} 
        QPushButton:pressed {background-color: #404040;}""")
        button2.setGeometry(700, 750, 220, 100)
        button2.clicked.connect(self.loadData)

        button3 = QPushButton("save⇩", self)
        button3.setStyleSheet(""" *{background-color: grey; color: black;}""")
        button3.setGeometry(30,150,48,48)
        # icon = QIcon('save_sign_icon_flat_contrast_sketch_6919593.jpg')     #Исправить сделать так чтоб картинка работала на след стадии
        # button3.setIcon(icon)
        button3.clicked.connect(self.saveData)


        color_button = QPushButton("Выбрать цвет линии", self)
        color_button.setGeometry(1100, 750, 150, 50)
        color_button.clicked.connect(self.chooseColor)

        grid_toggle = QCheckBox("Сетка выкл", self)
        grid_toggle.setGeometry(1300, 130, 100, 50)
        grid_toggle.stateChanged.connect(self.toggleGrid)

        # экран
        self.graphics_view = MatplotlibWidget(self)
        self.graphics_view.setGeometry(90, 40, 1200, 700)


    def toggleGrid(self, state):
            self.graphics_view.toggleGrid(state == Qt.CheckState.Checked)

    def chooseColor(self):
        color = QColorDialog.getColor(initial=QColor(self.line_color), parent=self)
        if color.isValid():
            self.line_color = color.name()


    def plotGraph(self):
        if self.data is not None:
            self.data = self.data.sort_values(by='X')
            x = self.data['X']
            y = self.data['Y']

            self.graphics_view.plot(x, y, line_color=self.line_color)
            print(x, y)

    def loadData(self):
        options = QFileDialog.Option.ReadOnly
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("CSV Files (*.csv);;All Files (*)")
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.csv);;All Files (*)", options=options)

        if file_path:
            self.data = pd.read_csv(file_path)


    def saveData(self):
        options = QFileDialog.Option(QFileDialog.Option.ReadOnly)
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PNG files (*.png);; All Files(*)")
        # file_path, _ = file_dialog.getSaveFileName(self,"PNG files (*.png);; All Files(*)", options=options)
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранить график", "", "PNG files (*.png);;All Files (*)",options=options)

        if file_path:
            self.graphics_view.figure.savefig(file_path, format="png")


    def gridview(self):
        self.grid_enabled = not self.grid_enabled
        self.graphics_view.gridview(self.grid_enabled)


class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        super().__init__(fig)
        self.figure.set_size_inches(20, 30)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def plot(self, x, y, **kwargs):
        line_color = kwargs.get('line_color', 'k')
        self.axes.clear()
        self.axes.plot(x, y, marker = "o", color=line_color)
        self.axes.set_xlabel('X-ось')
        self.axes.set_ylabel('Y-ось')
        self.axes.set_title('Ваш  график')
        # self.axes.legend()

        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(1))
        self.axes.xaxis.set_major_locator(ticker.MultipleLocator(1))


        self.axes.grid(True)
        self.draw()

    def toggleGrid(self, state):
        self.grid_enabled = state
        self.axes.grid(self.grid_enabled)
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataVisualizer()
    window.show()
    sys.exit(app.exec())
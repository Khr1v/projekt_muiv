#гистрограмм

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import *
import pandas as pd
import numpy as np
import matplotlib.ticker as  ticker

class DataVisualizer3(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = None
        self.grid_enabled = False
        self.line_color = 'k'


    def initUI(self):
        self.setWindowTitle("Гистрограмма ")
        self.setGeometry(100, 100, 1420, 900)
        self.setStyleSheet("QDialog{border-image:url('backgroundBIG.png');}")

        # Кнопки
        button = QPushButton("Построить гистограмму", self)
        button.setStyleSheet(""" 
        *{background-color: #B22222;
        color: black;
        margin-left: auto;
        margin-right: auto;
        border-radius: 10px;}
        QPushButton:hover {background-color: #e30e1b;}
        QPushButton:pressed {background-color: #800000;}""")
        button.setGeometry(500, 750, 240, 100)
        button.clicked.connect(self.plotGraph)

        button2 = QPushButton("Загрузить данные", self)
        button2.setStyleSheet("""
        *{background-color: grey;
        color: black; 
        margin-left: auto;
        margin-right: auto; 
        border-radius: 10px;}
        QPushButton:hover {background-color: #B0C4DE;}
        QPushButton:pressed {background-color: #404040;}""")
        button2.setGeometry(700, 750, 220, 100)
        button2.clicked.connect(self.loadData)

        button3 = QPushButton("save⇩", self)
        button3.setStyleSheet("""
                                        *{background-color: #afdef0;
                                        color: black; 
                                        border-radius: 5px;} 
                                        QPushButton:hover {background-color: #B0C4DE;}
                                        QPushButton:pressed {background-color: #404040;}""")
        button3.setGeometry(30, 150, 48, 48)
        button3.clicked.connect(self.saveData)

        # цветная кнопка
        # color_button = QPushButton("Выбрать цвет линии", self)
        # color_button.setGeometry(1100, 750, 150, 50)
        # color_button.clicked.connect(self.chooseColor)


        grid_toggle = QCheckBox("Сетка выкл", self)
        grid_toggle.setGeometry(1300, 130, 100, 50)
        grid_toggle.stateChanged.connect(self.toggleGrid)

        # экран
        self.graphics_view = MatplotlibWidget(self)
        self.graphics_view.setGeometry(90, 40, 1200, 700)


    def toggleGrid(self, state):
            self.graphics_view.toggleGrid(state == Qt.CheckState.Checked)

    # цветная кнопка функция
    # def chooseColor(self):
    #     color = QColorDialog.getColor(initial=QColor(self.line_color), parent=self)
    #     if color.isValid():
    #         self.line_color = color.name()


    def plotGraph(self):
        if self.data is not None:
            # self.data = self.data.sort_values(by= self.data.columns[0])

            perviy = self.data

            xlabel = self.data.columns[0]
            ylabel = self.data.columns[1]

            self.graphics_view.set_labels(xlabel, ylabel)
            self.graphics_view.plot(perviy.iloc[:,0],perviy.iloc[:,1],  line_color=self.line_color)

            print(perviy)


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
        self.xlabel = None
        self.ylabel = None

    def set_labels(self, xlabel, ylabel):
        self.xlabel = xlabel
        self.ylabel = ylabel




    def plot(self, x, y, **kwargs):
        line_color = kwargs.get('line_color', 'k')

        # Установка пределов осей x и y
        max_value_x = np.max(x)
        max_value_y = np.max(y)
        max_value = max(max_value_x, max_value_y)
        bins = np.arange(1, max_value + 2) - 0.5

        self.axes.clear()

        # Построение гистограммы с использованием bar
        self.axes.bar(np.arange(1, len(x) + 1), x, alpha=0.5, color=line_color, edgecolor='black', label=self.xlabel)
        self.axes.bar(np.arange(1, len(y) + 1), y, alpha=0.5, color='blue', edgecolor='black', label=self.ylabel)

        # Установка меток на осях x
        self.axes.set_xticks(np.arange(1, max(len(x), len(y)) + 1))
        self.axes.set_xticklabels(np.arange(1, max(len(x), len(y)) + 1))

        # Установка пределов осей x и y
        self.axes.set_xlim(0.5, max(len(x), len(y)) + 0.5)
        self.axes.set_ylim(0, max(self.axes.get_ylim()[1], max_value))

        # Добавление легенды
        self.axes.legend(loc='upper right')

        self.axes.set_title('Гистограмма данных')
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)

        #
        # if  len(x) > 100 or   len(y) > 100:
        #     self.axes.yaxis.set_major_locator(ticker.MultipleLocator(10))
        # else:
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(1))




        self.axes.grid(True)
        self.draw()

    def toggleGrid(self, state):
        self.grid_enabled = state
        self.axes.grid(self.grid_enabled)
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataVisualizer3()
    window.show()
    sys.exit(app.exec())
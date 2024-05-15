import sys
from PyQt6.QtWidgets import *
import matplotlib.pyplot as plt
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import *
import pandas as pd
import numpy as np
import matplotlib.ticker as  ticker

class DataVisualizer4(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = None

    def initUI(self):
        self.setWindowTitle("Диаграмма ")
        self.setGeometry(100, 100, 1420, 900)

        # Кнопки
        button = QPushButton("Построить Диаграму ", self)
        button.setStyleSheet(""" 
        *{background-color: #B22222;
        color: black;
        margin-left: auto;
        margin-right: auto;
        border-radius: 10px;}
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
        QPushButton:pressed {background-color: #404040;}""")
        button2.setGeometry(700, 750, 220, 100)
        button2.clicked.connect(self.loadData)

        button3 = QPushButton("save⇩", self)
        button3.setStyleSheet(""" *{background-color: grey; color: black;}""")
        button3.setGeometry(30,150,48,48)
        button3.clicked.connect(self.saveData)

        # Поле для ввода названия диаграммы
        self.diagram_name_edit = QLineEdit(self)
        self.diagram_name_edit.setPlaceholderText("Название вашей диаграмы")
        self.diagram_name_edit.setGeometry(300, 750, 200, 30)

        self.graphics_view = MatplotlibWidget(self)
        self.graphics_view.setGeometry(90, 40, 1200, 700)

    def plotGraph(self):
        if self.data is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала загрузите данные!")
            return

        labels = self.data[self.data.columns[0]].tolist()
        sizes = self.data[self.data.columns[1]].tolist()

        diagram_name = self.diagram_name_edit.text()

        # Строим круговую диаграмму
        self.graphics_view.plotGraph(sizes, labels, diagram_name)

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


class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(20, 30))  # Установка желаемых размеров фигуры
        super().__init__(fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def plotGraph(self, data, labels, diagram_name):
        self.axes.clear()
        self.axes.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
        self.axes.axis('equal')  # Сделаем равные пропорции для осей, чтобы круг был кругом
        self.axes.set_title(diagram_name)  # Установка названия диаграммы
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataVisualizer4()
    window.show()
    sys.exit(app.exec())



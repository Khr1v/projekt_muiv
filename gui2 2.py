#РАБОЧАЯ ВЕРСИЯ ДЛЯ ДВУХ ГРАФИКОВ

import sys
from PyQt6.QtWidgets import *
import matplotlib as plt
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import *
import pandas as pd
import matplotlib.ticker as ticker


class DataVisualizer2(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = []
        self.grid_enabled = False
        self.line_colors = ['k', 'k','k']


    def initUI(self):
        self.setWindowTitle("Линейный двойной ")
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
        button3.clicked.connect(self.saveData)

        # цветная кнопка
        color_button = QPushButton("Выбрать цвет линии", self)
        color_button.setStyleSheet("""
                *{background-color: grey;
                color: black; 
                border-radius: 5px;} 
                QPushButton:pressed {background-color: #404040;}""")
        color_button.setGeometry(1100, 750, 150, 30)
        color_button.clicked.connect(self.chooseColor)

        # цветная кнопка 2
        color_button2 = QPushButton("Выбрать цвет линии 2 ", self)
        color_button2.setStyleSheet("""
                        *{background-color: grey;
                        color: black; 
                        border-radius: 5px;} 
                        QPushButton:pressed {background-color: #404040;}""")
        color_button2.setGeometry(1100, 788, 150, 30)
        color_button2.clicked.connect(self.chooseColor2)

        #цветная кнопка 3
        color_button3 = QPushButton("Выбрать цвет линии 3", self)
        color_button3.setStyleSheet("""
                        *{background-color: grey;
                        color: black; 
                        border-radius: 5px;} 
                        QPushButton:pressed {background-color: #404040;}""")
        color_button3.setGeometry(1100, 826, 150, 30)
        color_button3.clicked.connect(self.chooseColor3)

        grid_toggle = QCheckBox("Сетка выкл", self)
        grid_toggle.setGeometry(1300, 130, 100, 50)
        grid_toggle.stateChanged.connect(self.toggleGrid)

        # кнопки для называния линий
        self.name_button1 = QLineEdit(self)
        self.name_button1.setGeometry(200, 746, 100, 20)
        self.name_button1.setPlaceholderText("Ваш график")
        self.send_name_button1 = QPushButton("Отправить", self)
        self.send_name_button1.setGeometry(300, 743, 100, 27)

        self.name_button2 = QLineEdit(self)
        self.name_button2.setGeometry(200, 775, 100, 20)
        self.name_button2.setPlaceholderText("линия 1")
        self.send_name_button2 = QPushButton("Отправить", self)
        self.send_name_button2.setGeometry(300, 772, 100, 27)

        self.name_button3 = QLineEdit(self)
        self.name_button3.setGeometry(200, 795, 100, 20)
        self.name_button3.setPlaceholderText("линия 2")
        self.send_name_button3 = QPushButton("Отправить", self)
        self.send_name_button3.setGeometry(300, 792, 100, 27)

        self.name_button4 = QLineEdit(self)
        self.name_button4.setGeometry(200, 815, 100, 20)
        self.name_button4.setPlaceholderText("линия 3")
        self.send_name_button4 = QPushButton("Отправить", self)
        self.send_name_button4.setGeometry(300, 812, 100, 27)


        # экран
        self.graphics_view = MatplotlibWidget(self)
        self.graphics_view.setGeometry(90, 40, 1200, 700)


    def toggleGrid(self, state):
            self.graphics_view.toggleGrid(state == Qt.CheckState.Checked)

    # цветная кнопка функции
    def chooseColor(self):
        color = QColorDialog.getColor(initial=QColor(self.line_colors[0]), parent=self)
        if color.isValid():
            self.line_colors[0] = color.name()

    def chooseColor2(self):
        if len(self.line_colors) < 1 :
            QMessageBox.warning(self, "Внимание", "На графике только одна линия(")
        else:
            color = QColorDialog.getColor(initial=QColor(self.line_colors[1]), parent=self)
            if color.isValid():
                self.line_colors[1] = color.name()

    def chooseColor3(self):
        print("Длина списка self.line_colors:", len(self.line_colors))

        if len(self.line_colors) == 2:
            QMessageBox.warning(self, "Внимание", "На графике меньше 3 линий(")
        else:
            color = QColorDialog.getColor(initial=QColor(self.line_colors[2]), parent=self)
            if color.isValid():
                self.line_colors[2] = color.name()


    def plotGraph(self):
        if self.data:
            self.graphics_view.axes.clear()
            for i, dataset in enumerate(self.data):
                x_colvo = f'X{i + 1}'
                y_colvo = f'Y{i + 1}'
                dataset.sort_values(by = [x_colvo, y_colvo], inplace=True)
                x_values = dataset[x_colvo]
                y_values = dataset[y_colvo]
                color = self.line_colors[i % len(self.line_colors)]
                self.graphics_view.axes.plot(x_values, y_values, marker="o", color=color)
        self.graphics_view.axes.set_xlabel('X-ось')
        self.graphics_view.axes.set_ylabel('Y-ось')
        self.graphics_view.axes.set_title(self.name_button1.text())
        self.graphics_view.axes.legend([self.name_button2.text(), self.name_button3.text(), self.name_button4.text()], loc="upper right")
        self.graphics_view.axes.yaxis.set_major_locator(ticker.MultipleLocator(1))
        self.graphics_view.axes.xaxis.set_major_locator(ticker.MultipleLocator(1))
        self.graphics_view.axes.grid(True)
        self.graphics_view.draw()


    def loadData(self):
        options = QFileDialog.Option.ReadOnly
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("CSV Files (*.csv);;All Files (*)")
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.csv);;All Files (*)", options=options)

        if file_path:
            try:
                self.data.clear()
                df = pd.read_csv(file_path)
                num_columns = len(df.columns)
                for i in range(0, num_columns, 2):
                    dataset = df.iloc[:, i:i + 2]
                    self.data.append(dataset)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные из файла: {str(e)}")
            print("Загруженные данные:")
            for dataset in self.data:
                print(dataset.head())


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



    def plot(self):

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
    window = DataVisualizer2()
    window.show()
    sys.exit(app.exec())
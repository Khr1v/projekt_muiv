#РАБОЧАЯ ВЕРСИЯ ДЛЯ линейных ГРАФИКОВ

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import *
import pandas as pd
import matplotlib.ticker as ticker
import json


class DataVisualizer2(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = []
        self.grid_enabled = False
        self.line_colors = ['k', 'k','k']


    def initUI(self):
        self.setWindowTitle("Линейный  ")
        self.setGeometry(100, 100, 1420, 900)
        self.setStyleSheet("QDialog{border-image:url('backgroundBIG.png');}")


        # Кнопки
        button = QPushButton("Построить график", self)
        button.setStyleSheet(""" 
        *{background-color: #B22222;
        color: black;
        margin-left: auto;
        margin-right: auto;
        border-radius: 10px;}
        QPushButton:hover {background-color: #e30e1b;}
        QPushButton:pressed {background-color: #800000;}""")
        button.setGeometry(500, 750, 220, 100)
        button.clicked.connect(self.plotGraph)

        button2 = QPushButton("Загрузить данные", self)
        button2.setStyleSheet("""
        *{background-color: #64818f;
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
        button3.setGeometry(30,150,48,48)
        button3.clicked.connect(self.saveData)

        # цветная кнопка
        color_button = QPushButton("Выбрать цвет линии", self)
        color_button.setStyleSheet("""
                *{background-color: #64818f;
                color: black; 
                border-radius: 5px;} 
                QPushButton:hover {background-color: #B0C4DE;}
                QPushButton:pressed {background-color: #404040;}""")
        color_button.setGeometry(1100, 750, 150, 30)
        color_button.clicked.connect(self.chooseColor)

        # цветная кнопка 2
        color_button2 = QPushButton("Выбрать цвет линии 2 ", self)
        color_button2.setStyleSheet("""
                        *{background-color: #64818f;
                        color: black; 
                        border-radius: 5px;} 
                        QPushButton:hover {background-color: #B0C4DE;}
                        QPushButton:pressed {background-color: #404040;}""")
        color_button2.setGeometry(1100, 788, 150, 30)
        color_button2.clicked.connect(self.chooseColor2)

        #цветная кнопка 3
        color_button3 = QPushButton("Выбрать цвет линии 3", self)
        color_button3.setStyleSheet("""
                        *{background-color: #64818f;
                        color: black; 
                        border-radius: 5px;} 
                        QPushButton:hover {background-color: #B0C4DE;}
                        QPushButton:pressed {background-color: #404040;}""")
        color_button3.setGeometry(1100, 826, 150, 30)
        color_button3.clicked.connect(self.chooseColor3)

        grid_toggle = QCheckBox("Сетка выкл", self)
        grid_toggle.setGeometry(1300, 130, 100, 50)
        grid_toggle.setStyleSheet("""*{ color: black} """)
        grid_toggle.stateChanged.connect(self.toggleGrid)

        # кнопки для называния линий
        self.name_button1 = QLineEdit(self)
        self.name_button1.setGeometry(200, 746, 120, 30)
        self.name_button1.setPlaceholderText("Название")
        self.name_button1.setStyleSheet("""*{ background : #2c363b} """)


        self.name_button2 = QLineEdit(self)
        self.name_button2.setGeometry(200, 785, 120, 30)
        self.name_button2.setPlaceholderText("Линия 1")
        self.name_button2.setStyleSheet("""*{ background : #2c363b} """)



        self.name_button3 = QLineEdit(self)
        self.name_button3.setGeometry(200, 815, 120, 30)
        self.name_button3.setPlaceholderText("Линия 2")
        self.name_button3.setStyleSheet("""*{ background : #2c363b} """)



        self.name_button4 = QLineEdit(self)
        self.name_button4.setGeometry(200, 845, 120, 30)
        self.name_button4.setPlaceholderText("Линия 3")
        self.name_button4.setStyleSheet("""*{ background : #2c363b} """)




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
                dataset.columns = ['X', 'Y']  # обновление имена столбцов
                dataset.sort_values(by=['X', 'Y'], inplace=True)  # сортировка по 'X' и 'Y'
                x_values = dataset['X']
                y_values = dataset['Y']
                color = self.line_colors[i % len(self.line_colors)]
                legend = self.name_button2.text() if i == 0 else \
                    self.name_button3.text() if i == 1 else \
                        self.name_button4.text() if i == 2 else ""
                self.graphics_view.axes.plot(x_values, y_values, marker="o", color=color, label=legend)
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
        file_dialog.setNameFilter("CSV Files (*.csv);;JSON Files (*.json);;All Files (*)")
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "",
                                                   "Text Files (*.csv);;JSON Files (*.json);;All Files (*)",
                                                   options=options)

        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.loadCSVData(file_path)
                elif file_path.endswith('.json'):
                    self.loadJSONData(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные из файла: {str(e)}")

    def loadCSVData(self, file_path):
        self.data.clear()
        df = pd.read_csv(file_path)
        num_columns = len(df.columns)
        for i in range(0, num_columns, 2):
            dataset = df.iloc[:, i:i + 2]
            dataset.columns = ['X', 'Y']
            self.data.append(dataset)
        print("Загруженные данные:")
        for dataset in self.data:
            print(dataset.head())


    def loadJSONData(self, file_path):
        with open(file_path, 'r') as f:
            plot_data = json.load(f)

        self.name_button1.setText(plot_data['title'])
        self.data.clear()
        line_count = len(plot_data['lines'])
        print(f"Total number of lines: {line_count}")
        for i in range(line_count):
            x_key = f'X{i + 1}'
            y_key = f'Y{i + 1}'
            x_values = plot_data['lines'][i][x_key]
            y_values = plot_data['lines'][i][y_key]
            color = plot_data['lines'][i]['line_color']
            legend = plot_data['lines'][i]['legend']
            print(f"Line {i + 1}: X = {x_values}, Y = {y_values}, Color = {color}, Legend = {legend}")
            dataset = pd.DataFrame({x_key: x_values, y_key: y_values})
            print(dataset.columns)  # Отладочный вывод
            self.data.append(dataset)
            if i == 0:
                self.name_button2.setText(legend)
            elif i == 1:
                self.name_button3.setText(legend)
            elif i == 2:
                self.name_button4.setText(legend)
            self.line_colors[i] = color  # Обновляем цвета линий
        print("Loaded data:")
        for dataset in self.data:
            print(dataset.head())

    def saveData(self):
        save_options = "PNG Files (*.png);;JSON Files (*.json)"
        save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", "", save_options)
        if save_path:
            if save_path.endswith('.png'):
                self.graphics_view.figure.savefig(save_path, bbox_inches="tight")
            elif save_path.endswith('.json'):
                plot_data = {}
                plot_data['title'] = self.name_button1.text()
                plot_data['lines'] = []
                plot_data['Type'] = ("Line")

                for i, dataset in enumerate(self.data):
                    line_data = {}
                    line_data[f'X{i + 1}'] = dataset['X'].tolist()
                    line_data[f'Y{i + 1}'] = dataset['Y'].tolist()
                    line_data['line_color'] = self.line_colors[i % len(self.line_colors)]
                    legend = self.name_button2.text() if i == 0 else \
                        self.name_button3.text() if i == 1 else \
                            self.name_button4.text() if i == 2 else ""
                    line_data['legend'] = legend
                    plot_data['lines'].append(line_data)
                    # line_data['Type'] =("Line")
                with open(save_path, 'w') as json_file:
                    json.dump(plot_data, json_file, indent=4)


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
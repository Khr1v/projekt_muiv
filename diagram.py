import sys
from PyQt6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import *
import pandas as pd
import json


class DataVisualizer4(QDialog):
    def __init__(self, data = None ):
        super().__init__()
        self.initUI()
        self.data = None
        if data:
            self.loadJSONData(data)
            self.plotGraph()

    def initUI(self):
        self.setWindowTitle("Диаграмма ")
        self.setGeometry(100, 100, 1420, 900)
        self.setStyleSheet("QDialog{border-image:url('backgroundBIG.png');}")


        # Кнопки
        button = QPushButton("Построить Диаграму ", self)
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
        button3.setGeometry(30, 150, 48, 48)
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
        file_dialog.setNameFilter("CSV Files (*.csv);;JSON Files (*.json);;All Files (*)")
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "","CSV Files (*.csv);;JSON Files (*.json);;All Files (*)",options=options)

        if file_path:
             if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
             elif file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    plot_data = json.load(f)
                self.loadJSONData(plot_data)
             self.plotGraph()
    def loadJSONData(self, plot_data):
        # with open(file_path, 'r') as f:
        #     plot_data = json.load(f)

        diagram_name = plot_data['title']
        self.diagram_name_edit.setText(diagram_name)

        labels = []
        sizes = []

        for entry in plot_data['data']:
            labels.append(entry['labels'])
            sizes.append(entry['sizes'])

        self.data = pd.DataFrame({'Label': labels, 'Size': sizes})

    def saveData(self):
        save_options = "PNG Files (*.png);;JSON Files (*.json)"
        directory = "/Users/ivanharitonov/Desktop/plot_data"
        save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", directory, save_options)
        if save_path:
            if save_path.endswith('.png'):
                self.graphics_view.figure.savefig(save_path, bbox_inches="tight")
            elif save_path.endswith('.json'):
                diag_data = {}
                diag_data['title'] = self.diagram_name_edit.text()
                diag_data['data'] = []
                diag_data['Type'] = ("Diagram")

                labels = self.data[self.data.columns[0]].tolist()
                sizes = self.data[self.data.columns[1]].tolist()

                for labels, sizes in zip(labels,sizes):
                    diag_data['data'].append({'labels': labels, 'sizes': sizes})

                with open(save_path, 'w') as json_file:
                    json.dump(diag_data, json_file, indent=4 )



class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(20, 30))
        super().__init__(fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

    def plotGraph(self, data, labels, diagram_name):
        self.axes.clear()
        self.axes.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
        self.axes.axis('equal')  # Сделаем равные пропорции для осей, чтобы круг был кругом
        self.axes.set_title(diagram_name)
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataVisualizer4()
    window.show()
    sys.exit(app.exec())



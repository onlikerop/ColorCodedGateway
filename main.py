from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QWidget, QGridLayout, QRadioButton
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont, QIcon, QPalette
from PyQt6.QtCore import Qt, pyqtSignal, QObject
import sys


class Cell(QWidget):
    def __init__(self, color, free=True, parent=None):
        super().__init__(parent)
        self.color = color
        self.free = free

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawRect(self.rect())


class Gateway(QObject):
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.valueChanged.emit(new_value)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Color Coded Gateway')
        self.setFixedSize(400, 400)

        self.light_theme_color = '#FFFFFF'
        self.dark_theme_color = '#1C1E22'
        self.empty_cell_color = self.light_theme_color  # Изначально используем цвет фона светлой темы

        self.setup_ui()
        self.setup_connections()
        self.toggle_theme()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        input_layout = QHBoxLayout()
        gateway_label = QLabel('Номер шлюза:')
        self.entry = QLineEdit()
        calculate_button = QPushButton('Рассчитать', objectName='calculateButton')
        self.error_label = QLabel()

        input_layout.addWidget(gateway_label)
        input_layout.addWidget(self.entry)
        input_layout.addWidget(calculate_button)

        self.table_layout = QGridLayout()
        self.numeric_layout = QHBoxLayout()
        self.numeric_frame = QWidget()

        self.theme_switch_button = QPushButton('☀')
        self.theme_switch_button.setObjectName('themeSwitchButton')

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(self.theme_switch_button)
        theme_layout.addStretch()

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(self.table_layout)
        main_layout.addWidget(self.numeric_frame)
        main_layout.addLayout(theme_layout)
        main_layout.addStretch()

    def setup_connections(self):
        calculate_button = self.findChild(QPushButton, 'calculateButton')
        if calculate_button:
            calculate_button.clicked.connect(self.calculate_conditional_code)

        self.theme_switch_button.clicked.connect(self.toggle_theme)

    def calculate_conditional_code(self):
        try:
            gateway_number = int(self.entry.text())

            colors = ['#C00000', '#ED7D31', '#FFC000', '#00B050']
            values = [50, 10, 5, 1]

            min_gateway_number = 1
            max_gateway_number = 264
            if gateway_number < min_gateway_number or gateway_number > max_gateway_number:
                raise ValueError(f'Номер шлюза должен быть в диапазоне от {min_gateway_number} до {max_gateway_number}')

            for i in reversed(range(self.table_layout.count())):
                widget = self.table_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            for i in range(4):
                for j in range(4):
                    empty_cell = Cell(self.empty_cell_color)
                    self.table_layout.addWidget(empty_cell, i, j)

            count = 0
            remaining_number = gateway_number

            for j in range(4):
                cells_to_fill = min(remaining_number // values[j], 4)
                for i in range(4):
                    cell = Cell(colors[j], False) if i < cells_to_fill else Cell(self.empty_cell_color)
                    self.table_layout.addWidget(cell, i, j)
                    self.table_layout.setColumnMinimumWidth(j, 80)
                    self.table_layout.setRowMinimumHeight(i, 80)
                    count += 1

                if cells_to_fill == 4:
                    remaining_number -= cells_to_fill * values[j]
                else:
                    remaining_number = remaining_number % values[j]

            self.error_label.setText('')
        except ValueError as ve:
            self.error_label.setText(f'Ошибка: {str(ve)}')

    def toggle_theme(self):
        is_dark_theme = self.theme_switch_button.text() == '☀'
        if is_dark_theme:
            self.setStyleSheet('''
                background-color: {0};
                color: {1};
            '''.format(self.dark_theme_color, self.light_theme_color))
            self.empty_cell_color = self.dark_theme_color
            self.theme_switch_button.setText('🌙')
        else:
            self.setStyleSheet('''
                background-color: {0};
                color: {1};
            '''.format(self.light_theme_color, self.dark_theme_color))
            self.empty_cell_color = self.light_theme_color
            self.theme_switch_button.setText('☀')

        self.update_empty_cell_color()  # Обновляем цвет фона пустых ячеек

    def update_empty_cell_color(self):
        for i in range(self.table_layout.count()):
            widget = self.table_layout.itemAt(i).widget()
            if isinstance(widget, Cell):
                if widget.free:
                    widget.color = self.empty_cell_color
                    widget.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_numeric_layout()

    def update_numeric_layout(self):
        self.numeric_frame.setGeometry(
            self.table_layout.cellRect(0, 0).left(),
            self.table_layout.cellRect(0, 0).top(),
            self.table_layout.cellRect(3, 3).right() - self.table_layout.cellRect(0, 0).left(),
            self.table_layout.cellRect(3, 3).bottom() - self.table_layout.cellRect(0, 0).top()
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)

    font = QFont("Arial", 12)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

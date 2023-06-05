from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from PyQt6.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Отображение порта')
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        input_layout = QHBoxLayout()
        gateway_label = QLabel('Номер шлюза:')
        self.entry = QLineEdit()
        calculate_button = QPushButton('Рассчитать')
        self.error_label = QLabel()

        input_layout.addWidget(gateway_label)
        input_layout.addWidget(self.entry)
        input_layout.addWidget(calculate_button)

        self.table_layout = QGridLayout()
        self.table_widget = QWidget()
        self.numeric_frame = QWidget()
        self.numeric_frame.setStyleSheet('background-color: white')
        self.numeric_frame.setFixedHeight(40)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.table_widget)
        main_layout.addWidget(self.numeric_frame)

        self.table_widget.setLayout(self.table_layout)

        calculate_button.clicked.connect(self.calculate_conditional_code)

    def calculate_conditional_code(self):
        try:
            gateway_number = int(self.entry.text())

            colors = ['red', 'orange', 'yellow', 'green']
            values = [50, 10, 5, 1]

            min_gateway_number = 1
            max_gateway_number = 264
            if gateway_number < min_gateway_number or gateway_number > max_gateway_number:
                raise ValueError(f'Номер шлюза должен быть в диапазоне от {min_gateway_number} до {max_gateway_number}')

            for i in reversed(range(self.table_layout.count())):
                self.table_layout.itemAt(i).widget().setParent(None)

            count = 0
            remaining_number = gateway_number
            for j in range(4):
                column_frame = QWidget()
                column_layout = QVBoxLayout(column_frame)

                cells_to_fill = min(remaining_number // values[j], 4)
                for i in range(cells_to_fill):
                    cell_label = QLabel()
                    cell_label.setStyleSheet(f'background-color: {colors[j]}')
                    cell_label.setMinimumSize(30, 30)  # Set minimum size for color code cells
                    column_layout.addWidget(cell_label)
                    count += 1
                    if count == gateway_number:
                        break

                if cells_to_fill < 4:
                    for _ in range(4 - cells_to_fill):
                        empty_cell_label = QLabel()
                        empty_cell_label.setStyleSheet('background-color: white')
                        column_layout.addWidget(empty_cell_label)

                column_layout.addStretch()
                self.table_layout.addWidget(column_frame, 0, j)

                remaining_number %= values[j]  # Update the remaining number

            numeric_layout = QHBoxLayout()
            for i in range(4):
                numeric_label = QLabel(str(values[i]))
                numeric_layout.addWidget(numeric_label, alignment=Qt.AlignmentFlag.AlignCenter)

            self.numeric_frame.setLayout(numeric_layout)

            self.error_label.setText('')

        except ValueError:
            self.error_label.setText('Ошибка: Некорректный ввод')

        except Exception as e:
            self.error_label.setText(f'Ошибка: {str(e)}')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

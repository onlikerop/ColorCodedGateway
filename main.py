from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QGridLayout, QFrame, QSizePolicy
from PyQt6.QtGui import QPainter, QColor, QBrush, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QObject
import sys
import logging


class Cell(QWidget):
    """
    The Cell class represents a cell widget that will be displayed in the table.

    Attributes:
        color (str): The color of the cell.
        free (bool): Flag indicating whether the cell is free.
    """

    cellClicked = pyqtSignal()

    colors = ['#C00000', '#ED7D31', '#FFC000', '#00B050']
    values = [50, 10, 5, 1]

    def __init__(self, color, position, free=True, parent=None):
        """
        Initialize the Cell object.

        Args:
            color (str): The color of the cell.
            free (bool, optional): Flag indicating whether the cell is free. Defaults to True.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.color = color
        self.free = free
        self.position = position

    def paintEvent(self, event):
        """
        Event handler for painting the cell.

        Args:
            event (QPaintEvent): The paint event.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        self.cellClicked.emit()
        event.accept()

    def getColor(self):
        """
        Getter for the color of the cell.

        Returns:
            str: The current color of the cell.
        """
        return self.color

    def setColor(self, new_value):
        """
        Setter for the color of the cell.

        Args:
            new_value (str): The new color of the cell.
        """
        self.color = new_value
        self.update()

    def getPosition(self, easy=False):
        """
        Getter for the position of the cell.

        Returns:
            list: The current position of the cell.
        """
        return self.position if not easy else [self.position[0] + 1, self.position[1] + 1]

    def setPosition(self, new_value):
        """
        Setter for the position of the cell.

        Args:
            new_value (list): The new position of the cell.
        """
        self.position = new_value
        self.update()

    def isFree(self):
        """
        Getter for the free of the cell.

        Returns:
            bool: The current free of the cell.
        """
        return self.free

    def setFree(self):
        """
        Setter for making cell free.
        """
        self.free = True
        self.update()

    def occupy(self):
        """
        Setter for making cell occupied.
        """
        self.free = False
        self.update()


class Gateway(QObject):
    """
    The Gateway class represents a signal object that serves as a gateway for value transmission.

    Signals:
        valueChanged (int): The signal emitted when the value changes.

    Attributes:
        value (int): The current value of the gateway.
    """

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        """
        Initialize the Gateway object.

        Args:
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(parent)
        self._value = 0

    @property
    def value(self):
        """
        Getter for the value of the gateway.

        Returns:
            int: The current value of the gateway.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        Setter for the value of the gateway.

        Args:
            new_value (int): The new value of the gateway.
        """
        self._value = new_value
        self.valueChanged.emit(new_value)


class MainWindow(QMainWindow):
    """
    The MainWindow class represents the main application window.

    Attributes:
        light_theme_color (str): The color for the light theme.
        dark_theme_color (str): The color for the dark theme.
        empty_cell_color (str): The color of the empty cell.
    """

    def __init__(self):
        """
        Initialize the MainWindow object.
        """
        super().__init__()
        self.setWindowTitle('Color Coded Gateway')

        self.light_theme_color = '#FFFFFF'
        self.dark_theme_color = '#1C1E22'
        self.empty_cell_color = self.light_theme_color
        self.setFixedSize(self.baseSize())

        self.setup_ui()
        self.setup_connections()
        self.toggle_theme()

        logging.basicConfig(filename='gateway.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        self.min_gateway_number = 1
        self.max_gateway_number = 264

    def setup_ui(self):
        """
        Set up the user interface.
        """
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        input_layout = QHBoxLayout()
        gateway_label = QLabel('Gateway Number:')
        self.entry = QSpinBox()
        self.entry.setRange(1, 264)
        self.entry.setValue(1)
        calculate_button = QPushButton('Encode', objectName='calculateButton')
        calculate_port_button = QPushButton('Decode ', objectName='calculatePortButton')
        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet('color: red;')

        input_layout.addWidget(gateway_label)
        input_layout.addWidget(self.entry)
        input_layout.addWidget(calculate_button)
        input_layout.addWidget(calculate_port_button)

        self.table_container = QFrame()
        table_container_layout = QVBoxLayout(self.table_container)
        self.table_container.setMinimumSize(320, 320)
        self.table_container.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        table_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_layout = QGridLayout(self.table_container)
        table_container_layout.addLayout(self.table_layout)

        self.table_layout.setHorizontalSpacing(0)  # Remove horizontal spacing
        self.table_layout.setVerticalSpacing(0)  # Remove vertical spacing

        self.numeric_layout = QHBoxLayout()
        self.numeric_frame = QWidget()

        self.theme_switch_button = QPushButton('☀')
        self.theme_switch_button.setObjectName('themeSwitchButton')
        self.theme_switch_button.setFixedSize(
            self.theme_switch_button.fontMetrics().horizontalAdvance('☀'),
            self.theme_switch_button.fontMetrics().height()
        )
        self.theme_switch_button.setStyleSheet('border: none;')

        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_switch_button)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(theme_layout)
        main_layout.addWidget(self.table_container)
        main_layout.addWidget(self.numeric_frame)
        main_layout.addStretch()
        self.create_table()

    def setup_connections(self):
        """
        Set up signal-slot connections.
        """
        calculate_button = self.findChild(QPushButton, 'calculateButton')
        if calculate_button:
            calculate_button.clicked.connect(self.calculate_conditional_code)

        self.theme_switch_button.clicked.connect(self.toggle_theme)

        # Connect the calculate_port_button to the calculate_port method
        calculate_port_button = self.findChild(QPushButton, 'calculatePortButton')
        if calculate_port_button:
            calculate_port_button.clicked.connect(self.calculate_port)
        for i in range(4):
            for j in range(4):
                cell = self.table_layout.itemAtPosition(i, j).widget()
                if isinstance(cell, Cell):
                    cell.cellClicked.connect(self.toggle_cell_color)

    def create_table(self):
        """
        Create an empty table for the code.
        """
        for i in range(4):
            for j in range(4):
                empty_cell = Cell(self.empty_cell_color, position=[i, j])
                self.table_layout.addWidget(empty_cell, i, j)
            self.table_layout.setColumnMinimumWidth(i, 80)
            self.table_layout.setRowMinimumHeight(i, 80)

    def calculate_conditional_code(self):
        """
        Handle the "Encode" button click event.
        """
        try:
            gateway_number = self.entry.value()

            logging.info(f'Gateway encoding request: {gateway_number}')

            if gateway_number < self.min_gateway_number or gateway_number > self.max_gateway_number:
                raise ValueError(
                    f'Gateway number should be in the range of {self.min_gateway_number} to {self.max_gateway_number}')

            count = 0
            remaining_number = gateway_number

            for j in range(4):
                cells_to_fill = min(remaining_number // Cell.values[j], 4)
                for i in range(4):
                    cell = self.table_layout.itemAtPosition(i, j).widget()
                    if isinstance(cell, Cell):
                        cell.setFree()
                        cell.setColor(self.empty_cell_color)
                    if i < cells_to_fill:
                        if isinstance(cell, Cell):
                            cell.setColor(Cell.colors[j])
                            cell.occupy()
                    count += 1

                if cells_to_fill == 4:
                    remaining_number -= cells_to_fill * Cell.values[j]
                else:
                    remaining_number = remaining_number % Cell.values[j]

            self.error_label.setText('')
        except ValueError as ve:
            self.error_label.setText(f'Error: {str(ve)}')
            logging.error(f'Error occurred: {str(ve)}')

    def calculate_port(self):
        """
        Handle the "Decode" button click event.
        """
        try:
            red_count = 0
            orange_count = 0
            yellow_count = 0
            code = 0

            for j in range(4):
                for i in range(4):
                    cell = self.table_layout.itemAtPosition(i, j)
                    if cell:
                        cell_widget = cell.widget()
                        if isinstance(cell_widget, Cell):
                            if not cell_widget.free:
                                code += Cell.values[j]

                            if i > 0 and not cell_widget.isFree():
                                for k in range(i):
                                    if self.table_layout.itemAtPosition(k, j).widget().isFree():
                                        raise ValueError("Invalid cell marked at {}".format(cell_widget.getPosition(easy=True)))

                            if cell_widget.getColor() == Cell.colors[2]:
                                yellow_count += 1

                            if cell_widget.getColor() == Cell.colors[1]:
                                orange_count += 1

                            if cell_widget.getColor() == Cell.colors[0]:
                                red_count += 1

            if (red_count != 4 or orange_count != 4) and yellow_count > 1:
                raise ValueError("More than one yellow cell with not all red and orange cells are filled")
            if code == 0:
                raise ValueError(
                    f'Gateway number should be in the range of {self.min_gateway_number} to {self.max_gateway_number}')

            logging.info(f'Gateway decoding request: {code}')
            self.entry.setValue(code)
            self.error_label.setText('')
        except Exception as e:
            self.error_label.setText(f'Error: {str(e)}')
            logging.error(f'Error occurred: {str(e)}')

    def toggle_cell_color(self):
        sender = self.sender()
        if isinstance(sender, Cell):
            if sender.isFree():
                column = sender.getPosition()[1]
                color = Cell.colors[column]
                sender.setColor(color)
                sender.occupy()
            else:
                sender.setColor(self.empty_cell_color)
                sender.setFree()
            sender.update()

    def toggle_theme(self):
        """
        Toggle the application theme.
        """
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

        self.update_empty_cell_color()

    def update_empty_cell_color(self):
        """
        Update the color of empty cells.
        """
        for i in range(self.table_layout.count()):
            widget = self.table_layout.itemAt(i).widget()
            if isinstance(widget, Cell):
                if widget.free:
                    widget.color = self.empty_cell_color
                    widget.update()

    def showEvent(self, event):
        """
        Handle the window show event.
        """
        super().showEvent(event)
        logging.info('Application started')

    def resizeEvent(self, event):
        """
        Handle the window resize event.
        """
        super().resizeEvent(event)
        self.update_numeric_layout()

    def update_numeric_layout(self):
        """
        Update the layout of numeric labels.
        """
        first_cell_rect = self.table_layout.cellRect(0, 0)
        last_cell_rect = self.table_layout.cellRect(3, 3)

        numeric_frame_width = last_cell_rect.right() - first_cell_rect.left() + first_cell_rect.width()
        numeric_frame_height = last_cell_rect.bottom() - first_cell_rect.top() + first_cell_rect.height()

        self.numeric_frame.setGeometry(first_cell_rect.left(), first_cell_rect.top(), numeric_frame_width,
                                       numeric_frame_height)

        self.numeric_layout.setContentsMargins(0, 0, 0, 0)
        self.numeric_layout.setSpacing(0)
        self.numeric_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.apply_numeric_style()

    def apply_numeric_style(self):
        numeric_labels = self.numeric_frame.findChildren(QLabel, 'numericLabel')
        for label in numeric_labels:
            label.setFixedSize(
                self.table_layout.columnMinimumWidth(0),
                self.table_layout.rowMinimumHeight(0)
            )
            label.setStyleSheet('''
                background-color: {0};
                color: {1};
                font-weight: bold;
            '''.format(self.empty_cell_color, self.dark_theme_color))

    def closeEvent(self, event):
        """
        Handle the window close event.
        """
        logging.info('Application closed')
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set application icon
    app_icon = QIcon('materials/ico9-alpha.png')
    app.setWindowIcon(app_icon)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

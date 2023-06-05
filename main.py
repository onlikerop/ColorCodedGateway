import tkinter as tk


def calculate_conditional_code():
    try:
        gateway_number = int(entry.get())

        # Создаем список цветов столбцов
        colors = ['red', 'orange', 'yellow', 'green']

        # Создаем список значений столбцов
        values = [50, 10, 5, 1]

        # Проверка на минимально и максимально допустимые номера портов
        min_gateway_number = 1
        max_gateway_number = 264
        if gateway_number < min_gateway_number or gateway_number > max_gateway_number:
            raise ValueError(f'Номер шлюза должен быть в диапазоне от {min_gateway_number} до {max_gateway_number}')

        # Очищаем таблицу перед заполнением
        for cell in table_frame.winfo_children():
            cell.destroy()

        # Заполняем таблицу столбцами согласно условиям
        count = 0  # Счетчик для отслеживания текущего номера шлюза
        for j in range(4):
            column_frame = tk.Frame(table_frame, bg='white', bd=0)
            column_frame.grid(row=0, column=j)

            # Вычисляем количество ячеек, которые нужно заполнить в текущем столбце
            cells_to_fill = min(gateway_number // values[j], 4)
            for i in range(cells_to_fill):
                cell_label = tk.Label(column_frame, bg=colors[j], width=6, height=3)
                cell_label.pack(fill=tk.BOTH)
                count += 1
                if count == gateway_number:
                    break
            if cells_to_fill < 4:  # Добавляем пустые ячейки, если меньше 4 ячеек заполнено
                for _ in range(4 - cells_to_fill):
                    empty_cell_label = tk.Label(column_frame, bg='white', width=6, height=3)
                    empty_cell_label.pack(fill=tk.BOTH)

            if cells_to_fill == 4:  # Переносим остаток в следующий столбец, если максимальное количество ячеек достигнуто
                gateway_number -= cells_to_fill * values[j]
            else:
                gateway_number = gateway_number % values[j]  # Обновляем значение шлюза после заполнения столбца

        # Выводим числовое представление
        numeric_frame = tk.Frame(window, bg='white', bd=0)
        numeric_frame.pack(pady=10)

        for i in range(4):
            numeric_label = tk.Label(numeric_frame, text=str(values[i]), width=6, height=3)
            numeric_label.pack(side=tk.LEFT, padx=10)

        error_label.config(text='')

    except ValueError:
        error_label.config(text='Ошибка: Некорректный ввод номера шлюза')


# Создаем графический интерфейс
window = tk.Tk()
window.title('Условное обозначение по номеру шлюза')

# Рассчитываем размер окна
element_width = 100
element_height = 40
table_width = 4 * element_width
table_height = 4 * element_height

window_width = max(table_width, element_width)
window_height = 4 * (element_height + 10) + table_height

window.geometry(f'{window_width}x{window_height}')
window.resizable(False, False)

# Создаем метку и поле ввода номера шлюза
gateway_label = tk.Label(window, text='Номер шлюза:', width=element_width, height=2)
gateway_label.pack()

entry = tk.Entry(window, width=element_width)
entry.pack()

# Создаем кнопку для расчета
calculate_button = tk.Button(window, text='Рассчитать', command=calculate_conditional_code, width=element_width, height=2)
calculate_button.pack()

# Создаем метку для вывода ошибки
error_label = tk.Label(window, text='', fg='red', width=element_width, height=2)
error_label.pack()

# Создаем фрейм для отображения таблицы
table_frame = tk.Frame(window, bg='white', bd=0)
table_frame.pack(pady=10)

# Запускаем основной цикл программы
window.mainloop()

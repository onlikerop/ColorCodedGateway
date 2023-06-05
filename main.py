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
            column_frame = tk.Frame(table_frame)  # Создаем фрейм для текущего столбца
            column_frame.grid(row=0, column=j)

            # Вычисляем количество ячеек, которые нужно заполнить в текущем столбце
            cells_to_fill = min(gateway_number // values[j], 4)
            for i in range(cells_to_fill):
                cell_label = tk.Label(column_frame, bg=colors[j], width=10, height=2)
                cell_label.pack()
                count += 1
                if count == gateway_number:
                    break
            if cells_to_fill < 4:  # Добавляем пустые ячейки, если меньше 4 ячеек заполнено
                for _ in range(4 - cells_to_fill):
                    empty_cell_label = tk.Label(column_frame, bg='white', width=10, height=2)
                    empty_cell_label.pack()

            if cells_to_fill == 4:  # Переносим остаток в следующий столбец, если максимальное количество ячеек достигнуто
                gateway_number -= cells_to_fill * values[j]
            else:
                gateway_number = gateway_number % values[j]  # Обновляем значение шлюза после заполнения столбца

        # Выводим числовое представление
        numeric_frame = tk.Frame(window)
        numeric_frame.pack()

        for i in range(4):
            numeric_label = tk.Label(numeric_frame, text=str(values[i]), width=20, height=2)
            numeric_label.pack()

    except ValueError:
        error_label.config(text='Ошибка: Некорректный ввод номера шлюза')


# Создаем графический интерфейс
window = tk.Tk()
window.title('Условное обозначение по номеру шлюза')
window.geometry('400x300')
window.resizable(False, False)  # Запрещаем изменение размера окна

# Создаем метку и поле ввода для номера шлюза
gateway_label = tk.Label(window, text='Номер шлюза:', width=20, height=2)
gateway_label.pack()

entry = tk.Entry(window, width=20)
entry.pack()

# Создаем кнопку для расчета
calculate_button = tk.Button(window, text='Рассчитать', command=calculate_conditional_code, width=20, height=2)
calculate_button.pack()

# Создаем метку для вывода ошибки
error_label = tk.Label(window, text='', fg='red')
error_label.pack()

# Создаем фрейм для отображения условного обозначения
table_frame = tk.Frame(window)
table_frame.pack()

# Запускаем основной цикл программы
window.mainloop()
import tkinter as tk


def calculate_conditional_code():
    try:
        gateway_number = int(entry.get())

        # Создаем список цветов столбцов
        colors = ['Red', 'Orange', 'Yellow', 'Green']

        # Создаем список значений столбцов
        values = [50, 10, 5, 1]

        # Проверка на минимально и максимально допустимые номера портов
        min_gateway_number = 1
        max_gateway_number = 264
        if gateway_number < min_gateway_number or gateway_number > max_gateway_number:
            raise ValueError(f'Номер шлюза должен быть в диапазоне от {min_gateway_number} до {max_gateway_number}')

        # Создаем графический интерфейс
        window = tk.Tk()
        window.title('Условное обозначение')

        # Создаем таблицу 4x4
        table_frame = tk.Frame(window)
        table_frame.pack()

        # Заполняем таблицу столбцами согласно условиям
        count = 0  # Счетчик для отслеживания текущего номера шлюза
        for j in range(4):
            # Вычисляем количество ячеек, которые нужно заполнить в текущем столбце
            cells_to_fill = min(gateway_number // values[j], 4)
            for i in range(cells_to_fill):
                cell_label = tk.Label(table_frame, text=colors[j], width=10, height=2, relief='solid')
                cell_label.grid(row=i, column=j)
                count += 1
                if count == gateway_number:
                    break
            if cells_to_fill == 4:  # Переносим остаток в следующий столбец, если максимальное количество ячеек достигнуто
                gateway_number -= cells_to_fill * values[j]
            else:
                gateway_number = gateway_number % values[j]  # Обновляем значение шлюза после заполнения столбца

        # Выводим числовое представление
        numeric_frame = tk.Frame(window)
        numeric_frame.pack()

        for i in range(4):
            numeric_label = tk.Label(numeric_frame, text=colors[i] + ': ' + str(values[i]), width=20, height=2)
            numeric_label.pack()

        window.mainloop()

    except ValueError:
        error_label.config(text='Ошибка: Некорректный ввод номера шлюза')


# Создаем графический интерфейс
window = tk.Tk()
window.title('Условное обозначение')

# Создаем метку и поле ввода для номера шлюза
label = tk.Label(window, text='Введите номер шлюза:')
label.pack()

entry = tk.Entry(window, width=20)
entry.pack()

# Создаем кнопку для расчета условного обозначения
button = tk.Button(window, text='Рассчитать', command=calculate_conditional_code)
button.pack()

# Создаем метку для вывода ошибок
error_label = tk.Label(window, text='', fg='red')
error_label.pack()

window.mainloop()

import pandas as pd
import matplotlib.pyplot as plt

files = [
    {'filename': '1.txt', 'label': 'befor bonding', 'color': 'blue', 'marker': 'o'},
    {'filename': 'after.txt', 'label': 'after bonding', 'color': 'red', 'marker': 's'},
    {'filename': 'night1.txt', 'label': 'night', 'color': 'green', 'marker': '^'},
    #{'filename': 'data4.csv', 'label': 'График 4', 'color': 'orange', 'marker': 'd'},
]
plt.figure(figsize=(10, 6))

for file in files:
    # Чтение данных из файла
    data = pd.read_csv(file['filename'], sep='\s+', header=None)
    second_values = data[1].astype(float)
    third_values = data[2].astype(float)
    # Построение графика
    plt.plot(
    second_values, third_values,
        label=file['label'],
        color=file['color'],
        marker=file['marker'],
        linestyle='-'
    )

# Добавление заголовка и меток осей
plt.title('Сравнительный график из нескольких файлов')
plt.xlabel('Ось X')
plt.ylabel('Ось Y')

# Добавление сетки
plt.grid(True, linestyle='--', alpha=0.5)

# Добавление легенды
plt.legend()

# Показать график
plt.tight_layout()
plt.show()

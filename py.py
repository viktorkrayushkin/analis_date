import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из файла Excel
df = pd.read_excel('200s_5V_2400.xlsx')

# Просмотр первых нескольких строк данных (необязательно)
print(df.head())

# Предположим, что у вас есть столбцы 'X' и 'Y' в вашем файле Excel
x = df['t']
y = df['I']

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='Данные')

# Добавление подписей и заголовка
plt.xlabel('Параметр X')
plt.ylabel('Параметр Y')
plt.title('График зависимости Y от X')
plt.legend()
plt.grid(True)

# Отображение графика
plt.show()

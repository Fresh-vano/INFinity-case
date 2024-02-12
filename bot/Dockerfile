# Используем официальный образ Python
FROM python:3.8

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем зависимости проекта в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы в контейнер
COPY . .

# Определение переменной окружения для токена бота
ENV BOT_TOKEN="6449226644:AAEXsQkSGSjBs8tAlRYyDSgkO5C_8zdVcBo"

# Команда для запуска бота при старте контейнера
CMD ["python", "main.py"]

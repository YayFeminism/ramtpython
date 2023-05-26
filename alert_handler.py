import threading
import datetime

# Список алертов и блокировка для безопасного доступа к нему
_alerts = []
_lock = threading.Lock()

# Функция добавления алерта
def add_alert(message):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d/%m/%Y, %H:%M:%S")
    full_message = f"{formatted_time} - {message}"
    with _lock:
        _alerts.append(full_message)
        with open('alerts.txt', 'a') as f:
            f.write(full_message + "\n")

# Функция получения всех алертов
def get_alerts():
    with _lock:
        return list(_alerts)

import threading

# Список алертов и блокировка для безопасного доступа к нему
_alerts = []
_lock = threading.Lock()

# Функция добавления алерта
def add_alert(message):
    with _lock:
        _alerts.append(message)

# Функция получения всех алертов
def get_alerts():
    with _lock:
        return list(_alerts)

# Функция очистки алертов
def clear_alerts():
    with _lock:
        _alerts.clear()

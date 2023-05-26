import time

# Счетчики вызовов и таймеры
_url_downloads = 0
_create_processes = 0
_last_url_download = 0
_last_create_process = 0

# Константы для проверки времени между вызовами функций
TIME_THRESHOLD = 1  # в секундах

# Функция обратного вызова для обновления статистики вызовов
_update_callback = None

def _update_calls_stats():
    global _update_callback, _url_downloads, _create_processes
    print(f"Вызов _update_callback с аргументами: {_url_downloads}, {_create_processes}")
    if _update_callback:
        _update_callback(_url_downloads, _create_processes)


# Функции проверки вызовов
def check_URLDownloadToFile(url, file_name):
    print(f"check_URLDownloadToFile called with URL {url} and FileName {file_name}")
    global _url_downloads, _last_url_download
    _url_downloads += 1
    current_time = time.time()

    # Атака определена, отправляем алерт
    from alert_handler import add_alert
    print("Sending alert from check_URLDownloadToFile")  # Добавлен вызов print
    add_alert(f"Подозрительная активность: URLDownloadToFile (URL: {url}, File: {file_name})")

    _last_url_download = current_time

    # Обновляем статистику вызовов
    _update_calls_stats()

    return True

def check_CreateProcessA(application_name, command_line):
    print(f"check_CreateProcessA called with ApplicationName {application_name} and CommandLine {command_line}")
    global _create_processes, _last_create_process
    _create_processes += 1
    current_time = time.time()

    # Атака определена, отправляем алерт
    from alert_handler import add_alert
    print("Sending alert from check_CreateProcessA")  # Добавлен вызов print
    add_alert(f"Подозрительная активность: CreateProcessA (Application: {application_name}, Command Line: {command_line})")

    _last_create_process = current_time

    # Обновляем статистику вызовов
    _update_calls_stats()

    return True

# Функции для получения статистики вызовов
def get_url_downloads_count():
    return _url_downloads

def get_create_processes_count():
    return _create_processes

# Функция инициализации диспетчера безопасности
def initialize(update_callback):
    global _update_callback
    _update_callback = update_callback

# Функция завершения работы диспетчера безопасности
def shutdown():
    pass

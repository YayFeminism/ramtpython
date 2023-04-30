import os
import sys

def is_running_as_admin():
    """
    Проверка, запущено ли приложение с привилегиями администратора
    """
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def exit_with_message(message):
    """
    Завершает выполнение программы с выводом сообщения
    """
    print(message)
    sys.exit(1)

def prompt_for_admin_rights():
    """
    Запрашивает повышение привилегий для приложения в случае, если оно не запущено с правами администратора
    """
    if not is_running_as_admin():
        print("Приложение должно быть запущено с правами администратора.")
        if sys.platform == "win32":
            print("Пожалуйста, запустите приложение с правами администратора и повторите попытку.")
        else:
            print("Пожалуйста, используйте 'sudo' для запуска приложения и повторите попытку.")
        sys.exit(1)

import tkinter as tk
from tkinter import messagebox

import detours_wrapper
import security_dispatcher
import alert_handler
import Pyro5.api
import threading

class RASPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RASP Система защиты")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self, text="Система RASP активна", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.info_label = tk.Label(self, text="Статистика вызовов", font=("Arial", 12))
        self.info_label.pack(pady=10)

        self.calls_stats = tk.StringVar()
        self.calls_stats.set("URLDownloadToFile: 0\nCreateProcessA: 0")
        self.stats_label = tk.Label(self, textvariable=self.calls_stats, font=("Arial", 12))
        self.stats_label.pack(pady=10)


    def update_calls_stats(self, url_downloads, create_processes):
        print(f"Вызов update_calls_stats с аргументами: {url_downloads}, {create_processes}")  # Добавлен вызов print
        self.calls_stats.set(f"URLDownloadToFile: {url_downloads}\nCreateProcessA: {create_processes}")

    @Pyro5.api.expose
    def on_update_calls_stats(self, url_downloads, create_processes):
        self.after(0, lambda: self.update_calls_stats(url_downloads, create_processes))


    def start_pyro5_daemon(self):
         with Pyro5.api.Daemon() as daemon:
            uri = daemon.register(self)
            with Pyro5.api.locate_ns() as ns:
                ns.register("rasp_app", uri)
            daemon.requestLoop()

def main():
    # Инициализация модулей
    detours_wrapper.initialize()

    # Запуск GUI
    app = RASPApp()

    # Запуск Pyro5 сервера
    pyro5_daemon_thread = threading.Thread(target=app.start_pyro5_daemon, daemon=True)
    pyro5_daemon_thread.start()

    security_dispatcher.initialize(app.on_update_calls_stats)

    app.mainloop()

    # Очистка ресурсов
    detours_wrapper.shutdown()
    security_dispatcher.shutdown()


if __name__ == "__main__":
    main()

import time
import schedule
import threading

def run_continuously(interval: int = 1) -> threading.Event:
    """Запускает выполнение задач по расписанию в отдельном потоке."""
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run



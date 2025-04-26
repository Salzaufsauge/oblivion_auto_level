import threading
import time

class ThreadHandler:
    def __init__(self):
        self._event = threading.Event()
        self._thread = None
        self._last_toggle_time = 0

    def _worker(self, function, button, delay, key_release_delay=0.1):
        while not self._event.is_set():
            function(button, key_release_delay)
            time.sleep(delay)

    def toggle_thread(self, function, button, delay=0., key_release_delay=0.1):
        if time.time() - self._last_toggle_time < 0.5:
            return
        self._last_toggle_time = time.time()
        if self._thread and self._thread.is_alive():
            print("Stopping thread")
            self._event.set()
            self._thread.join()
        else:
            print("Starting thread")
            self._event.clear()
            self._thread = threading.Thread(target=self._worker, args=(function, button, delay, key_release_delay), daemon=True)
            self._thread.start()

    def stop_thread(self):
        if self._thread and self._thread.is_alive():
            print("Stopping thread")
            self._event.set()
            self._thread.join()

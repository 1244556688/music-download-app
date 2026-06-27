import threading, queue
from downloader import YTDlpDownloader

class DownloadManager:
    def __init__(self):
        self.queue = queue.Queue()
        self.active_downloads, self.tasks_status, self.lock = {}, {}, threading.Lock()

    def add_task(self, url, settings):
        with self.lock:
            if url in self.tasks_status and self.tasks_status[url]["status"] in ["queued", "downloading"]: return False
            self.tasks_status[url] = {"url": url, "title": url[:40] + "...", "status": "queued", "percent": 0, "speed": "0 KB/s", "eta": "N/A", "error": ""}
        self.queue.put({'url': url, 'settings': settings})
        self._start_worker()
        return True

    def _start_worker(self):
        with self.lock:
            if len(self.active_downloads) < 3: threading.Thread(target=self._worker_loop, daemon=True).start()

    def _worker_loop(self):
        while not self.queue.empty():
            try: task = self.queue.get_nowait()
            except queue.Empty: break
            url = task['url']
            downloader = YTDlpDownloader(url, task['settings'], self.tasks_status, url)
            with self.lock: self.active_downloads[url] = downloader
            downloader.start()
            with self.lock:
                if url in self.active_downloads: del self.active_downloads[url]
            self.queue.task_done()

    def cancel_task(self, url):
        with self.lock:
            if url in self.active_downloads: self.active_downloads[url].cancel()
            if url in self.tasks_status: self.tasks_status[url]["status"] = "cancelled"

    def get_all_status(self):
        with self.lock: return list(self.tasks_status.values())

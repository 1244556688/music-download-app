import yt_dlp, sys
from utils import build_ytdlp_options
import config

class YTDlpDownloader:
    def __init__(self, url, settings, status_dict, url_key):
        self.url, self.settings, self.status_dict, self.url_key = url, settings, status_dict, url_key
        self._cancel_requested = False

    def progress_hook(self, d):
        if self._cancel_requested: raise Exception("Cancelled by user")
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%').replace('\x1b[0;94m', '').replace('\x1b[0m', '').strip()
            speed_str = d.get('_speed_str', 'N/A').replace('\x1b[0;32m', '').replace('\x1b[0m', '').strip()
            eta_str = d.get('_eta_str', 'N/A').replace('\x1b[0;33m', '').replace('\x1b[0m', '').strip()
            try: percent = float(percent_str.replace('%', ''))
            except: percent = 0.0
            self.status_dict[self.url_key].update({"status": "downloading", "percent": percent, "speed": speed_str, "eta": eta_str})

    def start(self):
        try:
            ydl_opts = build_ytdlp_options(self.settings, config.get_download_dir())
            ydl_opts['progress_hooks'] = [self.progress_hook]
            self.status_dict[self.url_key]["status"] = "downloading"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                self.status_dict[self.url_key].update({"status": "completed", "title": info.get('title', '未知標題'), "percent": 100})
        except Exception as e:
            self.status_dict[self.url_key].update({"status": "cancelled" if "Cancelled by user" in str(e) else "failed", "error": str(e)})

    def cancel(self): self._cancel_requested = True

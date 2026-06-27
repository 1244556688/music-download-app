import os
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "V3_Downloader")
MODE_OPTIONS = ["影音合併", "只下載影片", "只下載音訊"]
RESOLUTION_OPTIONS = ["BEST", "4320", "2160", "1440", "1080", "720", "480", "360", "240", "144"]
FPS_OPTIONS = ["BEST", "60", "30", "24"]
VIDEO_FORMATS = ["mp4", "mkv", "webm"]
VIDEO_CODECS = ["BEST", "h264", "h265", "vp9", "av1"]
AUDIO_QUALITIES = ["LOSSLESS", "320", "256", "192", "128", "64"]
AUDIO_FORMATS = ["mp3", "aac", "m4a", "opus", "wav", "flac"]

def get_download_dir():
    global DOWNLOAD_DIR
    if not os.path.exists(DOWNLOAD_DIR):
        try: os.makedirs(DOWNLOAD_DIR)
        except: pass
    return DOWNLOAD_DIR

def set_download_dir(new_path):
    global DOWNLOAD_DIR
    if new_path.strip():
        DOWNLOAD_DIR = new_path.strip()
        if not os.path.exists(DOWNLOAD_DIR):
            try: os.makedirs(DOWNLOAD_DIR)
            except: pass

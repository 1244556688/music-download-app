from flask import Flask, render_template, request, jsonify
import config, os, sys, webbrowser
from threading import Timer
from manager import DownloadManager
from utils import check_ffmpeg

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

manager = DownloadManager()

@app.route('/')
def index():
    ffmpeg_status = check_ffmpeg()
    return render_template('index.html', config=config, ffmpeg_status=ffmpeg_status, current_dir=config.get_download_dir())

@app.route('/api/path', methods=['POST'])
def update_path():
    data = request.json
    new_path = data.get('path', '').strip()
    if new_path:
        config.set_download_dir(new_path)
        return jsonify({"success": True, "path": config.get_download_dir()})
    return jsonify({"success": False, "msg": "路徑不可為空"})

@app.route('/api/download', methods=['POST'])
def start_download():
    data = request.json
    url = data.get('url', '').strip()
    if not url: return jsonify({"success": False, "msg": "網址不可為空"})
    settings = {
        "mode": data.get("mode"), "resolution": data.get("resolution"), "fps": data.get("fps"),
        "video_format": data.get("video_format"), "video_codec": data.get("video_codec"),
        "audio_quality": data.get("audio_quality"), "audio_format": data.get("audio_format")
    }
    success = manager.add_task(url, settings)
    return jsonify({"success": success})

@app.route('/api/status', methods=['GET'])
def get_status(): return jsonify(manager.get_all_status())

@app.route('/api/cancel', methods=['POST'])
def cancel_download():
    data = request.json
    manager.cancel_task(data.get('url'))
    return jsonify({"success": True})

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    Timer(1.5, open_browser).start()
    print("=" * 65)
    print("  ⚡ 下載器系統已成功開機！")
    print("  👉 系統會自動幫您開啟網頁控制台頁面。")
    print("  💡 (這個視窗是後台引擎，請勿關閉它，直接將它最小化即可！)")
    print("=" * 65)
    app.run(debug=False, host='0.0.0.0', port=5000)

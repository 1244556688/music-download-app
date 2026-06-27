import os, shutil, sys

def check_ffmpeg():
    if shutil.which("ffmpeg") or os.path.exists("./ffmpeg.exe") or os.path.exists("ffmpeg.exe"):
        return True
    if getattr(sys, 'frozen', False):
        if os.path.exists(os.path.join(sys._MEIPASS, "ffmpeg.exe")):
            return True
    return False

def build_ytdlp_options(settings, output_dir):
    mode, res, fps, v_ext, v_codec, a_qual, a_ext = (
        settings.get("mode"), settings.get("resolution"), settings.get("fps"),
        settings.get("video_format"), settings.get("video_codec"), settings.get("audio_quality"), settings.get("audio_format")
    )
    
    ffmpeg_location = "."
    if getattr(sys, 'frozen', False):
        ffmpeg_location = sys._MEIPASS

    opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'noplaylist': True, 'retries': 3, 'quiet': True, 'no_warnings': True,
        'ffmpeg_location': ffmpeg_location
    }

    if mode == "只下載音訊":
        opts['format'] = 'bestaudio/best'
        postprocessor = {'key': 'FFmpegExtractAudio', 'preferredcodec': a_ext}
        if a_qual != "LOSSLESS": postprocessor['preferredquality'] = a_qual
        opts['postprocessors'] = [postprocessor]
        return opts

    res_str = "" if res == "BEST" else f"[height<={res}]"
    fps_str = "" if fps == "BEST" else f"[fps<={fps}]"
    codec_str = ""
    if v_codec == "h264": codec_str = "[vcodec^=avc]"
    elif v_codec == "h265": codec_str = "[vcodec^=hev]"
    elif v_codec == "vp9": codec_str = "[vcodec^=vp9]"
    elif v_codec == "av1": codec_str = "[vcodec^=av01]"

    format_str = f"bestvideo{res_str}{fps_str}{codec_str}"
    if mode == "只下載影片": opts['format'] = format_str
    else:
        opts['format'] = f"{format_str}+bestaudio/best"
        opts['merge_output_format'] = v_ext
    return opts

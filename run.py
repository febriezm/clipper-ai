import os
import re
import json
import sys
import subprocess
import requests
import shutil
from urllib.parse import urlparse, parse_qs
import argparse
import warnings
warnings.filterwarnings("ignore")

OUTPUT_DIR = "clips"      # Directory where generated clips will be saved
MAX_DURATION = 60         # Maximum duration (in seconds) for each clip
MIN_SCORE = 0.40          # Minimum heatmap intensity score to be considered viral
MAX_CLIPS = 10            # Maximum number of clips to generate per video
MAX_WORKERS = 1           # Number of parallel workers (reserved for future concurrency)
PADDING = 10              # Extra seconds added before and after each detected segment
TOP_HEIGHT = 960          # Height for top section (center content) in split mode
BOTTOM_HEIGHT = 320       # Height for bottom section (facecam) in split mode
USE_SUBTITLE = True       # Enable auto subtitle using Faster-Whisper (4-5x faster)
WHISPER_MODEL = "small"    # Whisper model size: tiny, base, small, medium, large
SUBTITLE_FONT = "Poppins"
SUBTITLE_FONTS_DIR = None
SUBTITLE_LOCATION = "bottom"
OUTPUT_RATIO = "9:16"
RESOLUTION = "720p"
OUT_WIDTH = 720
OUT_HEIGHT = 1280


def set_ratio_preset(preset, resolution=None):
    global OUTPUT_RATIO, RESOLUTION, OUT_WIDTH, OUT_HEIGHT
    OUTPUT_RATIO = preset
    if resolution:
        RESOLUTION = str(resolution).strip().lower()

    res = RESOLUTION
    if preset == "9:16":
        if res == "4k":
            OUT_WIDTH, OUT_HEIGHT = 2160, 3840
        elif res == "1080p":
            OUT_WIDTH, OUT_HEIGHT = 1080, 1920
        else:
            OUT_WIDTH, OUT_HEIGHT = 720, 1280
        return
    if preset == "1:1":
        if res == "4k":
            OUT_WIDTH, OUT_HEIGHT = 2160, 2160
        elif res == "1080p":
            OUT_WIDTH, OUT_HEIGHT = 1080, 1080
        else:
            OUT_WIDTH, OUT_HEIGHT = 720, 720
        return
    if preset == "16:9":
        if res == "4k":
            OUT_WIDTH, OUT_HEIGHT = 3840, 2160
        elif res == "1080p":
            OUT_WIDTH, OUT_HEIGHT = 1920, 1080
        else:
            OUT_WIDTH, OUT_HEIGHT = 1280, 720
        return
    if preset == "original":
        OUT_WIDTH, OUT_HEIGHT = None, None
        return
    raise ValueError(f"Invalid ratio preset: {preset}")

def ffmpeg_tersedia():
    return bool(shutil.which("ffmpeg"))


def get_ytdlp_js_args():
    if shutil.which("node"):
        return ["--js-runtimes", "node"]
    if shutil.which("deno"):
        return ["--js-runtimes", "deno"]
    return []


def coba_masukkan_ffmpeg_ke_path():
    if ffmpeg_tersedia():
        return True

    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        return False

    winget_packages = os.path.join(local_app_data, "Microsoft", "WinGet", "Packages")
    gyan_root = os.path.join(winget_packages, "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe")
    if not os.path.isdir(gyan_root):
        return False

    found_bin_dir = None
    for root, dirs, files in os.walk(gyan_root):
        if "ffmpeg.exe" in files and os.path.basename(root).lower() == "bin":
            found_bin_dir = root
            break

    if not found_bin_dir:
        return False

    os.environ["PATH"] = f"{found_bin_dir};{os.environ.get('PATH', '')}"
    return ffmpeg_tersedia()


def parse_args():
    parser = argparse.ArgumentParser(prog="yt-heatmap-clipper")
    parser.add_argument("--url", help="YouTube URL (watch/shorts/youtu.be)")
    parser.add_argument(
        "--crop",
        choices=["default", "split_left", "split_right"],
        help="Crop mode",
    )
    parser.add_argument(
        "--subtitle",
        choices=["y", "n"],
        help="Enable auto subtitle (y/n)",
    )
    parser.add_argument("--whisper-model", dest="whisper_model", help="Faster-Whisper model")
    parser.add_argument("--subtitle-font", dest="subtitle_font", help="Subtitle font name (e.g., Poppins)")
    parser.add_argument("--subtitle-fontsdir", dest="subtitle_fontsdir", help="Folder containing .ttf/.otf fonts")
    parser.add_argument(
        "--subtitle-location",
        dest="subtitle_location",
        choices=["center", "bottom"],
        help="Subtitle placement: center or bottom",
    )
    parser.add_argument("--ratio", choices=["9:16", "1:1", "16:9", "original"], help="Output ratio preset")
    parser.add_argument("--resolution", choices=["720p", "1080p", "4k"], default="720p", help="Output resolution (720p, 1080p, 4k)")
    parser.add_argument("--check", action="store_true", help="Check dependencies then exit")
    parser.add_argument("--no-update-ytdlp", action="store_true", help="Skip auto-update yt-dlp")
    return parser.parse_args()


def escape_subtitles_filter_path(path):
    abs_path = os.path.abspath(path)
    return abs_path.replace("\\", "/").replace(":", "\\:")


def escape_subtitles_filter_dir(path):
    abs_path = os.path.abspath(path)
    return abs_path.replace("\\", "/").replace(":", "\\:")

def ensure_fonts_available(target_dir=None):
    fonts_dir = target_dir or SUBTITLE_FONTS_DIR or "fonts"
    if not os.path.isdir(fonts_dir):
        return
    for root, dirs, files in os.walk(fonts_dir):
        if os.path.abspath(root) == os.path.abspath(fonts_dir):
            continue
        for f in files:
            if f.lower().endswith((".ttf", ".otf")):
                dst = os.path.join(fonts_dir, f)
                if not os.path.exists(dst):
                    try:
                        shutil.copy2(os.path.join(root, f), dst)
                    except Exception:
                        pass


def build_subtitle_force_style():
    """
    Build subtitle force_style for libass.
    Note: libass evaluates SRT subtitles on a virtual 288p canvas (PlayResY=288)
    and automatically scales it to any video resolution (720p, 1080p, 4K).
    Therefore FontSize must NOT be multiplied by video height, otherwise it double-scales.
    FontSize=11 produces ~3.1% video height and ~75% max width, leaving safe margins
    for Reels, Shorts, and TikTok without ever blocking the speaker's face.
    """
    alignment = "2" if SUBTITLE_LOCATION == "bottom" else "5"
    margin_v = "35" if SUBTITLE_LOCATION == "bottom" else "0"
    return (
        f"FontName={SUBTITLE_FONT},FontSize=11,Bold=1,"
        f"PrimaryColour=&HFFFFFF,OutlineColour=&H000000,"
        f"BorderStyle=1,Outline=2,Shadow=1,"
        f"Alignment={alignment},MarginV={margin_v}"
    )


def build_cover_scale_crop_vf(out_w, out_h):
    ar_expr = f"{out_w}/{out_h}"
    scale = f"scale='if(gte(iw/ih,{ar_expr}),-2,{out_w})':'if(gte(iw/ih,{ar_expr}),{out_h},-2)'"
    crop = f"crop={out_w}:{out_h}:(iw-{out_w})/2:(ih-{out_h})/2"
    return f"{scale},{crop}"


def build_cover_scale_vf(out_w, out_h):
    ar_expr = f"{out_w}/{out_h}"
    scale = f"scale='if(gte(iw/ih,{ar_expr}),-2,{out_w})':'if(gte(iw/ih,{ar_expr}),{out_h},-2)'"
    return scale


def get_split_heights(out_h):
    if not out_h:
        return None, None
    bottom = int(round(out_h * 0.25))
    bottom = max(1, min(bottom, out_h - 1))
    top = max(1, out_h - bottom)
    return top, bottom
def extract_video_id(url):
    """
    Extract the YouTube video ID from a given URL.
    Supports standard YouTube URLs, shortened URLs, and Shorts URLs.
    """
    parsed = urlparse(url)

    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path[1:]

    if parsed.hostname in ("youtube.com", "www.youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

    return None


def get_model_size(model):
    """
    Get the approximate size of a Whisper model.
    """
    sizes = {
        "tiny": "75 MB",
        "base": "142 MB",
        "small": "466 MB",
        "medium": "1.5 GB",
        "large-v1": "2.9 GB",
        "large-v2": "2.9 GB",
        "large-v3": "2.9 GB"
    }
    return sizes.get(model, "unknown size")


def cek_dependensi(install_whisper=False, fatal=True):
    """
    Ensure required dependencies are available.
    Automatically updates yt-dlp and checks FFmpeg availability.
    """
    global WHISPER_MODEL
    args = getattr(cek_dependensi, "_args", None)
    skip_update = bool(getattr(args, "no_update_ytdlp", False)) if args else False

    if not skip_update:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    if install_whisper:
        # Check if faster-whisper package is installed
        try:
            import faster_whisper
            print(f"✅ Faster-Whisper package installed.")
            
            # Check if selected model is cached
            cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
            model_name = f"faster-whisper-{WHISPER_MODEL}"
            
            model_cached = False
            if os.path.exists(cache_dir):
                try:
                    cached_items = os.listdir(cache_dir)
                    model_cached = any(model_name in item.lower() for item in cached_items)
                except Exception:
                    pass
            
            if model_cached:
                print(f"✅ Model '{WHISPER_MODEL}' already cached and ready.\n")
            else:
                print(f"⚠️  Model '{WHISPER_MODEL}' not found in cache.")
                print(f"   📥 Will auto-download ~{get_model_size(WHISPER_MODEL)} on first transcribe.")
                print(f"   ⏱️  Download happens only once, then cached for future use.\n")
                
        except ImportError:
            print("📦 Installing Faster-Whisper package...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "faster-whisper"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ Faster-Whisper package installed successfully.")
            print(f"⚠️  Model '{WHISPER_MODEL}' (~{get_model_size(WHISPER_MODEL)}) will be downloaded on first use.\n")

    coba_masukkan_ffmpeg_ke_path()
    if not ffmpeg_tersedia():
        print("FFmpeg not found. Please install FFmpeg and ensure it is in PATH.")
        if fatal:
            sys.exit(1)
        return False
    return True


def ambil_most_replayed(video_id):
    """
    Fetch and parse YouTube 'Most Replayed' heatmap data.
    Returns a list of high-engagement segments.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    print("Reading YouTube heatmap data...")

    try:
        html = requests.get(url, headers=headers, timeout=20).text
    except Exception:
        return []

    match = re.search(
        r'"markers":\s*(\[.*?\])\s*,\s*"?markersMetadata"?',
        html,
        re.DOTALL
    )

    if not match:
        return []

    try:
        markers = json.loads(match.group(1).replace('\\"', '"'))
    except Exception:
        return []

    results = []

    for marker in markers:
        if "heatMarkerRenderer" in marker:
            marker = marker["heatMarkerRenderer"]

        try:
            score = float(marker.get("intensityScoreNormalized", 0))
            if score >= MIN_SCORE:
                results.append({
                    "start": float(marker["startMillis"]) / 1000,
                    "duration": min(
                        float(marker["durationMillis"]) / 1000,
                        MAX_DURATION
                    ),
                    "score": score
                })
        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def get_duration(video_id):
    """
    Retrieve the total duration of a YouTube video in seconds.
    """
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        *get_ytdlp_js_args(),
        "--get-duration",
        f"https://youtu.be/{video_id}"
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        time_parts = res.stdout.strip().split(":")

        if len(time_parts) == 2:
            return int(time_parts[0]) * 60 + int(time_parts[1])
        if len(time_parts) == 3:
            return (
                int(time_parts[0]) * 3600 +
                int(time_parts[1]) * 60 +
                int(time_parts[2])
            )
    except Exception:
        pass

    return 3600


def build_srt_cues_from_segments(segments, max_words=4, max_chars=26):
    """
    Split Whisper transcription segments into short, punchy subtitle cues (3-5 words each).
    This matches modern short-form video standards (TikTok/Shorts/Reels), ensuring subtitles
    never wrap into giant multi-line walls of text that cover the speaker's face.
    """
    cues = []
    for segment in segments:
        words = getattr(segment, "words", None)
        if words:
            current_words = []
            current_len = 0
            for w in words:
                w_text = (getattr(w, "word", "") or "").strip()
                if not w_text:
                    continue
                w_start = getattr(w, "start", segment.start)
                w_end = getattr(w, "end", segment.end)
                if len(current_words) >= max_words or (current_len + len(w_text) + 1 > max_chars and current_words):
                    cues.append({
                        "start": current_words[0]["start"],
                        "end": current_words[-1]["end"],
                        "text": " ".join(item["text"] for item in current_words)
                    })
                    current_words = [{"text": w_text, "start": w_start, "end": w_end}]
                    current_len = len(w_text)
                else:
                    current_words.append({"text": w_text, "start": w_start, "end": w_end})
                    current_len += len(w_text) + 1
            if current_words:
                cues.append({
                    "start": current_words[0]["start"],
                    "end": current_words[-1]["end"],
                    "text": " ".join(item["text"] for item in current_words)
                })
        else:
            seg_text = (getattr(segment, "text", "") or "").strip()
            if not seg_text:
                continue
            seg_words = seg_text.split()
            seg_duration = max(0.1, segment.end - segment.start)
            time_per_word = seg_duration / max(1, len(seg_words))

            chunk = []
            chunk_len = 0
            chunk_start_idx = 0
            for idx, w_str in enumerate(seg_words):
                if len(chunk) >= max_words or (chunk_len + len(w_str) + 1 > max_chars and chunk):
                    c_start = segment.start + chunk_start_idx * time_per_word
                    c_end = segment.start + idx * time_per_word
                    cues.append({
                        "start": c_start,
                        "end": min(segment.end, c_end),
                        "text": " ".join(chunk)
                    })
                    chunk = [w_str]
                    chunk_len = len(w_str)
                    chunk_start_idx = idx
                else:
                    chunk.append(w_str)
                    chunk_len += len(w_str) + 1
            if chunk:
                c_start = segment.start + chunk_start_idx * time_per_word
                cues.append({
                    "start": c_start,
                    "end": segment.end,
                    "text": " ".join(chunk)
                })
    return cues


def generate_subtitle(video_file, subtitle_file, event_hook=None):
    """
    Generate subtitle file using Faster-Whisper for the given video.
    Returns True if successful, False otherwise.
    """
    from faster_whisper import WhisperModel

    def load_and_transcribe():
        if callable(event_hook):
            try:
                event_hook("stage", {"stage": "subtitle_model_load"})
            except Exception:
                pass
        print(f"  Loading Faster-Whisper model '{WHISPER_MODEL}'...")
        print(f"  (If this is first time, downloading ~{get_model_size(WHISPER_MODEL)}...)")
        model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        print("  ✅ Model loaded. Transcribing audio (4-5x faster than standard Whisper)...")
        if callable(event_hook):
            try:
                event_hook("stage", {"stage": "subtitle_transcribe"})
            except Exception:
                pass
        segments, info = model.transcribe(video_file, language="id", word_timestamps=True)
        return list(segments)

    try:
        segments = load_and_transcribe()
    except Exception as e:
        msg = str(e)
        if os.name == "nt" and "WinError 1314" in msg:
            print(f"  Failed to generate subtitle: {msg}")
            print("  Windows kamu kelihatan tidak mengizinkan symlink (HuggingFace cache).")
            print("  Retrying sekali lagi (biasanya langsung beres setelah fallback cache aktif)...")
            try:
                segments = load_and_transcribe()
            except Exception as e2:
                print(f"  Failed to generate subtitle: {str(e2)}")
                return False
        else:
            print(f"  Failed to generate subtitle: {msg}")
            return False

    if callable(event_hook):
        try:
            event_hook("stage", {"stage": "subtitle_write"})
        except Exception:
            pass
    print("  Generating subtitle file...")
    cues = build_srt_cues_from_segments(segments, max_words=4, max_chars=26)
    with open(subtitle_file, "w", encoding="utf-8") as f:
        for i, cue in enumerate(cues, start=1):
            start_time = format_timestamp(cue["start"])
            end_time = format_timestamp(cue["end"])
            text = cue["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

    return True


def format_timestamp(seconds):
    """
    Convert seconds to SRT timestamp format (HH:MM:SS,mmm)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def download_source_video(video_id, output_path, event_hook=None, resolution=None):
    """
    Download the complete YouTube video natively using yt-dlp at full speed.
    This avoids remote FFmpeg seeking throttling on DASH/HLS streams.
    Supports up to 4K (2160p) resolution when selected.
    """
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1024 * 100:
        return True

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    if callable(event_hook):
        try:
            event_hook("stage", {"stage": "download", "clip_index": 0})
        except Exception:
            pass

    res_choice = (resolution or RESOLUTION or "720p").strip().lower()
    if res_choice == "4k":
        max_h = 2160
    elif res_choice == "1080p":
        max_h = 1080
    else:
        max_h = 720

    print(f"[*] Downloading source video for {video_id} (target resolution up to {max_h}p) via native yt-dlp...")
    js_args = get_ytdlp_js_args()
    cmd = [
        sys.executable, "-m", "yt_dlp",
        *js_args,
        "--force-ipv4",
        "--no-warnings",
        "--quiet",
        "-N", "4",
        "-f", f"bv*[height<={max_h}][ext=mp4][protocol^=http]+ba[ext=m4a][protocol^=http]/bv*[height<={max_h}]+ba/b[height<={max_h}]/bv*+ba/b",
        "--merge-output-format", "mp4",
        "-o", output_path,
        f"https://youtu.be/{video_id}"
    ]

    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0 or not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        cmd_fallback = [
            sys.executable, "-m", "yt_dlp",
            *js_args,
            "--force-ipv4",
            "--no-warnings",
            "--quiet",
            "-N", "4",
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", output_path,
            f"https://youtu.be/{video_id}"
        ]
        res_fb = subprocess.run(cmd_fallback, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if res_fb.returncode != 0 or not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            err = (res_fb.stderr or res.stderr or "Gagal mengunduh video sumber").strip()
            raise RuntimeError(f"Gagal download video sumber: {err}")

    print("[OK] Source video downloaded successfully.")
    return True


def proses_satu_clip(video_id, item, index, total_duration, crop_mode="default", use_subtitle=False, event_hook=None, source_file=None):
    """
    Download/crop and export a single vertical clip
    based on a heatmap segment.
    
    Args:
        crop_mode: "default", "split_left", or "split_right"
        use_subtitle: whether to generate and burn subtitle
        source_file: optional pre-downloaded source video file
    """
    start_original = item["start"]
    end_original = item["start"] + item["duration"]

    start = max(0, start_original - PADDING)
    end = min(end_original + PADDING, total_duration)
    duration = max(1, end - start)

    if duration < 3:
        return False

    cropped_file = os.path.join(OUTPUT_DIR, f"temp_cropped_{index}.mp4")
    subtitle_file = os.path.join(OUTPUT_DIR, f"temp_{index}.srt")
    output_file = os.path.join(OUTPUT_DIR, f"clip_{index}.mp4")

    print(
        f"[Clip {index}] Processing segment "
        f"({int(start)}s - {int(end)}s, duration {int(duration)}s, padding {PADDING}s)"
    )

    created_source = False
    if not source_file or not os.path.exists(source_file):
        source_file = os.path.join(OUTPUT_DIR, f"source_{video_id}.mp4")
        if not os.path.exists(source_file):
            download_source_video(video_id, source_file, event_hook=event_hook)
            created_source = True

    try:
        out_w, out_h = OUT_WIDTH, OUT_HEIGHT
        if crop_mode == "default":
            if OUTPUT_RATIO == "original":
                cmd_crop = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(start), "-t", str(duration),
                    "-i", source_file,
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k",
                    cropped_file
                ]
            else:
                vf = build_cover_scale_crop_vf(out_w, out_h)
                cmd_crop = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(start), "-t", str(duration),
                    "-i", source_file,
                    "-vf", vf,
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k",
                    cropped_file
                ]
        elif crop_mode == "split_left":
            if OUTPUT_RATIO == "original" or not out_w or not out_h or out_h < out_w:
                vf = build_cover_scale_crop_vf(out_w or 720, out_h or 1280) if OUTPUT_RATIO != "original" else None
                cmd_crop = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(start), "-t", str(duration),
                    "-i", source_file,
                    *([] if not vf else ["-vf", vf]),
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k",
                    cropped_file
                ]
            else:
                top_h, bottom_h = get_split_heights(out_h)
                scaled = build_cover_scale_vf(out_w, out_h)
                vf = (
                    f"{scaled}[scaled];"
                    f"[scaled]split=2[s1][s2];"
                    f"[s1]crop={out_w}:{top_h}:(iw-{out_w})/2:(ih-{out_h})/2[top];"
                    f"[s2]crop={out_w}:{bottom_h}:0:ih-{bottom_h}[bottom];"
                    f"[top][bottom]vstack[out]"
                )
                cmd_crop = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(start), "-t", str(duration),
                    "-i", source_file,
                    "-filter_complex", vf,
                    "-map", "[out]", "-map", "0:a?",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k",
                    cropped_file
                ]
        elif crop_mode == "split_right":
            if OUTPUT_RATIO == "original" or not out_w or not out_h or out_h < out_w:
                vf = build_cover_scale_crop_vf(out_w or 720, out_h or 1280) if OUTPUT_RATIO != "original" else None
                cmd_crop = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(start), "-t", str(duration),
                    "-i", source_file,
                    *([] if not vf else ["-vf", vf]),
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k",
                    cropped_file
                ]
            else:
                top_h, bottom_h = get_split_heights(out_h)
                scaled = build_cover_scale_vf(out_w, out_h)
                vf = (
                    f"{scaled}[scaled];"
                    f"[scaled]split=2[s1][s2];"
                    f"[s1]crop={out_w}:{top_h}:(iw-{out_w})/2:(ih-{out_h})/2[top];"
                    f"[s2]crop={out_w}:{bottom_h}:iw-{out_w}:ih-{bottom_h}[bottom];"
                    f"[top][bottom]vstack[out]"
                )
                cmd_crop = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(start), "-t", str(duration),
                    "-i", source_file,
                    "-filter_complex", vf,
                    "-map", "[out]", "-map", "0:a?",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k",
                    cropped_file
                ]

        if callable(event_hook):
            try:
                event_hook("stage", {"stage": "crop", "clip_index": index})
            except Exception:
                pass
        print("  Cropping video...")
        result = subprocess.run(
            cmd_crop,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Generate and burn subtitle if enabled
        if use_subtitle:
            if callable(event_hook):
                try:
                    event_hook("stage", {"stage": "subtitle", "clip_index": index})
                except Exception:
                    pass
            print("  Generating subtitle...")
            if generate_subtitle(cropped_file, subtitle_file, event_hook=event_hook):
                if callable(event_hook):
                    try:
                        event_hook("stage", {"stage": "burn_subtitle", "clip_index": index})
                    except Exception:
                        pass
                print("  Burning subtitle to video...")
                # Get absolute path for subtitle file
                subtitle_path = escape_subtitles_filter_path(subtitle_file)
                fonts_dir = SUBTITLE_FONTS_DIR
                fontsdir_arg = ""
                if fonts_dir and os.path.isdir(fonts_dir):
                    ensure_fonts_available(fonts_dir)
                    fontsdir_arg = f":fontsdir='{escape_subtitles_filter_dir(fonts_dir)}'"
                
                force_style = build_subtitle_force_style()
                cmd_subtitle = [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", cropped_file,
                    "-vf", f"subtitles='{subtitle_path}'{fontsdir_arg}:force_style='{force_style}'",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-c:a", "copy",
                    output_file
                ]
                
                result = subprocess.run(
                    cmd_subtitle,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                transcript_text = ""
                if os.path.exists(subtitle_file):
                    try:
                        with open(subtitle_file, "r", encoding="utf-8") as sf:
                            text_lines = []
                            for line in sf:
                                sline = line.strip()
                                if not sline or sline.isdigit() or "-->" in sline:
                                    continue
                                text_lines.append(sline)
                            transcript_text = " ".join(text_lines)
                    except Exception:
                        pass

                if os.path.exists(cropped_file):
                    os.remove(cropped_file)
                if os.path.exists(subtitle_file):
                    os.remove(subtitle_file)
            else:
                transcript_text = ""
                # If subtitle generation failed, use cropped file as output
                print("  Subtitle generation failed, continuing without subtitle...")
                if callable(event_hook):
                    try:
                        event_hook("stage", {"stage": "finalize", "clip_index": index})
                    except Exception:
                        pass
                if os.path.exists(cropped_file):
                    if os.path.exists(output_file):
                        os.remove(output_file)
                    os.rename(cropped_file, output_file)
        else:
            transcript_text = ""
            # No subtitle, rename cropped file to output
            if callable(event_hook):
                try:
                    event_hook("stage", {"stage": "finalize", "clip_index": index})
                except Exception:
                    pass
            if os.path.exists(cropped_file):
                if os.path.exists(output_file):
                    os.remove(output_file)
                os.rename(cropped_file, output_file)

        # Save metadata for social kit generation (title, caption, hashtags)
        meta_file = os.path.join(OUTPUT_DIR, f"clip_{index}.meta.json")
        try:
            with open(meta_file, "w", encoding="utf-8") as mf:
                json.dump({
                    "clip": f"clip_{index}.mp4",
                    "index": index,
                    "start": start,
                    "end": end,
                    "duration": duration,
                    "transcript": transcript_text
                }, mf, ensure_ascii=False, indent=2)
        except Exception:
            pass

        print("Clip successfully generated.")
        if callable(event_hook):
            try:
                event_hook("stage", {"stage": "done_clip", "clip_index": index})
            except Exception:
                pass
        return True

    except subprocess.CalledProcessError as e:
        for f in [cropped_file, subtitle_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except Exception:
                    pass

        print(f"Failed to generate this clip.")
        print(f"Error details: {e.stderr if e.stderr else e.stdout}")
        return False
    except Exception as e:
        for f in [cropped_file, subtitle_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except Exception:
                    pass

        print(f"Failed to generate this clip.")
        print(f"Error: {str(e)}")
        return False
    finally:
        if created_source and os.path.exists(source_file):
            try:
                os.remove(source_file)
            except Exception:
                pass


def main():
    """
    Main entry point of the application.
    """
    args = parse_args()
    cek_dependensi._args = args

    if args.whisper_model:
        global WHISPER_MODEL
        WHISPER_MODEL = args.whisper_model
    if args.subtitle_font:
        global SUBTITLE_FONT
        SUBTITLE_FONT = args.subtitle_font
    if args.subtitle_fontsdir:
        global SUBTITLE_FONTS_DIR
        SUBTITLE_FONTS_DIR = args.subtitle_fontsdir
    if args.subtitle_location:
        global SUBTITLE_LOCATION
        SUBTITLE_LOCATION = args.subtitle_location
    if args.ratio or args.resolution:
        set_ratio_preset(args.ratio or OUTPUT_RATIO, resolution=args.resolution)

    if args.check:
        cek_dependensi(install_whisper=False)
        print("✅ Basic dependencies OK.")
        return

    coba_masukkan_ffmpeg_ke_path()
    if not ffmpeg_tersedia():
        print("FFmpeg not found. Please install FFmpeg and ensure it is in PATH.")
        return

    crop_mode = args.crop
    crop_desc = None
    if crop_mode:
        crop_desc = {
            "default": "Default center crop",
            "split_left": "Split crop (bottom-left facecam)",
            "split_right": "Split crop (bottom-right facecam)",
        }[crop_mode]

    subtitle_choice = args.subtitle
    if subtitle_choice:
        use_subtitle = subtitle_choice == "y"
    else:
        use_subtitle = None

    link = args.url

    if crop_mode is None or use_subtitle is None or not link:
        print("\n=== Crop Mode ===")
        print("1. Default (center crop)")
        print("2. Split 1 (top: center, bottom: bottom-left (facecam))")
        print("3. Split 2 (top: center, bottom: bottom-right ((facecam))")

        while crop_mode is None:
            choice = input("\nSelect crop mode (1-3): ").strip()
            if choice == "1":
                crop_mode = "default"
                crop_desc = "Default center crop"
                break
            if choice == "2":
                crop_mode = "split_left"
                crop_desc = "Split crop (bottom-left facecam)"
                break
            if choice == "3":
                crop_mode = "split_right"
                crop_desc = "Split crop (bottom-right facecam)"
                break
            print("Invalid choice. Please enter 1, 2, or 3.")

        print(f"Selected: {crop_desc}")

        print("\n=== Auto Subtitle ===")
        print(f"Available model: {WHISPER_MODEL} (~{get_model_size(WHISPER_MODEL)})")
        while use_subtitle is None:
            subtitle_choice = input("Add auto subtitle using Faster-Whisper? (y/n): ").strip().lower()
            if subtitle_choice in ["y", "yes"]:
                use_subtitle = True
            elif subtitle_choice in ["n", "no"]:
                use_subtitle = False
            else:
                print("Invalid choice. Please enter y or n.")

        if use_subtitle:
            print(f"✅ Subtitle enabled (Model: {WHISPER_MODEL}, Bahasa Indonesia)")
        else:
            print("❌ Subtitle disabled")

        print()

        cek_dependensi(install_whisper=use_subtitle)

        if not link:
            link = input("Link YT: ").strip()
    else:
        cek_dependensi(install_whisper=use_subtitle)

    video_id = extract_video_id(link)

    if not video_id:
        print("Invalid YouTube link.")
        return

    heatmap_data = ambil_most_replayed(video_id)

    if not heatmap_data:
        print("No high-engagement segments found.")
        return

    print(f"Found {len(heatmap_data)} high-engagement segments.")

    total_duration = get_duration(video_id)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(
        f"Processing clips with {PADDING}s pre-padding "
        f"and {PADDING}s post-padding."
    )
    print(f"Using crop mode: {crop_desc}")

    source_file = os.path.join(OUTPUT_DIR, f"source_{video_id}.mp4")
    try:
        download_source_video(video_id, source_file, resolution=args.resolution)
    except Exception as e:
        print(f"Error downloading video: {e}")
        return

    success_count = 0

    try:
        for item in heatmap_data:
            if success_count >= MAX_CLIPS:
                break

            if proses_satu_clip(
                video_id,
                item,
                success_count + 1,
                total_duration,
                crop_mode,
                use_subtitle,
                source_file=source_file
            ):
                success_count += 1
    finally:
        if os.path.exists(source_file):
            try:
                os.remove(source_file)
            except Exception:
                pass

    print(
        f"Finished processing. "
        f"{success_count} clip(s) successfully saved to '{OUTPUT_DIR}'."
    )


if __name__ == "__main__":
    main()

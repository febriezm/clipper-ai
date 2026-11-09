import os
import re
import json
import subprocess
import sys
import threading
import time
import uuid
from types import SimpleNamespace

from flask import Flask, jsonify, render_template, request, send_from_directory

import run as core


app = Flask(__name__, static_folder="static", template_folder="templates")

jobs_lock = threading.Lock()
jobs = {}
preview_lock = threading.Lock()
preview_cache = {}


def now_ms():
    return int(time.time() * 1000)


def safe_int(value, default=None):
    try:
        return int(value)
    except Exception:
        return default


def parse_time_to_seconds(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip()
    if not s:
        return None
    if s.isdigit():
        return int(s)
    parts = s.split(":")
    if len(parts) == 2:
        m, sec = parts
        return int(m) * 60 + int(float(sec))
    if len(parts) == 3:
        h, m, sec = parts
        return int(h) * 3600 + int(m) * 60 + int(float(sec))
    return None


def set_job(job_id, **patch):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return
        job.update(patch)


def add_log(job_id, line):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return
        job["logs"].append(line)
        if len(job["logs"]) > 300:
            job["logs"] = job["logs"][-300:]


def generate_clip_social_kit(clip_index, video_title="", uploader="", transcript=""):
    """
    Generate catchy viral titles, engaging caption, and relevant hashtags
    for a YouTube Short / Reel / TikTok clip.
    """
    clean_title = (video_title or "").strip()
    clean_uploader = (uploader or "").strip()
    clean_transcript = (transcript or "").strip()

    # 1. Generate Hashtags
    evergreen_tags = ["#shorts", "#fyp", "#viral", "#trending", "#reels", "#youtubeshorts", "#foryou"]
    tags = list(evergreen_tags)

    if clean_uploader:
        up_tag = re.sub(r"[^a-zA-Z0-9]", "", clean_uploader).lower()
        if up_tag and f"#{up_tag}" not in tags:
            tags.append(f"#{up_tag}")

    if clean_title:
        t_clean = re.sub(r"[^a-zA-Z0-9]", "", clean_title).lower()
        if 4 <= len(t_clean) <= 24 and f"#{t_clean}" not in tags:
            tags.append(f"#{t_clean}")

        words = re.findall(r"[a-zA-Z0-9]+", clean_title.lower())
        stopwords = {
            "yang", "untuk", "dengan", "dari", "pada", "dalam", "video", "youtube",
            "this", "that", "with", "from", "and", "the", "bisa", "akan", "kamu", "saya"
        }
        for w in words:
            if len(w) >= 4 and w not in stopwords:
                tag = f"#{w}"
                if tag not in tags:
                    tags.append(tag)

        title_lower = clean_title.lower()
        if any(k in title_lower for k in ["podcast", "bahlul", "ngobrol", "cerita", "bicara"]):
            tags.extend(["#podcast", "#ngobrol"])
        if any(k in title_lower for k in ["lucu", "ngakak", "komedi", "standup", "lawak", "kocak"]):
            tags.extend(["#lucu", "#ngakak", "#komedi"])
        if any(k in title_lower for k in ["game", "gaming", "mabar", "play"]):
            tags.extend(["#gaming", "#gameplay"])
        if any(k in title_lower for k in ["tutorial", "cara", "tips", "belajar", "coding"]):
            tags.extend(["#tips", "#tutorial", "#edukasi"])

    tags.append("#indonesia")
    seen = set()
    final_tags = [t for t in tags if not (t in seen or seen.add(t))][:15]
    hashtags_str = " ".join(final_tags)

    # 2. Generate Titles (Hooks)
    title_variations = []
    if clean_transcript:
        sentences = re.split(r"[.!?\n]+", clean_transcript)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 8]
        if sentences:
            first_s = sentences[0]
            if len(first_s) > 55:
                first_s = first_s[:52] + "..."
            title_variations.append(f'"{first_s}" 😱')
            title_variations.append(f'"{first_s}" - {clean_uploader or "Momen Seru"} 🔥')

    if clean_title:
        title_variations.append(f"Momen Tak Terduga di {clean_title}! 😱 Part {clip_index}")
        title_variations.append(f"{clean_title} | Momen Paling Pecah! 🔥")
        title_variations.append(f"Gak Nyangka Banget! {clean_title} 💥 Part {clip_index}")
        title_variations.append(f"Wajib Tonton Sampai Habis! {clean_title} 🎬")
    else:
        title_variations.append(f"Momen Viral Paling Seru Part {clip_index} 🔥")
        title_variations.append(f"Tonton Sampai Habis! 😱 Part {clip_index}")

    main_title = title_variations[0] if title_variations else f"Highlight Clip #{clip_index} 🔥"

    # 3. Generate Caption
    caption_lines = []
    if clean_transcript:
        snippet = clean_transcript[:180] + ("..." if len(clean_transcript) > 180 else "")
        caption_lines.append(f'"{snippet}"\n')

    if clean_title:
        caption_lines.append(f"Momen paling rame dari: {clean_title}")
    if clean_uploader:
        caption_lines.append(f"Kreator: {clean_uploader}")

    caption_lines.append("\nKalian setuju gak nih? Tulis pendapat kalian di kolom komentar ya! 👇")
    caption_lines.append("Jangan lupa Like, Share & Follow untuk klip seru berikutnya! ✨")
    caption_str = "\n".join(caption_lines)

    return {
        "title": main_title,
        "title_variations": title_variations,
        "caption": caption_str,
        "hashtags": hashtags_str
    }


def list_outputs(job_dir, video_preview=None):
    if not os.path.isdir(job_dir):
        return []
    items = []
    video_title = (video_preview or {}).get("title", "")
    uploader = (video_preview or {}).get("uploader", "")
    for name in os.listdir(job_dir):
        path = os.path.join(job_dir, name)
        if (
            os.path.isfile(path)
            and name.lower().endswith(".mp4")
            and not name.startswith("temp_")
            and not name.startswith("source_")
        ):
            base_name = os.path.splitext(name)[0]
            idx_match = re.search(r"\d+", base_name)
            clip_idx = int(idx_match.group()) if idx_match else len(items) + 1
            meta_path = os.path.join(job_dir, f"{base_name}.meta.json")
            meta = {}
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as mf:
                        meta = json.load(mf)
                except Exception:
                    pass

            if not meta.get("title") or not meta.get("caption") or not meta.get("hashtags"):
                kit = generate_clip_social_kit(clip_idx, video_title, uploader, meta.get("transcript", ""))
                meta.update(kit)
                try:
                    with open(meta_path, "w", encoding="utf-8") as mf:
                        json.dump(meta, mf, ensure_ascii=False, indent=2)
                except Exception:
                    pass

            items.append({
                "name": name,
                "size": os.path.getsize(path),
                "title": meta.get("title", f"Clip #{clip_idx}"),
                "title_variations": meta.get("title_variations", []),
                "caption": meta.get("caption", ""),
                "hashtags": meta.get("hashtags", ""),
                "transcript": meta.get("transcript", "")
            })
    items.sort(key=lambda x: x["name"])
    return items


def run_job(job_id, payload):
    started = now_ms()
    try:
        set_job(job_id, status="running", started_at=started)

        url = (payload.get("url") or "").strip()
        if not url:
            raise ValueError("URL kosong")

        crop = payload.get("crop") or "default"
        ratio = payload.get("ratio") or "9:16"
        resolution = payload.get("resolution") or "720p"
        subtitle = bool(payload.get("subtitle"))
        whisper_model = payload.get("whisper_model") or "small"
        subtitle_font = payload.get("subtitle_font") or "Poppins"
        subtitle_location = payload.get("subtitle_location") or "bottom"
        subtitle_fontsdir = payload.get("subtitle_fontsdir") or None
        if not subtitle_fontsdir and os.path.isdir("fonts"):
            subtitle_fontsdir = "fonts"
        padding = safe_int(payload.get("padding"), 10)
        max_clips = safe_int(payload.get("max_clips"), 10)
        mode = payload.get("mode") or "heatmap"
        set_job(job_id, subtitle_enabled=subtitle)

        core.WHISPER_MODEL = whisper_model
        core.SUBTITLE_FONT = subtitle_font
        core.SUBTITLE_FONTS_DIR = subtitle_fontsdir
        core.SUBTITLE_LOCATION = subtitle_location
        core.PADDING = max(0, padding if padding is not None else 10)
        core.set_ratio_preset(ratio, resolution=resolution)

        job_dir = os.path.join("clips", job_id)
        os.makedirs(job_dir, exist_ok=True)
        core.OUTPUT_DIR = job_dir

        core.cek_dependensi._args = SimpleNamespace(no_update_ytdlp=True)
        ok = core.cek_dependensi(install_whisper=subtitle, fatal=False)
        if not ok:
            raise RuntimeError("FFmpeg tidak ketemu")

        video_id = core.extract_video_id(url)
        if not video_id:
            raise ValueError("URL YouTube invalid")

        total_duration = core.get_duration(video_id)
        try:
            video_preview = get_preview(url)
        except Exception:
            video_preview = {}
        set_job(job_id, preview=video_preview)

        targets = []
        picked = payload.get("segments")
        if isinstance(picked, list) and len(picked) > 0:
            add_log(job_id, f"Pakai {len(picked)} segment yang dipilih...")
            for seg in picked:
                try:
                    start = float(seg.get("start"))
                    dur = float(seg.get("duration"))
                    score = float(seg.get("score", 1.0))
                except Exception:
                    continue
                if dur <= 0:
                    continue
                targets.append({"start": start, "duration": dur, "score": score})
            if not targets:
                raise ValueError("Segment pilihan invalid")
        elif mode == "custom":
            start_s = parse_time_to_seconds(payload.get("start"))
            end_s = parse_time_to_seconds(payload.get("end"))
            if start_s is None or end_s is None:
                raise ValueError("Start/End belum diisi")
            if end_s <= start_s:
                raise ValueError("End harus lebih besar dari Start")
            targets = [{"start": float(start_s), "duration": float(end_s - start_s), "score": 1.0}]
        else:
            add_log(job_id, "Scan heatmap...")
            segments = core.ambil_most_replayed(video_id)
            if not segments:
                raise RuntimeError("Tidak ada heatmap/Most Replayed data")
            targets = segments[: max(1, max_clips or 10)]

        set_job(job_id, total=len(targets), done=0, status_text="processing")

        def event_hook(kind, data):
            if kind != "stage" or not isinstance(data, dict):
                return
            stage = data.get("stage") or ""
            clip_index = safe_int(data.get("clip_index"), 0) or 0
            set_job(job_id, stage=stage, stage_at=now_ms(), stage_clip=clip_index)

        source_file = os.path.join(job_dir, f"source_{video_id}.mp4")
        set_job(job_id, stage="download", status_text=f"mengunduh video sumber ({resolution})...")
        add_log(job_id, f"Mengunduh video sumber (target resolusi {resolution}) via native yt-dlp...")
        core.download_source_video(video_id, source_file, event_hook=event_hook, resolution=resolution)
        add_log(job_id, "Video sumber berhasil diunduh. Mulai memotong klip...")

        success = 0
        try:
            for idx, item in enumerate(targets, start=1):
                set_job(job_id, current=idx, status_text=f"clip {idx}/{len(targets)}")
                ok = core.proses_satu_clip(
                    video_id, item, idx, total_duration, crop, subtitle,
                    event_hook=event_hook, source_file=source_file
                )
                if ok:
                    success += 1
                set_job(job_id, done=idx, success=success, outputs=list_outputs(job_dir, video_preview=video_preview))
        finally:
            if os.path.exists(source_file):
                try:
                    os.remove(source_file)
                except Exception:
                    pass

        set_job(job_id, status="done", finished_at=now_ms(), outputs=list_outputs(job_dir, video_preview=video_preview))
    except Exception as e:
        set_job(job_id, status="error", error=str(e), finished_at=now_ms())


@app.get("/")
def index():
    return render_template("index.html")

@app.get("/assets/fonts/<path:filename>")
def serve_font(filename):
    return send_from_directory("fonts", filename, as_attachment=False)


def get_preview(url):
    key = url.strip()
    if not key:
        raise ValueError("URL kosong")

    with preview_lock:
        cached = preview_cache.get(key)
        if cached:
            return cached

    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        *core.get_ytdlp_js_args(),
        "--skip-download",
        "-J",
        key,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError((res.stderr or res.stdout or "Gagal ambil metadata").strip())

    raw = json.loads(res.stdout)
    item = raw["entries"][0] if isinstance(raw, dict) and "entries" in raw and raw.get("entries") else raw

    preview = {
        "title": item.get("title"),
        "thumbnail": item.get("thumbnail"),
        "uploader": item.get("uploader"),
        "duration": item.get("duration"),
        "webpage_url": item.get("webpage_url") or key,
        "id": item.get("id"),
    }

    with preview_lock:
        preview_cache[key] = preview
        if len(preview_cache) > 200:
            preview_cache.clear()

    return preview


@app.post("/api/preview")
def api_preview():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    try:
        preview = get_preview(url)
        return jsonify({"ok": True, "preview": preview})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.post("/api/scan")
def api_scan():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    video_id = core.extract_video_id(url)
    if not video_id:
        return jsonify({"ok": False, "error": "URL YouTube invalid"}), 400

    core.cek_dependensi._args = SimpleNamespace(no_update_ytdlp=True)
    ok = core.cek_dependensi(install_whisper=False, fatal=False)
    if not ok:
        return jsonify({"ok": False, "error": "FFmpeg tidak ketemu"}), 400

    segments = core.ambil_most_replayed(video_id)
    total = core.get_duration(video_id)
    return jsonify({"ok": True, "video_id": video_id, "duration": total, "segments": segments})


@app.post("/api/clip")
def api_clip():
    payload = request.get_json(silent=True) or {}
    job_id = uuid.uuid4().hex[:12]
    with jobs_lock:
        jobs[job_id] = {
            "id": job_id,
            "status": "queued",
            "created_at": now_ms(),
            "started_at": None,
            "finished_at": None,
            "error": None,
            "total": 0,
            "done": 0,
            "success": 0,
            "current": 0,
            "status_text": "",
            "stage": "",
            "stage_at": None,
            "stage_clip": 0,
            "subtitle_enabled": False,
            "outputs": [],
            "logs": [],
        }

    t = threading.Thread(target=run_job, args=(job_id, payload), daemon=True)
    t.start()
    return jsonify({"ok": True, "job_id": job_id})


@app.get("/api/job/<job_id>")
def api_job(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return jsonify({"ok": False, "error": "Job not found"}), 404
        return jsonify({"ok": True, "job": job})


@app.get("/clips/<job_id>/<path:filename>")
def serve_clip(job_id, filename):
    job_dir = os.path.join("clips", job_id)
    return send_from_directory(job_dir, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

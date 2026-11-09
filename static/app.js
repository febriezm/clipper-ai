const $ = (id) => document.getElementById(id);

const I18N = {
  id: {
    "top.tagline": "Scan Most Replayed, potong otomatis, subtitle rapi.",
    "label.url": "YouTube URL",
    "ph.url": "https://www.youtube.com/watch?v=...",
    "help.url": "Tempel link video/shorts. Nanti keluar preview.",
    "label.mode": "Mode",
    "opt.mode.heatmap": "Scan heatmap (Most Replayed)",
    "opt.mode.custom": "Custom start/end (manual)",
    "help.mode": "Scan = cari momen paling rame. Custom = potong dari waktu yang kamu tentuin.",
    "label.ratio": "Ratio",
    "opt.ratio.9_16": "9:16 (Shorts)",
    "opt.ratio.original": "Original",
    "help.ratio": "Pilih bentuk output video. 9:16 buat Shorts/Reels/TikTok.",
    "label.resolution": "Resolusi",
    "help.resolution": "Kualitas video output (720p, 1080p, atau 4K).",
    "label.crop": "Crop",
    "opt.crop.default": "Default",
    "opt.crop.split_left": "Split Left",
    "opt.crop.split_right": "Split Right",
    "help.crop": "Split itu buat gaming: atas gameplay, bawah facecam.",
    "label.padding": "Padding (detik)",
    "help.padding": "Nambah detik sebelum & sesudah momen biar nggak “kepotong nanggung”.",
    "label.max_clips": "Max clips",
    "help.max_clips": "Berapa potongan yang mau dihasilkan dari heatmap.",
    "label.subtitle": "Subtitle",
    "opt.no": "No",
    "opt.yes": "Yes",
    "help.subtitle": "Kalau Yes, audio ditranskrip jadi teks lalu dibakar ke video.",
    "label.whisper_model": "Model (Whisper)",
    "help.whisper_model": "Ini model AI buat transkripsi suara ke teks. Makin besar makin akurat, makin berat.",
    "label.subtitle_font": "Font Subtitle",
    "opt.custom": "Custom…",
    "ph.subtitle_font_custom": "Nama font custom (mis. Poppins)",
    "help.subtitle_font": "Kalau font-nya ada di folder fonts, isi Fonts dir = fonts.",
    "label.subtitle_location": "Subtitle Location",
    "opt.subtitle_location.bottom": "Bottom",
    "opt.subtitle_location.center": "Centered",
    "help.subtitle_location": "Bottom = lebih natural buat Shorts. Centered = lebih “in your face”.",
    "label.subtitle_fontsdir": "Fonts dir (opsional)",
    "help.subtitle_fontsdir": "Folder berisi file .ttf/.otf buat subtitle. Default: folder project <b>fonts</b>.",
    "label.start": "Start (detik atau mm:ss)",
    "ph.start": "689 atau 11:29",
    "label.end": "End (detik atau mm:ss)",
    "ph.end": "742 atau 12:22",
    "btn.scan": "Scan Heatmap",
    "btn.clip": "Buat Clip",
    "help.actions": "Scan Heatmap = ambil daftar momen “Most Replayed”. Buat Clip = download + crop + (opsional) subtitle.",
    "panel.segments": "Segments",
    "btn.select_all": "Select All",
    "btn.clear": "Clear",
    "btn.create_selected": "Create Selected Clip",
    "panel.progress": "Progress",
    "js.modal.preview_segment": "Preview Segment",
    "js.modal.preview_clip": "Preview Clip",
    "js.modal.open_yt": "Buka di YouTube",
    "js.modal.unmute_hint": "🔊 Video otomatis dibisukan oleh browser (unmute di kontrol player).",
    "js.segments.empty": "Belum ada segment. Klik Scan Heatmap dulu.",
    "js.preview.loading": "Loading preview…",
    "js.progress.count": "{done}/{total} selesai • {success} sukses",
    "js.selected.count": "{count} dipilih",
    "js.stage.download": "Download",
    "js.stage.crop": "Crop",
    "js.stage.subtitle": "Subtitle",
    "js.stage.subtitle_model_load": "Load model",
    "js.stage.subtitle_transcribe": "Transcribe",
    "js.stage.subtitle_write": "Tulis subtitle",
    "js.stage.burn_subtitle": "Burn subtitle",
    "js.stage.finalize": "Finalize",
    "js.stage.done_clip": "Selesai",
    "js.topprogress.processing": "Processing",
    "js.form.title": "📌 Judul Video (Title)",
    "js.form.caption": "📝 Caption / Deskripsi",
    "js.form.hashtags": "# Hashtag Rekomendasi",
    "js.form.copy_title": "📋 Salin Judul",
    "js.form.copy_caption": "📋 Salin Caption",
    "js.form.copy_hashtags": "📋 Salin #",
    "js.form.copy_all": "📋 Salin Lengkap (Judul + Caption + #)",
    "js.form.var_title": "🔄 Variasi Judul Lain",
    "js.form.copied": "✅ Berhasil disalin!",
    "js.loading.title": "Sedang Membuat Klip Video...",
    "js.loading.subtitle": "Memproses video dengan resolusi tinggi & subtitle AI",
    "js.loading.warn_title": "JANGAN TUTUP ATAU REFRESH HALAMAN",
    "js.loading.warn_desc": "Proses rendering video sedang berlangsung. Menutup atau me-refresh halaman ini akan membatalkan klip yang sedang diproses.",
    "js.loading.complete": "Semua klip berhasil dibuat!",
    "js.loading.failed": "Terjadi kendala saat memproses klip.",
    "label.auto_tiktok": "🎵 Otomatis arahkan ke TikTok Upload setelah klip selesai",
    "btn.tiktok_upload": "🎵 Upload ke TikTok",
    "js.scan.loading_title": "Memindai Heatmap YouTube...",
    "js.scan.loading_desc": "Menganalisis kurva Most Replayed untuk menemukan momen viral dengan retensi penonton tertinggi...",
    "js.scan.scanning_btn": "Memindai Heatmap...",
    "js.tiktok.toast_title": "🚀 Klip Siap Di-upload ke TikTok!",
    "js.tiktok.toast_desc": "Video telah otomatis diunduh & caption disalin ke clipboard! Di tab TikTok, tinggal seret file video & tekan Ctrl+V pada deskripsi.",
    "js.tiktok.reopen_btn": "🎵 Buka TikTok Creator Studio ({name})",
  },
  en: {
    "top.tagline": "Scan Most Replayed, auto cut, clean subtitles.",
    "label.url": "YouTube URL",
    "ph.url": "https://www.youtube.com/watch?v=...",
    "help.url": "Paste a video/shorts link. Preview will show up.",
    "label.mode": "Mode",
    "opt.mode.heatmap": "Scan heatmap (Most Replayed)",
    "opt.mode.custom": "Custom start/end (manual)",
    "help.mode": "Scan = find the hottest moments. Custom = cut by your timestamps.",
    "label.ratio": "Ratio",
    "opt.ratio.9_16": "9:16 (Shorts)",
    "opt.ratio.original": "Original",
    "help.ratio": "Choose output aspect ratio. 9:16 is for Shorts/Reels/TikTok.",
    "label.resolution": "Resolution",
    "help.resolution": "Output video quality (720p, 1080p, or 4K).",
    "label.crop": "Crop",
    "opt.crop.default": "Default",
    "opt.crop.split_left": "Split Left",
    "opt.crop.split_right": "Split Right",
    "help.crop": "Split is for gaming: gameplay on top, facecam below.",
    "label.padding": "Padding (seconds)",
    "help.padding": "Adds seconds before & after, so it doesn’t cut awkwardly.",
    "label.max_clips": "Max clips",
    "help.max_clips": "How many clips to generate from the heatmap.",
    "label.subtitle": "Subtitle",
    "opt.no": "No",
    "opt.yes": "Yes",
    "help.subtitle": "If Yes, audio is transcribed to text and burned into the video.",
    "label.whisper_model": "Model (Whisper)",
    "help.whisper_model": "AI model for speech-to-text. Bigger = more accurate, heavier.",
    "label.subtitle_font": "Subtitle Font",
    "opt.custom": "Custom…",
    "ph.subtitle_font_custom": "Custom font name (e.g. Poppins)",
    "help.subtitle_font": "If the font is in fonts folder, set Fonts dir = fonts.",
    "label.subtitle_location": "Subtitle Location",
    "opt.subtitle_location.bottom": "Bottom",
    "opt.subtitle_location.center": "Centered",
    "help.subtitle_location": "Bottom looks natural for Shorts. Centered is more “in your face”.",
    "label.subtitle_fontsdir": "Fonts dir (optional)",
    "help.subtitle_fontsdir": "Folder containing .ttf/.otf for subtitles. Default: project <b>fonts</b> folder.",
    "label.start": "Start (seconds or mm:ss)",
    "ph.start": "689 or 11:29",
    "label.end": "End (seconds or mm:ss)",
    "ph.end": "742 or 12:22",
    "btn.scan": "Scan Heatmap",
    "btn.clip": "Create Clip",
    "help.actions": "Scan Heatmap = fetch “Most Replayed” moments. Create Clip = download + crop + (optional) subtitles.",
    "panel.segments": "Segments",
    "btn.select_all": "Select All",
    "btn.clear": "Clear",
    "btn.create_selected": "Create Selected Clip",
    "panel.progress": "Progress",
    "js.modal.preview_segment": "Preview Segment",
    "js.modal.preview_clip": "Preview Clip",
    "js.modal.open_yt": "Open in YouTube",
    "js.modal.unmute_hint": "🔊 Video is auto-muted by browser policy (unmute in player controls).",
    "js.segments.empty": "No segments yet. Click Scan Heatmap first.",
    "js.preview.loading": "Loading preview…",
    "js.progress.count": "{done}/{total} done • {success} success",
    "js.selected.count": "{count} selected",
    "js.stage.download": "Download",
    "js.stage.crop": "Crop",
    "js.stage.subtitle": "Subtitle",
    "js.stage.subtitle_model_load": "Load model",
    "js.stage.subtitle_transcribe": "Transcribe",
    "js.stage.subtitle_write": "Write subtitles",
    "js.stage.burn_subtitle": "Burn subtitles",
    "js.stage.finalize": "Finalize",
    "js.stage.done_clip": "Done",
    "js.topprogress.processing": "Processing",
    "js.form.title": "📌 Video Title",
    "js.form.caption": "📝 Caption / Description",
    "js.form.hashtags": "# Recommended Hashtags",
    "js.form.copy_title": "📋 Copy Title",
    "js.form.copy_caption": "📋 Copy Caption",
    "js.form.copy_hashtags": "📋 Copy #",
    "js.form.copy_all": "📋 Copy All (Title + Caption + #)",
    "js.form.var_title": "🔄 New Title Hook",
    "js.form.copied": "✅ Copied to clipboard!",
    "js.loading.title": "Creating Video Clips...",
    "js.loading.subtitle": "Rendering high-res video & AI subtitles",
    "js.loading.warn_title": "DO NOT CLOSE OR REFRESH PAGE",
    "js.loading.warn_desc": "Video rendering in progress. Closing or refreshing will cancel the active clip processing.",
    "js.loading.complete": "All video clips created successfully!",
    "js.loading.failed": "Encountered an issue processing clips.",
    "label.auto_tiktok": "🎵 Auto-redirect to TikTok Upload after clips finish",
    "btn.tiktok_upload": "🎵 Upload to TikTok",
    "js.scan.loading_title": "Scanning YouTube Heatmap...",
    "js.scan.loading_desc": "Analyzing Most Replayed curve to find peak viral retention moments...",
    "js.scan.scanning_btn": "Scanning Heatmap...",
    "js.tiktok.toast_title": "🚀 Ready to Upload to TikTok!",
    "js.tiktok.toast_desc": "Video downloaded & caption copied! On TikTok, drag & drop the video and press Ctrl+V into caption.",
    "js.tiktok.reopen_btn": "🎵 Open TikTok Creator Studio ({name})",
  },
};

let currentLang = "id";

function t(key, vars) {
  const base = I18N[currentLang] || I18N.id;
  const fallback = I18N.id || {};
  let s = base[key] ?? fallback[key] ?? key;
  if (vars && typeof s === "string") {
    Object.entries(vars).forEach(([k, v]) => {
      s = s.replaceAll(`{${k}}`, String(v));
    });
  }
  return s;
}

const TOP_PROGRESS = {
  pct: 0,
  titleBase: document.title || "YouTube Heatmap Clipper",
  hideTimer: null,
};

function clamp(n, a, b) {
  return Math.min(b, Math.max(a, n));
}

function easeOutCubic(x) {
  const t = clamp(x, 0, 1);
  return 1 - Math.pow(1 - t, 3);
}

function stageLabel(stage) {
  const key = {
    download: "js.stage.download",
    crop: "js.stage.crop",
    subtitle: "js.stage.subtitle",
    subtitle_model_load: "js.stage.subtitle_model_load",
    subtitle_transcribe: "js.stage.subtitle_transcribe",
    subtitle_write: "js.stage.subtitle_write",
    burn_subtitle: "js.stage.burn_subtitle",
    finalize: "js.stage.finalize",
    done_clip: "js.stage.done_clip",
  }[stage];
  return key ? t(key) : stage || "";
}

function computeJobPct(job) {
  if (!job) return { pct: 0, text: "", active: false };
  const status = job.status || "";
  if (status !== "running" && status !== "queued") {
    const done = Number(job.done || 0);
    const total = Number(job.total || 0);
    const pct = total > 0 ? clamp((done / total) * 100, 0, 100) : 0;
    return { pct, text: "", active: false };
  }

  const total = Math.max(1, Number(job.total || 1));
  const done = clamp(Number(job.done || 0), 0, total);
  const subtitleEnabled = Boolean(job.subtitle_enabled);
  const stage = job.stage || "";
  const stageAt = job.stage_at ? Number(job.stage_at) : 0;
  const elapsed = stageAt ? Date.now() - stageAt : 0;
  const clipIndexRaw = Number(job.stage_clip || job.current || (done + 1) || 1);
  const clipIndex = clamp(clipIndexRaw, 1, total);

  const mapNoSub = {
    download: { a: 0.04, b: 0.62, d: 14000 },
    crop: { a: 0.62, b: 0.96, d: 9000 },
    finalize: { a: 0.96, b: 0.995, d: 2500 },
    done_clip: { a: 1, b: 1, d: 0 },
  };
  const mapSub = {
    download: { a: 0.03, b: 0.55, d: 14000 },
    crop: { a: 0.55, b: 0.86, d: 9000 },
    subtitle: { a: 0.86, b: 0.87, d: 1200 },
    subtitle_model_load: { a: 0.87, b: 0.885, d: 2500 },
    subtitle_transcribe: { a: 0.885, b: 0.93, d: 20000 },
    subtitle_write: { a: 0.93, b: 0.94, d: 1800 },
    burn_subtitle: { a: 0.94, b: 0.985, d: 12000 },
    finalize: { a: 0.985, b: 0.995, d: 2500 },
    done_clip: { a: 1, b: 1, d: 0 },
  };

  const table = subtitleEnabled ? mapSub : mapNoSub;
  const s = table[stage] || (subtitleEnabled ? mapSub.download : mapNoSub.download);
  const within = s.d > 0 ? s.a + (s.b - s.a) * easeOutCubic(clamp(elapsed / s.d, 0, 0.98)) : s.a;
  const pctBase = ((clipIndex - 1) + within) / total * 100;
  const pctFloor = (done / total) * 100;
  const pct = clamp(Math.max(pctBase, pctFloor), 0, 99.5);

  const clipText = total > 0 ? `clip ${clipIndex}/${total}` : "";
  const sLabel = stageLabel(stage);
  const text = [t("js.topprogress.processing"), clipText, sLabel].filter(Boolean).join(" • ");
  return { pct, text, active: true };
}

function renderTopProgress(job) {
  const wrap = $("topProgressWrap");
  const bar = $("topProgressBar");
  const textEl = $("topProgressText");
  if (!wrap || !bar || !textEl) return;

  const { pct, text, active } = computeJobPct(job);

  if (!active) {
    if (job && (job.status === "done" || job.status === "error")) {
      bar.style.width = "100%";
      textEl.textContent = job.status === "error" ? "Error" : "";
      wrap.classList.remove("hide");
      clearTimeout(TOP_PROGRESS.hideTimer);
      TOP_PROGRESS.hideTimer = setTimeout(() => {
        wrap.classList.add("hide");
        bar.style.width = "0%";
        textEl.textContent = "";
      }, 650);
      document.title = TOP_PROGRESS.titleBase;
      TOP_PROGRESS.pct = 0;
      return;
    }
    wrap.classList.add("hide");
    bar.style.width = "0%";
    textEl.textContent = "";
    document.title = TOP_PROGRESS.titleBase;
    TOP_PROGRESS.pct = 0;
    return;
  }

  clearTimeout(TOP_PROGRESS.hideTimer);
  wrap.classList.remove("hide");
  TOP_PROGRESS.pct = Math.max(TOP_PROGRESS.pct, pct);
  bar.style.width = `${TOP_PROGRESS.pct.toFixed(1)}%`;
  textEl.textContent = text;
  document.title = `${TOP_PROGRESS.titleBase} (${Math.round(TOP_PROGRESS.pct)}%)`;
}

function applyI18n() {
  document.documentElement.lang = currentLang;
  $("langId")?.classList.toggle("isActive", currentLang === "id");
  $("langEn")?.classList.toggle("isActive", currentLang === "en");

  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (!key) return;
    el.innerHTML = t(key);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.dataset.i18nPlaceholder;
    if (!key) return;
    el.setAttribute("placeholder", t(key));
  });
}

function setLang(lang) {
  currentLang = lang === "en" ? "en" : "id";
  localStorage.setItem("lang", currentLang);
  applyI18n();
  renderSegments(lastScanSegments);
  updateSelectedUi();
}

function fmtTime(s) {
  const sec = Math.max(0, Math.floor(Number(s) || 0));
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const r = sec % 60;
  if (h > 0) return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(r).padStart(2, "0")}`;
  return `${String(m).padStart(2, "0")}:${String(r).padStart(2, "0")}`;
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || data.ok === false) {
    throw new Error(data.error || `HTTP ${res.status}`);
  }
  return data;
}

function openModal(title, bodyEl) {
  $("modalTitle").textContent = title || "";
  const root = $("modalBody");
  root.innerHTML = "";
  root.appendChild(bodyEl);
  $("modal").classList.remove("hide");
}

function closeModal() {
  $("modal").classList.add("hide");
  $("modalBody").innerHTML = "";
}

function debounce(fn, wait) {
  let t = null;
  return (...args) => {
    if (t) clearTimeout(t);
    t = setTimeout(() => fn(...args), wait);
  };
}

function readPayload() {
  const fontSel = $("subtitle_font_select").value;
  const fontCustom = ($("subtitle_font_custom").value || "").trim();
  const subtitleFont = fontSel === "custom" ? fontCustom : fontSel;
  return {
    url: $("url").value,
    mode: $("mode").value,
    ratio: $("ratio").value,
    resolution: $("resolution")?.value || "720p",
    crop: $("crop").value,
    padding: Number($("padding").value || 0),
    max_clips: Number($("max_clips").value || 6),
    subtitle: $("subtitle").value === "y",
    whisper_model: $("whisper_model").value,
    subtitle_font: subtitleFont,
    subtitle_location: $("subtitle_location").value,
    subtitle_fontsdir: $("subtitle_fontsdir").value || "",
    start: $("start").value || "",
    end: $("end").value || "",
  };
}

function setBusy(busy) {
  $("scanBtn").disabled = busy;
  $("clipBtn").disabled = busy;
  $("segSelectAllBtn").disabled = busy;
  $("segClearBtn").disabled = busy;
  $("segCreateBtn").disabled = busy || selectedKeys.size === 0;
}

function getVideoThumb(videoId, fallback) {
  if (!videoId) return fallback || "";
  return `https://i.ytimg.com/vi_webp/${videoId}/hqdefault.webp`;
}

function openYouTubePreview(videoId, startSec, endSec, title) {
  const start = Math.max(0, Math.floor(Number(startSec) || 0));
  const end = Math.max(0, Math.floor(Number(endSec) || 0));
  const origin = window.location.origin;
  const ytUrl = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(videoId)}?start=${start}${end > start ? `&end=${end}` : ""}&autoplay=1&mute=1&playsinline=1&rel=0&enablejsapi=1${origin && origin.startsWith("http") ? `&origin=${encodeURIComponent(origin)}` : ""}`;
  const directUrl = `https://youtu.be/${encodeURIComponent(videoId)}?t=${start}`;

  const container = document.createElement("div");
  container.className = "previewContainer";

  const iframe = document.createElement("iframe");
  iframe.className = "embed";
  iframe.src = ytUrl;
  iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
  iframe.allowFullscreen = true;
  iframe.referrerPolicy = "strict-origin-when-cross-origin";
  container.appendChild(iframe);

  const footer = document.createElement("div");
  footer.className = "previewFooter";

  const info = document.createElement("div");
  info.className = "previewInfo";
  const dur = end > start ? ` (${end - start}s)` : "";
  info.innerHTML = `<div>⏱️ <strong>${fmtTime(start)} → ${fmtTime(end)}</strong>${dur}</div><div class="previewHint">${t("js.modal.unmute_hint")}</div>`;
  footer.appendChild(info);

  const actions = document.createElement("div");
  actions.className = "previewActions";
  const directLink = document.createElement("a");
  directLink.className = "btn ghost smallBtn";
  directLink.href = directUrl;
  directLink.target = "_blank";
  directLink.rel = "noopener noreferrer";
  directLink.textContent = `↗ ${t("js.modal.open_yt")}`;
  actions.appendChild(directLink);
  footer.appendChild(actions);

  container.appendChild(footer);
  openModal(title || t("js.modal.preview_segment"), container);
}

function openClipPreview(title, src) {
  const v = document.createElement("video");
  v.className = "video";
  v.controls = true;
  v.autoplay = true;
  v.muted = true;
  v.playsInline = true;
  v.src = src;
  openModal(title || t("js.modal.preview_clip"), v);
}

function segKey(seg) {
  const start = Math.round(Number(seg.start || 0) * 1000);
  const dur = Math.round(Number(seg.duration || 0) * 1000);
  return `${start}:${dur}`;
}

function setSegControlsVisible(visible) {
  $("segControls").classList.toggle("hide", !visible);
}

function updateSelectedUi() {
  const count = selectedKeys.size;
  $("segSelectedMeta").textContent = count > 0 ? t("js.selected.count", { count }) : "";
  $("segCreateBtn").disabled = count === 0 || $("scanBtn").disabled;
  setSegControlsVisible($("mode").value === "heatmap" && lastScanSegments.length > 0);
}

function selectAllSegments() {
  selectedKeys = new Set(lastScanSegments.map(segKey));
  renderSegments(lastScanSegments);
  updateSelectedUi();
}

function clearSelectedSegments() {
  selectedKeys = new Set();
  renderSegments(lastScanSegments);
  updateSelectedUi();
}

// --- Loading Overlay & Prevent Accidental Page Close/Reload ---
let isProcessingClip = false;

function showLoadingOverlay(totalClips = 1) {
  isProcessingClip = true;
  document.body.classList.add("isClipping");
  const overlay = $("loadingOverlay");
  if (!overlay) return;

  $("loadingBarFill").style.width = "0%";
  $("loadingPercent").textContent = "0%";
  $("loadingClipCounter").textContent = `Klip 0/${totalClips}`;
  $("loadingStatusText").textContent = t("js.topprogress.processing") + "...";

  ["stageDownload", "stageCrop", "stageSubtitle", "stageFinal"].forEach((id) => {
    const el = $(id);
    if (el) el.classList.remove("active", "done");
  });

  overlay.classList.remove("hide");
}

function updateLoadingOverlay(job) {
  if (!job) return;
  const overlay = $("loadingOverlay");
  if (!overlay || overlay.classList.contains("hide")) return;

  const total = Number(job.total) || 1;
  const current = Number(job.current) || 0;
  const done = Number(job.done) || 0;
  const stage = (job.stage || "").toLowerCase();

  let stagePct = 0;
  if (stage === "download") stagePct = 0.15;
  else if (stage === "crop") stagePct = 0.35;
  else if (stage.startsWith("subtitle")) stagePct = 0.65;
  else if (stage.startsWith("burn") || stage === "finalize") stagePct = 0.90;
  else if (stage === "done_clip" || job.status === "done") stagePct = 1.0;

  let overallPct = 0;
  if (total > 0) {
    const completedFraction = done / total;
    const activeFraction = (1 / total) * stagePct;
    overallPct = Math.min(100, Math.round((completedFraction + activeFraction) * 100));
  }
  if (job.status === "done") overallPct = 100;

  $("loadingBarFill").style.width = `${overallPct}%`;
  $("loadingPercent").textContent = `${overallPct}%`;
  $("loadingClipCounter").textContent = `Klip ${Math.max(current, done)}/${total}`;

  if (job.status_text) {
    let readableStage = job.status_text;
    if (job.stage && I18N[currentLang]?.[`js.stage.${job.stage}`]) {
      readableStage = t(`js.stage.${job.stage}`);
    }
    $("loadingStatusText").textContent = `${readableStage} (Klip ${current || 1}/${total})`;
  }

  const bDownload = $("stageDownload");
  const bCrop = $("stageCrop");
  const bSub = $("stageSubtitle");
  const bFinal = $("stageFinal");

  [bDownload, bCrop, bSub, bFinal].forEach(el => el && el.classList.remove("active", "done"));

  if (stage === "download") {
    bDownload?.classList.add("active");
  } else if (stage === "crop") {
    bDownload?.classList.add("done");
    bCrop?.classList.add("active");
  } else if (stage.startsWith("subtitle")) {
    bDownload?.classList.add("done");
    bCrop?.classList.add("done");
    bSub?.classList.add("active");
  } else if (stage.startsWith("burn") || stage === "finalize") {
    bDownload?.classList.add("done");
    bCrop?.classList.add("done");
    bSub?.classList.add("done");
    bFinal?.classList.add("active");
  } else if (stage === "done_clip" || job.status === "done") {
    bDownload?.classList.add("done");
    bCrop?.classList.add("done");
    bSub?.classList.add("done");
    bFinal?.classList.add("done");
  }
}

function highlightLoadingWarning() {
  const box = $("loadingWarningBox");
  if (!box) return;
  box.classList.remove("shake");
  void box.offsetWidth;
  box.classList.add("shake");
  setTimeout(() => box.classList.remove("shake"), 600);
}

let toastTimer = null;
function showToast(title, message, icon = "🎵", duration = 7000) {
  const tEl = $("toast");
  if (!tEl) return;
  $("toastTitle").textContent = title;
  $("toastMessage").textContent = message;
  $("toastIcon").textContent = icon;
  tEl.classList.remove("hide");
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    tEl.classList.add("hide");
  }, duration);
}

async function uploadClipToTikTok(clipItem, jobId) {
  if (!clipItem) return;
  const href = `/clips/${jobId}/${encodeURIComponent(clipItem.name)}`;

  // 1. Trigger Video Download
  const a = document.createElement("a");
  a.href = href;
  a.download = clipItem.name || "tiktok_clip.mp4";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  // 2. Prepare text (Caption + Hashtags)
  const title = (clipItem.title || "").trim();
  const caption = (clipItem.caption || "").trim();
  const hashtags = (clipItem.hashtags || "").trim();
  const textToCopy = `${caption}\n\n${hashtags}`.trim() || title;

  // 3. Copy to clipboard
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(textToCopy);
    } else {
      const ta = document.createElement("textarea");
      ta.value = textToCopy;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
  } catch (err) {
    console.warn("Copy to clipboard error:", err);
  }

  // 4. Open TikTok Creator Studio Upload in new tab
  const tiktokUrl = "https://www.tiktok.com/creator-center/upload?from=webapp";
  window.open(tiktokUrl, "_blank");

  showToast(
    t("js.tiktok.toast_title"),
    t("js.tiktok.toast_desc"),
    "🎵",
    8000
  );
}

function hideLoadingOverlay(isSuccess = true, lastJob = null) {
  isProcessingClip = false;
  document.body.classList.remove("isClipping");
  const overlay = $("loadingOverlay");
  if (!overlay) return;

  if (isSuccess) {
    $("loadingBarFill").style.width = "100%";
    $("loadingPercent").textContent = "100%";
    $("loadingStatusText").textContent = t("js.loading.complete");
    ["stageDownload", "stageCrop", "stageSubtitle", "stageFinal"].forEach((id) => {
      $(id)?.classList.add("done");
    });

    const outputs = lastJob && Array.isArray(lastJob.outputs) ? lastJob.outputs : [];
    const shouldUploadTiktok = $("autoUploadTiktok")?.checked && outputs.length > 0;

    if (shouldUploadTiktok) {
      const firstClip = outputs[0];
      const compBox = $("loadingCompleteBox");
      const tiktokBtn = $("loadingTiktokBtn");
      if (compBox && tiktokBtn) {
        tiktokBtn.onclick = () => uploadClipToTikTok(firstClip, lastJob.id);
        compBox.classList.remove("hide");
      }
      uploadClipToTikTok(firstClip, lastJob.id);
    }

    setTimeout(() => {
      overlay.classList.add("hide");
      const compBox = $("loadingCompleteBox");
      if (compBox) compBox.classList.add("hide");

      const progEl = $("progress");
      if (progEl) {
        progEl.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, shouldUploadTiktok ? 1200 : 600);
  } else {
    overlay.classList.add("hide");
  }
}

window.addEventListener("beforeunload", (e) => {
  if (isProcessingClip) {
    e.preventDefault();
    e.returnValue = "";
    highlightLoadingWarning();
    return "";
  }
});

window.addEventListener("keydown", (e) => {
  if (isProcessingClip) {
    const isF5 = e.key === "F5";
    const isReload = (e.ctrlKey || e.metaKey) && (e.key === "r" || e.key === "R");
    if (isF5 || isReload) {
      e.preventDefault();
      highlightLoadingWarning();
    }
  }
});

async function clipSelected() {
  if ($("mode").value !== "heatmap") return;
  if (selectedKeys.size === 0) return;
  setBusy(true);
  const picked = lastScanSegments.filter((s) => selectedKeys.has(segKey(s)));
  showLoadingOverlay(picked.length || 1);
  try {
    const payload = readPayload();
    const data = await postJson("/api/clip", { ...payload, segments: picked });
    const jobId = data.job_id;
    const finalJob = await pollJob(jobId);
    hideLoadingOverlay(finalJob && finalJob.status === "done", finalJob);
  } catch (e) {
    hideLoadingOverlay(false);
    renderProgress({ status: "error", error: e.message, total: 0, done: 0, id: "" });
  } finally {
    setBusy(false);
    updateSelectedUi();
  }
}

function renderSegments(segments) {
  const root = $("segments");
  root.innerHTML = "";
  if (!segments || segments.length === 0) {
    root.innerHTML = `<div class="small">${t("js.segments.empty")}</div>`;
    updateSelectedUi();
    return;
  }
  segments.forEach((s, idx) => {
    const start = Number(s.start || 0);
    const dur = Number(s.duration || 0);
    const end = start + dur;
    const score = Number(s.score || 0);
    const el = document.createElement("div");
    el.className = "seg";
    const key = segKey(s);
    if (selectedKeys.has(key)) el.classList.add("selected");
    const thumb = getVideoThumb(currentVideoId, currentPreview?.thumbnail);
    el.innerHTML = `
      <div class="segThumb" data-preview-trigger="1" title="Preview video">
        <img alt="" src="${thumb}" />
        <div class="segPlayIcon" aria-hidden="true">▶</div>
        <div class="segTime">${fmtTime(start)}</div>
      </div>
      <div class="segMain">
        <div class="t">#${idx + 1} ${fmtTime(start)} → ${fmtTime(end)}</div>
        <div class="m">durasi ${Math.round(dur)}s</div>
      </div>
      <div class="segSide">
        <div class="pill">${score.toFixed(2)}</div>
        <button class="btn ghost smallBtn" type="button" data-preview="1">Preview</button>
      </div>
    `;
    el.addEventListener("click", (ev) => {
      const isPreview = ev.target && (ev.target.closest("[data-preview]") || ev.target.closest("[data-preview-trigger]"));
      if (isPreview) {
        ev.preventDefault();
        ev.stopPropagation();
        if (currentVideoId) openYouTubePreview(currentVideoId, start, end, currentPreview?.title || "Preview Segment");
        return;
      }
      if ($("mode").value === "custom") {
        $("start").value = Math.floor(start);
        $("end").value = Math.floor(end);
        return;
      }
      if (selectedKeys.has(key)) selectedKeys.delete(key);
      else selectedKeys.add(key);
      el.classList.toggle("selected");
      updateSelectedUi();
    });
    root.appendChild(el);
  });
  updateSelectedUi();
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderOutputCard(f, jobId, idx) {
  const card = document.createElement("div");
  card.className = "outCard";
  card.dataset.name = f.name;
  const href = `/clips/${jobId}/${encodeURIComponent(f.name)}`;

  const variations = Array.isArray(f.title_variations) && f.title_variations.length > 0
    ? f.title_variations
    : [f.title || `Clip #${idx}`];
  let varIdx = 0;

  card.innerHTML = `
    <div class="outHeader">
      <div class="outLeft">
        <span class="outBadge">🎬 Clip #${idx}</span>
        <a class="outFileName" href="${href}" target="_blank" rel="noreferrer">${escapeHtml(f.name)}</a>
        <span class="small">(${Math.round((f.size || 0) / 1024)} KB)</span>
      </div>
      <div class="outRight">
        <button class="btn smallBtn tiktokBtn" type="button" data-tiktok="1">${t("btn.tiktok_upload")}</button>
        <button class="btn ghost smallBtn" type="button" data-play="1">▶ Play</button>
        <a class="btn ghost smallBtn" href="${href}" download>⬇ Download</a>
      </div>
    </div>

    <div class="clipMetaForm">
      <div class="metaRow">
        <div class="metaLabelBar">
          <label class="metaFieldLabel">${t("js.form.title")}</label>
          <button class="copyMiniBtn" type="button" data-copy="title">${t("js.form.copy_title")}</button>
        </div>
        <input class="input clipTitleInput" type="text" value="${escapeHtml(f.title || '')}" />
      </div>

      <div class="metaRow">
        <div class="metaLabelBar">
          <label class="metaFieldLabel">${t("js.form.caption")}</label>
          <button class="copyMiniBtn" type="button" data-copy="caption">${t("js.form.copy_caption")}</button>
        </div>
        <textarea class="input clipCaptionInput" rows="3">${escapeHtml(f.caption || '')}</textarea>
      </div>

      <div class="metaRow">
        <div class="metaLabelBar">
          <label class="metaFieldLabel">${t("js.form.hashtags")}</label>
          <button class="copyMiniBtn" type="button" data-copy="hashtags">${t("js.form.copy_hashtags")}</button>
        </div>
        <textarea class="input clipHashtagsInput" rows="2">${escapeHtml(f.hashtags || '')}</textarea>
      </div>

      <div class="metaBottomBar">
        <button class="btn smallBtn copyAllBtn" type="button">${t("js.form.copy_all")}</button>
        ${variations.length > 1 ? `<button class="btn ghost smallBtn varTitleBtn" type="button">${t("js.form.var_title")}</button>` : ""}
        <span class="copyFeedback">${t("js.form.copied")}</span>
      </div>
    </div>
  `;

  card.querySelector("[data-play]")?.addEventListener("click", (ev) => {
    ev.preventDefault();
    openClipPreview(f.name, href);
  });

  card.querySelector("[data-tiktok]")?.addEventListener("click", () => {
    uploadClipToTikTok({
      name: f.name,
      title: titleInput.value,
      caption: captionInput.value,
      hashtags: hashtagsInput.value
    }, jobId);
  });

  const titleInput = card.querySelector(".clipTitleInput");
  const captionInput = card.querySelector(".clipCaptionInput");
  const hashtagsInput = card.querySelector(".clipHashtagsInput");
  const feedback = card.querySelector(".copyFeedback");

  function showFeedback() {
    if (!feedback) return;
    feedback.classList.add("show");
    setTimeout(() => {
      feedback.classList.remove("show");
    }, 2000);
  }

  async function copyToClipboard(text) {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
      }
      showFeedback();
    } catch (err) {
      console.error("Copy failed", err);
    }
  }

  card.querySelector('[data-copy="title"]')?.addEventListener("click", () => {
    copyToClipboard(titleInput.value);
  });

  card.querySelector('[data-copy="caption"]')?.addEventListener("click", () => {
    copyToClipboard(captionInput.value);
  });

  card.querySelector('[data-copy="hashtags"]')?.addEventListener("click", () => {
    copyToClipboard(hashtagsInput.value);
  });

  card.querySelector(".copyAllBtn")?.addEventListener("click", () => {
    const fullText = `${titleInput.value}\n\n${captionInput.value}\n\n${hashtagsInput.value}`.trim();
    copyToClipboard(fullText);
  });

  card.querySelector(".varTitleBtn")?.addEventListener("click", () => {
    if (variations.length <= 1) return;
    varIdx = (varIdx + 1) % variations.length;
    titleInput.value = variations[varIdx];
    titleInput.focus();
  });

  return card;
}

function renderProgress(job) {
  const root = $("progress");
  const meta = $("jobMeta");
  const out = $("outputs");
  root.innerHTML = "";
  meta.textContent = "";
  if (!job) {
    out.innerHTML = "";
    return;
  }
  renderTopProgress(job);
  const total = Number(job.total || 0);
  const done = Number(job.done || 0);
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const stage = stageLabel(job.stage || "");
  meta.textContent = `${job.status} • ${(job.status_text || "").trim()}${stage ? " • " + stage : ""}`.trim();

  const bar = document.createElement("div");
  bar.innerHTML = `<div class="bar"><div style="width:${pct}%"></div></div>`;
  root.appendChild(bar);

  const line = document.createElement("div");
  line.className = "small";
  line.textContent =
    total > 0
      ? t("js.progress.count", { done, total, success: job.success || 0 })
      : "";
  root.appendChild(line);

  if (job.status === "error") {
    const err = document.createElement("div");
    err.className = "small";
    err.textContent = job.error || "error";
    root.appendChild(err);
  }

  // Preserve card form contents across poll intervals by checking existing elements
  const currentJobId = out.dataset.jobId;
  if (currentJobId !== job.id) {
    out.innerHTML = "";
    out.dataset.jobId = job.id;
  }

  if (Array.isArray(job.outputs) && job.outputs.length > 0) {
    job.outputs.forEach((f, idx) => {
      const safeName = (f.name || "").replace(/"/g, '\\"');
      let existing = out.querySelector(`.outCard[data-name="${safeName}"]`);
      if (!existing) {
        const card = renderOutputCard(f, job.id, idx + 1);
        out.appendChild(card);
      }
    });
  }
}

let lastScanSegments = [];
let lastPreviewUrl = "";
let currentPreview = null;
let currentVideoId = "";
let selectedKeys = new Set();

function renderScanLoading() {
  const root = $("segments");
  root.innerHTML = `
    <div class="scanLoadingCard">
      <div class="scanRadarWrap">
        <div class="scanRadar">
          <div class="radarSweep"></div>
          <div class="radarPing"></div>
          <div class="radarCenter">📡</div>
        </div>
      </div>
      <div class="scanLoadingText">
        <h4>${t("js.scan.loading_title")}</h4>
        <p>${t("js.scan.loading_desc")}</p>
      </div>
      <div class="skeletonGrid">
        <div class="segSkeleton"><div class="skThumb"></div><div class="skBody"><div class="skLine1"></div><div class="skLine2"></div></div></div>
        <div class="segSkeleton"><div class="skThumb"></div><div class="skBody"><div class="skLine1"></div><div class="skLine2"></div></div></div>
        <div class="segSkeleton"><div class="skThumb"></div><div class="skBody"><div class="skLine1"></div><div class="skLine2"></div></div></div>
      </div>
    </div>
  `;
}

async function scan() {
  const scanBtn = $("scanBtn");
  const origBtnText = scanBtn.textContent;
  scanBtn.classList.add("isScanning");
  scanBtn.innerHTML = `<span class="btnSpinner"></span> ${t("js.scan.scanning_btn")}`;

  setBusy(true);
  renderScanLoading();
  $("segMeta").textContent = t("js.scan.scanning_btn");

  const segPanel = $("segments");
  if (segPanel) {
    segPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  try {
    const { url } = readPayload();
    const data = await postJson("/api/scan", { url });
    lastScanSegments = data.segments || [];
    selectedKeys = new Set();
    currentVideoId = data.video_id || currentVideoId;
    $("segMeta").textContent = `${lastScanSegments.length} segments • durasi ~${fmtTime(data.duration || 0)}`;
    renderSegments(lastScanSegments);
  } catch (e) {
    $("segMeta").textContent = e.message;
    renderSegments([]);
  } finally {
    setBusy(false);
    scanBtn.classList.remove("isScanning");
    scanBtn.textContent = origBtnText;
    updateSelectedUi();
  }
}

async function preview() {
  const url = $("url").value.trim();
  if (!url || url === lastPreviewUrl) return;
  lastPreviewUrl = url;
  const box = $("preview");
  const title = $("pvTitle");
  const sub = $("pvSub");
  const img = $("thumbImg");
  try {
    title.textContent = t("js.preview.loading");
    sub.textContent = "";
    img.removeAttribute("src");
    box.classList.remove("hide");
    const data = await postJson("/api/preview", { url });
    const p = data.preview || {};
    currentPreview = p;
    if (p.id) currentVideoId = p.id;
    title.textContent = p.title || "Untitled";
    const dur = p.duration != null ? fmtTime(p.duration) : "";
    const uploader = p.uploader || "";
    sub.textContent = [uploader, dur].filter(Boolean).join(" • ");
    if (p.thumbnail) img.src = p.thumbnail;
  } catch (e) {
    box.classList.add("hide");
  }
}

async function clip() {
  setBusy(true);
  showLoadingOverlay(1);
  try {
    const payload = readPayload();
    const data = await postJson("/api/clip", payload);
    const jobId = data.job_id;
    const finalJob = await pollJob(jobId);
    hideLoadingOverlay(finalJob && finalJob.status === "done", finalJob);
  } catch (e) {
    hideLoadingOverlay(false);
    renderProgress({ status: "error", error: e.message, total: 0, done: 0, id: "" });
  } finally {
    setBusy(false);
  }
}

async function pollJob(jobId) {
  const started = Date.now();
  while (true) {
    const res = await fetch(`/api/job/${jobId}`);
    const data = await res.json().catch(() => null);
    if (!data || !data.ok) throw new Error("Job not found");
    renderProgress(data.job);
    updateLoadingOverlay(data.job);
    if (data.job.status === "done" || data.job.status === "error") {
      return data.job;
    }
    if (Date.now() - started > 1000 * 60 * 30) throw new Error("Timeout");
    await new Promise((r) => setTimeout(r, 1500));
  }
}

function toggleMode() {
  const isCustom = $("mode").value === "custom";
  $("customBox").classList.toggle("hide", !isCustom);
  $("scanBtn").classList.toggle("hide", isCustom);
  if (isCustom) {
    setSegControlsVisible(false);
    $("segSelectedMeta").textContent = "";
  } else {
    setSegControlsVisible(lastScanSegments.length > 0);
    updateSelectedUi();
  }
}

function toggleFont() {
  const isCustom = $("subtitle_font_select").value === "custom";
  $("subtitle_font_custom").classList.toggle("hide", !isCustom);
}

$("mode").addEventListener("change", toggleMode);
$("subtitle_font_select").addEventListener("change", toggleFont);
$("url").addEventListener("input", debounce(preview, 500));
$("scanBtn").addEventListener("click", scan);
$("clipBtn").addEventListener("click", clip);
$("segSelectAllBtn").addEventListener("click", selectAllSegments);
$("segClearBtn").addEventListener("click", clearSelectedSegments);
$("segCreateBtn").addEventListener("click", clipSelected);
$("modalClose").addEventListener("click", closeModal);
$("modalBackdrop").addEventListener("click", closeModal);
$("langId")?.addEventListener("click", () => setLang("id"));
$("langEn")?.addEventListener("click", () => setLang("en"));
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});

currentLang = localStorage.getItem("lang") || document.documentElement.lang || "id";
currentLang = currentLang === "en" ? "en" : "id";
applyI18n();
toggleMode();
toggleFont();
renderSegments([]);

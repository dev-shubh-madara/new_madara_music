# ╔══════════════════════════════════════════════════╗
# ║        🎵  M A D A R A  M U S I C  🎵           ║
# ║  Premium Music Thumbnail — Player Style          ║
# ╚══════════════════════════════════════════════════╝
import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "MADARAMUSIC", "assets")
if not os.path.isdir(_ASSETS):
    _ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

def _af(name: str) -> str:
    p = os.path.join(_ASSETS, name)
    return p if os.path.exists(p) else ""


def _round_rect_mask(size: tuple, radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    return mask


def _paste_rounded(bg: Image.Image, img: Image.Image, pos: tuple, radius: int = 20):
    mask = _round_rect_mask(img.size, radius)
    bg.paste(img, pos, mask)


def _draw_progress_bar(
    draw: ImageDraw.Draw,
    x: int, y: int, total_w: int, played_ratio: float = 0.1,
    height: int = 8, bg_col=(60, 60, 80), fill_col=(200, 80, 255), knob_col=(255, 255, 255),
):
    """Spotify-style progress bar."""
    # track background
    draw.rounded_rectangle([x, y, x + total_w, y + height], height // 2, fill=bg_col)
    # played portion
    played_w = max(height, int(total_w * played_ratio))
    draw.rounded_rectangle([x, y, x + played_w, y + height], height // 2, fill=fill_col)
    # knob
    kx = x + played_w
    ky = y + height // 2
    draw.ellipse([kx - 7, ky - 7, kx + 7, ky + 7], fill=knob_col)


def _draw_volume_bar(
    draw: ImageDraw.Draw, x: int, y: int, total_w: int,
    vol_ratio: float = 0.75,
):
    """Volume slider bar."""
    draw.rounded_rectangle([x, y, x + total_w, y + 5], 3, fill=(60, 60, 80))
    draw.rounded_rectangle([x, y, x + int(total_w * vol_ratio), y + 5], 3, fill=(180, 180, 180))


def trim_to_width(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    ellipsis = "…"
    if font.getlength(text) <= max_w:
        return text
    for i in range(len(text) - 1, 0, -1):
        if font.getlength(text[:i] + ellipsis) <= max_w:
            return text[:i] + ellipsis
    return ellipsis


async def get_thumb(videoid: str) -> str:
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_v5.png")
    if os.path.exists(cache_path):
        return cache_path

    # ── Fetch YouTube metadata ───────────────────────────────
    results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
    try:
        results_data = await results.next()
        result_items = results_data.get("result", [])
        if not result_items:
            raise ValueError("No results found.")
        data      = result_items[0]
        title     = re.sub(r"\W+", " ", data.get("title", "Unsupported Title")).title()
        thumbnail = data.get("thumbnails", [{}])[0].get("url", YOUTUBE_IMG_URL)
        duration  = data.get("duration")
        views     = data.get("viewCount", {}).get("short", "Unknown Views")
        channel   = data.get("channel", {}).get("name", "Unknown Artist")
    except Exception:
        title, thumbnail, duration, views, channel = (
            "Unsupported Title", YOUTUBE_IMG_URL, None, "Unknown Views", "YouTube"
        )

    is_live      = not duration or str(duration).strip().lower() in {"", "live", "live now"}
    duration_txt = "LIVE" if is_live else (duration or "0:00")

    # ── Download thumbnail ───────────────────────────────────
    thumb_path = os.path.join(CACHE_DIR, f"thumb{videoid}.png")
    thumb_ok   = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await resp.read())
                    thumb_ok = True
    except Exception:
        pass
    if not thumb_ok or not os.path.exists(thumb_path):
        return YOUTUBE_IMG_URL

    # ── Canvas: 1280 × 720 ───────────────────────────────────
    W, H = 1280, 720

    # Background: blurred + darkened album art
    base = Image.open(thumb_path).resize((W, H)).convert("RGBA")
    bg   = ImageEnhance.Brightness(base.filter(ImageFilter.GaussianBlur(25))).enhance(0.35)

    # Dark vignette gradient overlay
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd       = ImageDraw.Draw(vignette)
    for i in range(100):
        alpha = int(i * 1.8)
        vd.rectangle([i, i, W - i, H - i], outline=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg, vignette)

    draw = ImageDraw.Draw(bg)

    # ── Fonts ────────────────────────────────────────────────
    font_path_b = _af("assets/font2.ttf") or _af("font2.ttf")
    font_path_r = _af("assets/font.ttf")  or _af("font.ttf")
    try:
        f_title   = ImageFont.truetype(font_path_b, 38) if font_path_b else ImageFont.load_default()
        f_artist  = ImageFont.truetype(font_path_r, 24) if font_path_r else ImageFont.load_default()
        f_time    = ImageFont.truetype(font_path_r, 22) if font_path_r else ImageFont.load_default()
        f_ctrl    = ImageFont.truetype(font_path_b, 44) if font_path_b else ImageFont.load_default()
        f_views   = ImageFont.truetype(font_path_r, 20) if font_path_r else ImageFont.load_default()
        f_badge   = ImageFont.truetype(font_path_b, 18) if font_path_b else ImageFont.load_default()
    except OSError:
        f_title = f_artist = f_time = f_ctrl = f_views = f_badge = ImageFont.load_default()

    # ── Album art (left panel) ───────────────────────────────
    ART_X, ART_Y = 70, 190
    ART_W, ART_H = 330, 330
    art           = Image.open(thumb_path).resize((ART_W, ART_H)).convert("RGBA")

    # Soft shadow under album art
    shadow = Image.new("RGBA", (ART_W + 20, ART_H + 20), (0, 0, 0, 0))
    shadow_d = ImageDraw.Draw(shadow)
    shadow_d.rounded_rectangle([10, 10, ART_W + 10, ART_H + 10], 22, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    bg.paste(shadow, (ART_X - 10, ART_Y - 10), shadow)

    _paste_rounded(bg, art, (ART_X, ART_Y), radius=22)

    # Views badge on album art bottom-left
    badge_txt = f"🎬 {views}"
    draw.rounded_rectangle([ART_X, ART_Y + ART_H - 36, ART_X + 150, ART_Y + ART_H], 8,
                           fill=(0, 0, 0, 180))
    draw.text((ART_X + 8, ART_Y + ART_H - 26), badge_txt, fill=(255, 255, 255), font=f_badge)

    # "OFFICIAL VIDEO" badge top-right of art
    draw.rounded_rectangle([ART_X + ART_W - 130, ART_Y, ART_X + ART_W, ART_Y + 30], 8,
                           fill=(200, 80, 255, 200))
    draw.text((ART_X + ART_W - 120, ART_Y + 6), "OFFICIAL VIDEO", fill=(255, 255, 255), font=f_badge)

    # ── Info panel (right side) ───────────────────────────────
    INFO_X  = 455
    INFO_TOP = 190
    INFO_W   = W - INFO_X - 60
    PROGRESS_W = INFO_W

    # Song title
    title_txt = trim_to_width(title, f_title, INFO_W)
    draw.text((INFO_X, INFO_TOP), title_txt, fill=(255, 255, 255), font=f_title)

    # Star / menu icons (decorative)
    draw.text((INFO_X + INFO_W - 30, INFO_TOP + 8), "⋮", fill=(200, 200, 200), font=f_artist)

    # Artist / channel
    artist_txt = trim_to_width(channel, f_artist, INFO_W - 80)
    draw.text((INFO_X, INFO_TOP + 58), artist_txt, fill=(180, 180, 200), font=f_artist)

    # Time display
    time_y      = INFO_TOP + 100
    start_time  = "0:03"
    minus_dur   = f"-{duration_txt}" if not is_live else "● LIVE"
    draw.text((INFO_X, time_y), start_time, fill=(180, 180, 180), font=f_time)
    minus_w = int(f_time.getlength(minus_dur))
    draw.text((INFO_X + PROGRESS_W - minus_w, time_y),
              minus_dur, fill=(200, 80, 255) if is_live else (180, 180, 180), font=f_time)

    # Progress bar
    bar_y = time_y + 32
    _draw_progress_bar(draw, INFO_X, bar_y, PROGRESS_W, played_ratio=0.02 if is_live else 0.08)

    # ── Controls ◄◄  ⏸  ▶▶ ────────────────────────────────
    ctrl_y     = bar_y + 50
    ctrl_cx    = INFO_X + PROGRESS_W // 2
    # prev
    draw.text((ctrl_cx - 120, ctrl_y), "◄◄", fill=(220, 220, 220), font=f_ctrl, anchor="mm")
    # pause / play — filled circle
    draw.ellipse([ctrl_cx - 32, ctrl_y - 32, ctrl_cx + 32, ctrl_y + 32], fill=(255, 255, 255))
    draw.text((ctrl_cx, ctrl_y), "⏸", fill=(20, 20, 40), font=f_ctrl, anchor="mm")
    # next
    draw.text((ctrl_cx + 120, ctrl_y), "▶▶", fill=(220, 220, 220), font=f_ctrl, anchor="mm")

    # ── Volume slider ──────────────────────────────────────
    vol_y = ctrl_y + 60
    draw.text((INFO_X, vol_y + 2), "🔈", fill=(160, 160, 160), font=f_time)
    _draw_volume_bar(draw, INFO_X + 34, vol_y + 7, PROGRESS_W - 70)
    draw.text((INFO_X + PROGRESS_W - 26, vol_y + 2), "🔊", fill=(160, 160, 160), font=f_time)

    # ── Cleanup & save ────────────────────────────────────────
    try:
        os.remove(thumb_path)
    except OSError:
        pass

    bg.save(cache_path)
    return cache_path

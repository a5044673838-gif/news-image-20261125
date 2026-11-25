# One-day world news infographic for make.fun's "news-image-20261125" bounty.
# Draws a 1024x1024 PNG summing up Wednesday 25 November 2026 world news.
# Pure Python standard library, no network, fully deterministic.
# Writes /output/entry.png (MAKEFUN_OUTPUT_DIR overrides).
import os
import struct
import zlib

# ---------------------------------------------------------------------------
# 5x7 bitmap font. Each glyph is 7 rows of 5 pixels ('#' = on, '.' = off).
# ---------------------------------------------------------------------------
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "10110", "11001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "10110", "11001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "10110", "11001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    'q': ("00000", "00000", "01101", "10011", "10001", "01111", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11110", "01000", "01000", "01001", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ';': ("00000", "00000", "01100", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}

# ---------------------------------------------------------------------------
# Canvas: a flat RGB pixel buffer.
# ---------------------------------------------------------------------------
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
GRAY = (90, 90, 90)
NAVY = (15, 42, 68)
RED = (179, 38, 30)
WHITE = (255, 255, 255)
LIGHT = (226, 222, 212)
CARD = (255, 255, 255)
BORDER = (200, 196, 186)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            if yy < 0 or yy >= self.h:
                continue
            base = (yy * self.w + max(x, 0)) * 3
            span = min(x + w, self.w) - max(x, 0)
            if span <= 0:
                continue
            self.px[base:base + span * 3] = bytes(color) * span

    def hline(self, x, y, w, color):
        self.rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.rect(x, y, 1, h, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def wrap(text, max_w, scale):
    """Word-wrap text to lines that fit max_w pixels at the given scale."""
    words = text.split(' ')
    lines, cur = [], ''
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# Stories: verified against Reuters / AP / AFP / WHO / Xinhua reporting.
# ---------------------------------------------------------------------------
STORIES = [
    ("CYBERATTACK", (179, 38, 30), "US SPY AGENCIES HACKED",
     "CIA and the intelligence director's office report a breach of "
     "unclassified systems; classified networks said unaffected."),
    ("COURTS", (15, 42, 68), "HUAWEI FOUND GUILTY IN US TRIAL",
     "A jury convicts the Chinese tech giant on 10 of 12 counts, "
     "including trade-secrets theft and bank fraud."),
    ("HEALTH", (31, 122, 90), "WHO PULLS EBOLA TEAMS FROM CONGO",
     "Staff evacuated from an Ituri hospital after three days sheltering "
     "from fierce fighting; outbreak toll: 5,775 dead."),
    ("CHINA", (140, 40, 90), "SHANGHAI PARTY CHIEF UNDER PROBE",
     "Chen Jining, a Politburo member, faces a graft investigation - "
     "the fourth top leader probed since 2025."),
    ("ENERGY", (180, 110, 20), "IRAN SAYS TANKERS HIT MINES",
     "Tehran claims three oil tankers caught fire after striking mines "
     "near the Strait of Hormuz; claims not verified."),
    ("WHITE HOUSE", (90, 90, 90), "TURKEYS PARDONED - ONE FLEES",
     "Trump spares Freedom and Feathers at the White House; Feathers "
     "runs into the bushes before the ceremony."),
]


def draw():
    c = Canvas(W, H, PAPER)
    # Header band.
    c.rect(0, 0, W, 132, NAVY)
    c.rect(0, 132, W, 6, RED)
    c.text(40, 26, "WORLD NEWS", 7, WHITE)
    c.text(40, 86, "WEDNESDAY, 25 NOVEMBER 2026", 4, (200, 210, 220))
    # Story cards.
    y = 144
    row_h, gap = 138, 6
    for i, (tag, accent, head, body) in enumerate(STORIES):
        c.rect(40, y, 944, row_h, CARD)
        # Border.
        c.hline(40, y, 944, BORDER)
        c.hline(40, y + row_h - 1, 944, BORDER)
        c.vline(40, y, row_h, BORDER)
        c.vline(40 + 944 - 1, y, row_h, BORDER)
        # Accent bar + number.
        c.rect(40, y, 12, row_h, accent)
        c.text(72, y + 40, str(i + 1), 6, accent)
        # Tag, headline, body.
        tx = 140
        c.text(tx, y + 12, tag, 2, accent)
        c.text(tx, y + 34, head, 4, INK)
        lines = wrap(body, 944 - (tx - 40) - 24, 3)
        by = y + 70
        for line in lines[:3]:
            c.text(tx, by, line, 3, GRAY)
            by += 22
        y += row_h + gap
    # Footer.
    c.text(40, 1006, "SOURCES: REUTERS, AP, AFP, WHO, XINHUA", 2, GRAY)
    return c


def write_png(canvas, path):
    raw = bytearray()
    for yy in range(canvas.h):
        raw.append(0)
        raw += canvas.px[yy * canvas.w * 3:(yy + 1) * canvas.w * 3]

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "output")
        os.makedirs(out_dir, exist_ok=True)
    write_png(draw(), os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

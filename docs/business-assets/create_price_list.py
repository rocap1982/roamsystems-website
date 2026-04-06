"""
ROAM Systems - Premium PDF Price List v6
Brand-matched: actual logo, Barlow font, #f47d23 orange
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import urllib.request
import os
import tempfile

WIDTH, HEIGHT = A4
CX = WIDTH / 2

# ── Brand palette (from website global.css) ──
ROAM_ORANGE    = HexColor("#f47d23")
ROAM_ORANGE_DK = HexColor("#d96a1a")
ROAM_DARK      = HexColor("#1a1a1a")
ROAM_GRAY      = HexColor("#2d2d2d")
ROAM_LIGHT     = HexColor("#f5f5f5")
CARD_BG        = HexColor("#262626")
WHITE_T        = HexColor("#F0F0F0")
GREY_T         = HexColor("#9A9A9A")
DIM_T          = HexColor("#5E5E5E")
RULE_COL       = HexColor("#383838")

# Logo path
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "roam-systems", "public", "images", "roam-systems-logo.png")


def register_fonts():
    """Download and register Barlow fonts for brand consistency."""
    font_dir = os.path.join(tempfile.gettempdir(), "roam_fonts")
    os.makedirs(font_dir, exist_ok=True)

    fonts = {
        "Barlow-Bold": "https://github.com/jpt/barlow/raw/main/fonts/ttf/Barlow-Bold.ttf",
        "Barlow-SemiBold": "https://github.com/jpt/barlow/raw/main/fonts/ttf/Barlow-SemiBold.ttf",
        "Barlow-Regular": "https://github.com/jpt/barlow/raw/main/fonts/ttf/Barlow-Regular.ttf",
        "Barlow-Medium": "https://github.com/jpt/barlow/raw/main/fonts/ttf/Barlow-Medium.ttf",
    }

    for name, url in fonts.items():
        path = os.path.join(font_dir, f"{name}.ttf")
        if not os.path.exists(path):
            try:
                urllib.request.urlretrieve(url, path)
                print(f"  Downloaded {name}")
            except Exception as e:
                print(f"  Failed to download {name}: {e}")
                return False
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except Exception:
            return False
    return True


def rect(c, x, y, w, h, col):
    c.setFillColor(col); c.rect(x, y, w, h, fill=1, stroke=0)

def rrect(c, x, y, w, h, r, col):
    c.setFillColor(col)
    p = c.beginPath(); p.roundRect(x, y, w, h, r)
    c.drawPath(p, fill=1, stroke=0)

def circ(c, cx, cy, r, col):
    c.setFillColor(col); c.circle(cx, cy, r, fill=1, stroke=0)

def grad_v(c, x, y, w, h, c1, c2, n=50):
    bh = h / n
    for i in range(n):
        t = i / (n - 1)
        c.setFillColor(Color(
            c1.red+(c2.red-c1.red)*t,
            c1.green+(c2.green-c1.green)*t,
            c1.blue+(c2.blue-c1.blue)*t))
        c.rect(x, y+h-(i+1)*bh, w, bh+0.5, fill=1, stroke=0)

def mountains(c, base, peaks, col):
    c.setFillColor(col)
    p = c.beginPath(); p.moveTo(0, base)
    for px, py in peaks:
        p.lineTo(px*mm, base+py*mm)
    p.lineTo(WIDTH, base); p.close()
    c.drawPath(p, fill=1, stroke=0)

def diamond(c, cx, cy, s, col):
    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(cx, cy+s); p.lineTo(cx+s, cy); p.lineTo(cx, cy-s); p.lineTo(cx-s, cy); p.close()
    c.drawPath(p, fill=1, stroke=0)


products = [
    ("M1 Certified U-Shape Seating Frame",
     "Integrated seatbelts & ISOFIX, powder coated", "1,850"),
    ("Kitchen Pod Package (SWB)",
     "Pod, overhead locker & Sequoia table system", "1,249"),
    ("Kitchen Pod Package (LWB)",
     "Pod, overhead locker & Sequoia table system", "1,399"),
    ("Full Upholstery Kit \u2013 Rear Seating",
     "CNC ply, dual density foam, 100+ colours", "1,099"),
    ("Rear Pull-Out Kitchen Pod",
     "Twin burner hob bay, 300L+ storage", "649"),
    ("Rear Pull-Out Drawer Storage",
     "Aluminium, 330L+, 220kg rated runners", "449"),
    ("Central Under Bed Drawer",
     "Aluminium build, 200L+, phenolic ply front", "399"),
    ("Aluminium Overhead Locker",
     "Lightweight, textured black powder coat", "399"),
    ("Powder Coated Front Panels",
     "Aluminium panels for U-Shape frame", "299"),
    ("Cushion Boards & Dual Density Foam",
     "12mm CNC birch ply, shaped foam", "299"),
]


def create_price_list():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ROAM_Systems_Price_List.pdf")
    c = canvas.Canvas(out, pagesize=A4)

    has_barlow = register_fonts()
    H_BOLD  = "Barlow-Bold" if has_barlow else "Helvetica-Bold"
    H_SEMI  = "Barlow-SemiBold" if has_barlow else "Helvetica-Bold"
    B_REG   = "Barlow-Regular" if has_barlow else "Helvetica"
    B_MED   = "Barlow-Medium" if has_barlow else "Helvetica"

    # ── Layout math (bottom-up) ──
    footer_h   = 18 * mm
    compat_h   = 8  * mm
    compat_gap = 3  * mm
    card_h     = 26 * mm
    card_gap   = 3  * mm
    grid_rows  = 5
    margin     = 12 * mm
    gutter     = 4  * mm
    col_w      = (WIDTH - 2*margin - gutter) / 2

    grid_height    = grid_rows * card_h + (grid_rows - 1) * card_gap
    grid_bottom    = footer_h + compat_gap + compat_h + compat_gap
    grid_top       = grid_bottom + grid_height
    title_zone     = 20 * mm
    title_top      = grid_top + title_zone
    bar_h          = 3.5 * mm
    bar_top        = title_top + 2 * mm
    header_bottom  = bar_top + bar_h
    header_height  = HEIGHT - header_bottom

    # ━━ RENDER ━━

    rect(c, 0, 0, WIDTH, HEIGHT, ROAM_DARK)

    # ── HEADER ──
    hb = header_bottom
    grad_v(c, 0, hb, WIDTH, header_height,
           HexColor("#15152A"), HexColor("#2A1A0E"))

    mountains(c, hb + 5*mm,
              [(25,14),(50,6),(75,22),(100,9),(125,18),(150,7),(175,16),(210,4)],
              HexColor("#1A1508"))
    mountains(c, hb,
              [(18,9),(42,3),(68,13),(92,5),(118,11),(142,4),(168,10),(195,2),(210,7)],
              ROAM_DARK)

    grad_v(c, 0, hb, WIDTH, 12*mm,
           Color(0.96, 0.49, 0.14, 0.10), Color(0,0,0,0))

    # ── LOGO (actual PNG from website) ──
    logo_w = 42 * mm
    logo_h = 42 * mm  # square aspect
    logo_x = CX - logo_w / 2
    logo_y = HEIGHT - 8*mm - logo_h

    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, logo_x, logo_y, logo_w, logo_h,
                    preserveAspectRatio=True, mask='auto')
    else:
        # Fallback: text logo
        c.setFillColor(WHITE_T); c.setFont(H_BOLD, 28)
        c.drawCentredString(CX, logo_y + logo_h/2, "ROAM")

    # Tagline below logo
    tag_y = logo_y - 6*mm
    c.setFillColor(GREY_T); c.setFont(B_REG, 7.5)
    c.drawCentredString(CX, tag_y,
                        "C A M P E R V A N   F U R N I T U R E   S P E C I A L I S T S")

    # ── ORANGE ACCENT BAR ──
    grad_v(c, 0, bar_top, WIDTH, bar_h, ROAM_ORANGE_DK, ROAM_ORANGE)

    # ── TITLE ZONE ──
    pty = grid_top + 10*mm
    title = "PRICE LIST"
    c.setFont(H_BOLD, 14)
    tw = c.stringWidth(title, H_BOLD, 14)
    c.setStrokeColor(RULE_COL); c.setLineWidth(0.4)
    c.line(margin, pty+5*mm, CX - tw/2 - 4*mm, pty+5*mm)
    c.line(CX + tw/2 + 4*mm, pty+5*mm, WIDTH-margin, pty+5*mm)
    c.setFillColor(WHITE_T)
    c.drawCentredString(CX, pty, title)

    c.setFillColor(DIM_T); c.setFont(B_REG, 6.2)
    c.drawCentredString(CX, pty - 7*mm,
        "All prices exclude VAT  \u00b7  Delivery calculated on order  \u00b7  Collection available from warehouse")

    # ── PRODUCT GRID ──
    for i, (name, desc, price) in enumerate(products):
        col = i % 2
        row = i // 2
        x = margin + col * (col_w + gutter)
        y = grid_top - (row + 1) * card_h - row * card_gap

        rrect(c, x, y, col_w, card_h, 2*mm, CARD_BG)

        # Top orange accent
        c.setStrokeColor(ROAM_ORANGE); c.setLineWidth(1.5)
        c.line(x + 2*mm, y + card_h, x + col_w - 2*mm, y + card_h)

        # Number badge
        bx = x + 7*mm
        by = y + card_h - 7*mm
        circ(c, bx, by, 3*mm, ROAM_ORANGE)
        c.setFillColor(WHITE_T); c.setFont(H_BOLD, 7)
        c.drawCentredString(bx, by - 1.2*mm, str(i+1).zfill(2))

        # Name
        nx = bx + 6.5*mm
        c.setFillColor(WHITE_T); c.setFont(H_SEMI, 7.8)
        max_w = col_w - 18*mm
        dn = name
        while c.stringWidth(dn, H_SEMI, 7.8) > max_w and len(dn) > 10:
            dn = dn[:-1]
        if dn != name: dn = dn.rstrip() + "\u2026"
        c.drawString(nx, y + card_h - 7.5*mm, dn)

        # Description
        c.setFillColor(GREY_T); c.setFont(B_REG, 6.3)
        dd = desc
        while c.stringWidth(dd, B_REG, 6.3) > max_w and len(dd) > 10:
            dd = dd[:-1]
        if dd != desc: dd = dd.rstrip() + "\u2026"
        c.drawString(nx, y + card_h - 12.5*mm, dd)

        # Thin rule
        c.setStrokeColor(RULE_COL); c.setLineWidth(0.3)
        c.line(x + 4*mm, y + 10*mm, x + col_w - 4*mm, y + 10*mm)

        # Price
        c.setFillColor(ROAM_ORANGE); c.setFont(H_BOLD, 16)
        c.drawRightString(x + col_w - 4.5*mm, y + 3.5*mm, f"\u00a3{price}")

        c.setFillColor(DIM_T); c.setFont(B_REG, 5)
        c.drawRightString(x + col_w - 4.5*mm, y + 0.8*mm, "exc VAT")

    # ── COMPATIBILITY BAR ──
    cy = footer_h + compat_gap
    rrect(c, margin, cy, WIDTH - 2*margin, compat_h, 2*mm, ROAM_GRAY)
    diamond(c, margin + 6.5*mm, cy + compat_h/2, 1.6*mm, ROAM_ORANGE)
    c.setFillColor(GREY_T); c.setFont(B_REG, 6)
    c.drawString(margin + 12*mm, cy + 2.5*mm,
        "Fits:  VW T5 / T6 / T6.1   \u00b7   Ford Transit Custom   \u00b7   Renault Trafic   \u00b7   Nissan Primastar   \u00b7   SWB & LWB")

    # ── FOOTER ──
    rect(c, 0, 0, WIDTH, footer_h, ROAM_GRAY)
    c.setStrokeColor(ROAM_ORANGE); c.setLineWidth(0.7)
    c.line(0, footer_h, WIDTH, footer_h)

    # Small logo in footer left
    footer_logo_h = 12 * mm
    footer_logo_w = 12 * mm
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, margin, footer_h - 15*mm, footer_logo_w, footer_logo_h,
                    preserveAspectRatio=True, mask='auto')

    fl_x = margin + footer_logo_w + 3*mm
    c.setFillColor(WHITE_T); c.setFont(H_SEMI, 7)
    c.drawString(fl_x, footer_h - 5.5*mm, "Roam Systems Ltd")
    c.setFillColor(GREY_T); c.setFont(B_REG, 5.8)
    c.drawString(fl_x, footer_h - 9.5*mm, "Unit 3, 47 King Street, Stanford-Le-Hope, Essex  SS17 0HJ")
    c.setFillColor(DIM_T); c.setFont(B_REG, 5.5)
    c.drawString(fl_x, footer_h - 13*mm, "Registered in England & Wales  \u00b7  Company No. 1318982")

    rx = WIDTH - margin
    c.setFillColor(ROAM_ORANGE); c.setFont(H_SEMI, 7)
    c.drawRightString(rx, footer_h - 5.5*mm, "roamsystems.co.uk")
    c.setFillColor(GREY_T); c.setFont(B_REG, 5.8)
    c.drawRightString(rx, footer_h - 9.5*mm, "sales@roamsystems.co.uk")
    c.drawRightString(rx, footer_h - 13*mm, "01375 809 808   \u00b7   07368 236 765")

    # Bottom orange strip
    rect(c, 0, 0, WIDTH, 1.2*mm, ROAM_ORANGE)

    c.save()
    return out


if __name__ == "__main__":
    print(f"Created: {create_price_list()}")

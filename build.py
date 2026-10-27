#!/usr/bin/env python3
"""Mor teması: Dinamik Ada ve Glass Dock'un mor cam dilinden türetilmiş masaüstü teması.

Üretir:
  ~/.themes/Mor/gtk-3.0     GTK3 uygulamaları (adw-gtk3-dark üstüne renk + köşe)
  ~/.config/gtk-4.0/gtk.css libadwaita uygulamaları (Nautilus, Ayarlar, ...)
  ~/.themes/Mor/gnome-shell Shell (Orchis-Purple-Dark kopyası, renk tonu mora çekilir, köşeler kare)

Palet tek yerde (PALET). Değiştir, yeniden çalıştır:  python3 build.py
Kurulum sonrası:  gsettings set org.gnome.desktop.interface gtk-theme Mor
                  gsettings set org.gnome.shell.extensions.user-theme name Mor
"""
import colorsys
import re
import shutil
from pathlib import Path

from tema import recolor_css  # the chosen colour theme (tema-rengi); violet = unchanged

HOME = Path.home()
OUT = HOME / ".themes/Mor"
GTK4 = HOME / ".config/gtk-4.0"
def _find_theme(name, sub):
    """A theme installed per user or system-wide (Orchis and adw-gtk3 are dependencies)."""
    for root in (HOME / ".themes", HOME / ".local/share/themes", Path("/usr/share/themes")):
        if (root / name / sub).exists():
            return root / name / sub
    return HOME / ".local/share/themes" / name / sub


SHELL_SRC = _find_theme("Orchis-Purple-Dark", "gnome-shell")
ADW_GTK3 = _find_theme("adw-gtk3-dark", "gtk-3.0/gtk.css")

# Adanın camı rgba(27,22,44), çerçevesi lavanta rgba(168,132,255), robotun morları.
PALET = {
    "window_bg": "#161221",
    "view_bg": "#120f1b",
    "headerbar_bg": "#1b162c",
    "sidebar_bg": "#18142a",
    "popover_bg": "#201b30",
    "card_bg": "rgba(255, 255, 255, 0.045)",
    "fg": "#eeebf7",
    "accent_bg": "#6f55d6",
    "accent": "#b39cff",
    "accent_fg": "#ffffff",
    "line": "rgba(168, 132, 255, 0.16)",
    "frame": "rgba(168, 132, 255, 0.55)",
    "destructive": "#ff4f6b",
    "success": "#3ed6a0",
    "warning": "#ff9f0a",
}
P = PALET

# ---------- Pah: adadaki gibi 45° kesik köşe ----------
# GTK CSS'te maske yok; köşeyi dört çeyrekte "transparent → dolgu" sert geçişli gradyanla
# kesiyoruz. Çeyrekler ortada üst üste bindiği için dolgu OPAK olmalı (yarı saydam
# renk ortada çizgi bırakır) — renkler paletin koyu morunun üstüne önceden karıştırıldı.
# Çerçeveli halde çerçeve katmanı border-box'a, dolgu padding-box'a çizilir; 1 px saydam
# kenarlık aradaki çizgiyi bırakır. Pencerenin kendi köşesi Glass Windows eklentisinde (shader).
KOSE = [(135, "left top"), (225, "right top"), (315, "right bottom"), (45, "left bottom")]


def pah(fill, cut=4, frame=None):
    def kat(renk, c):
        return [f"linear-gradient({a}deg, transparent {c:g}px, {renk} {c:g}px)" for a, _ in KOSE]
    imgs = kat(fill, cut - 0.41 if frame else cut)
    poz = [p for _, p in KOSE]
    css = "background-color: transparent; border-radius: 0; box-shadow: none; "
    if frame:
        imgs += kat(frame, cut)
        css += ("border: 1px solid transparent; "
                f"background-clip: {', '.join(['padding-box'] * 4 + ['border-box'] * 4)}; "
                f"background-origin: {', '.join(['padding-box'] * 4 + ['border-box'] * 4)}; ")
        poz *= 2
    return (css + f"background-image: {', '.join(imgs)}; background-size: 51% 51%; "
            f"background-repeat: no-repeat; background-position: {', '.join(poz)};")


# Opak dolgular (zemin #161221 / başlık #1b162c üstüne karıştırılmış)
D = {
    "btn": "#2a2340", "btn_hover": "#342b50", "btn_active": "#40355f",
    "accent_hover": "#7d64e0", "accent_active": "#5e46c4",
    "destr": "#c43a52", "destr_hover": "#d8445e",
    "entry": "#211b33", "entry_frame": "#2f2747", "entry_focus": "#8a70ec",
    "card": "#1e192c", "card_frame": "#2a2340",
    "pop": P["popover_bg"], "pop_frame": "#4a3d74",
    "sel": "#2b2344", "sel_frame": "#6a56b0", "sel_hover": "#332a50",
    "grid_hover": "#1d1829",
    "ctl_hover": "#3a3058",
}

PAH_CSS = f"""/* Pah: düğme, alan, kart, menü — adadaki 45° kesik */
button {{ {pah(D['btn'])} }}
button.flat, headerbar button, .toolbar button, toolbarview > .top button, spinbutton > button,
.path-bar button, searchbar button, popover button.flat, splitbutton > button,
splitbutton > menubutton > button, columnview > header button, columnview header > row > button,
columnview > header > row > button, .column-header {{ {pah("transparent")} }}
button:hover {{ {pah(D['btn_hover'])} }}
button:active, button:checked {{ {pah(D['btn_active'])} }}
button.suggested-action, button.default {{ {pah(P['accent_bg'])} color: {P['accent_fg']}; }}
button.suggested-action:hover {{ {pah(D['accent_hover'])} }}
button.suggested-action:active {{ {pah(D['accent_active'])} }}
button.destructive-action {{ {pah(D['destr'])} color: #ffffff; }}
button.destructive-action:hover {{ {pah(D['destr_hover'])} }}
button:disabled {{ opacity: 0.5; }}

entry, searchbar entry, spinbutton, .path-bar-box, .nautilus-path-bar {{ {pah(D['entry'], 4, D['entry_frame'])} outline: none; }}
entry:focus-within, spinbutton:focus-within {{ {pah(D['entry'], 4, D['entry_focus'])} }}

.card, list.boxed-list, .boxed-list {{ {pah(D['card'], 6, D['card_frame'])} }}

popover > contents, popover.menu > contents {{ {pah(D['pop'], 7, D['pop_frame'])} }}
popover > arrow {{ background-color: {D['pop']}; border-color: {D['pop_frame']}; }}

.navigation-sidebar > row:selected, placessidebar row:selected {{ {pah(D['sel'], 4, D['sel_frame'])} color: {P['fg']}; }}
.navigation-sidebar > row:selected:hover {{ {pah(D['sel_hover'], 4, D['sel_frame'])} }}

gridview > child:hover {{ {pah(D['grid_hover'], 5)} }}
gridview > child:selected, columnview > listview > row:selected {{ {pah(D['sel'], 5, D['sel_frame'])} }}
gridview > child .thumbnail, .icon-ui-labels-box {{ border-radius: 0; }}

/* Pencere gölgesi GTK varsayılanı: büyütülmüş gölge Zen ve masaüstünde (DING) fare koordinatlarını kaydırdı (2026-10-26) */

/* Pencere düğmeleri: macOS trafik ışığı yok; pahlı, sessiz; kapat üstüne gelince kırmızı */
windowcontrols button {{ {pah('transparent')} min-width: 28px; min-height: 28px; padding: 0; margin: 0 1px; }}
windowcontrols button image {{ background: none; box-shadow: none; padding: 5px; border-radius: 0; }}
windowcontrols button:hover {{ {pah(D['ctl_hover'], 5)} }}
windowcontrols button.close:hover {{ {pah(P['destructive'], 5)} color: #ffffff; }}

/* Nautilus liste görünümü: Windows Gezgini "Ayrıntılar" gibi ince satırlar (2026-10-26) */
.nautilus-list-view columnview > listview > row {{ min-height: 0; padding-top: 0; padding-bottom: 0; margin-left: 8px; margin-right: 8px; }}
.nautilus-list-view columnview > listview > row > cell {{ padding: 0; min-height: 0; }}
.nautilus-list-view .nautilus-view-cell, .nautilus-list-view.compact .nautilus-view-cell {{ padding: 2px 8px; min-height: 22px; }}
.nautilus-list-view button.star {{ min-height: 0; min-width: 0; padding: 0 4px; margin: 0; }}
.nautilus-list-view columnview > listview > row:hover {{ {pah(D['grid_hover'], 3)} }}
.nautilus-list-view columnview > listview > row:selected {{ {pah(D['sel'], 3, D['sel_frame'])} }}
.nautilus-list-view columnview > header > row > button {{ padding: 4px 8px; min-height: 0; font-weight: 400; }}
.nautilus-list-view columnview > header > row > button:not(:last-child) {{ box-shadow: inset -1px 0 {P['line']}; }}
.nautilus-list-view .thumbnail, .nautilus-list-view image {{ -gtk-icon-size: 16px; }}
"""


# İmza: kare köşe (Umut adada "radius'suz hali daha güzeldi" dedi, 2026-10-13) ve
# seçili satırın solunda lavanta çizgi.
GTK4_CSS = f"""/* Mor — üretildi: ~/.local/src/mor-theme/build.py, elle düzenleme */
:root {{
  --window-radius: 0px;
  --accent-bg-color: {P['accent_bg']};
  --accent-fg-color: {P['accent_fg']};
  --accent-color: {P['accent']};
  --destructive-bg-color: {P['destructive']};
  --destructive-color: {P['destructive']};
  --success-bg-color: #23a87a;
  --success-color: {P['success']};
  --warning-bg-color: #d98500;
  --warning-color: {P['warning']};
  --error-bg-color: {P['destructive']};
  --error-color: {P['destructive']};

  --window-bg-color: {P['window_bg']};
  --window-fg-color: {P['fg']};
  --view-bg-color: {P['view_bg']};
  --view-fg-color: {P['fg']};
  --headerbar-bg-color: {P['headerbar_bg']};
  --headerbar-fg-color: {P['fg']};
  --headerbar-backdrop-color: {P['window_bg']};
  --headerbar-border-color: {P['line']};
  --headerbar-shade-color: {P['line']};
  --sidebar-bg-color: {P['sidebar_bg']};
  --sidebar-fg-color: {P['fg']};
  --sidebar-backdrop-color: {P['window_bg']};
  --sidebar-border-color: {P['line']};
  --sidebar-shade-color: {P['line']};
  --secondary-sidebar-bg-color: {P['window_bg']};
  --secondary-sidebar-fg-color: {P['fg']};
  --secondary-sidebar-backdrop-color: {P['window_bg']};
  --secondary-sidebar-border-color: {P['line']};
  --card-bg-color: {P['card_bg']};
  --card-fg-color: {P['fg']};
  --card-shade-color: rgba(0, 0, 0, 0.36);
  --dialog-bg-color: {P['popover_bg']};
  --dialog-fg-color: {P['fg']};
  --popover-bg-color: {P['popover_bg']};
  --popover-fg-color: {P['fg']};
  --popover-shade-color: rgba(0, 0, 0, 0.4);
  --thumbnail-bg-color: {P['popover_bg']};
  --thumbnail-fg-color: {P['fg']};
  --overview-bg-color: {P['view_bg']};
  --overview-fg-color: {P['fg']};
  --border-color: {P['line']};
  --scrollbar-outline-color: rgba(0, 0, 0, 0.4);
}}

/* Kare köşe */
button, entry, spinbutton, dropdown > button, combobox > box > button,
.card, list.boxed-list, .boxed-list, row, popover > contents, popover > arrow,
menu, .menu, tooltip, toast, .osd, frame, scrollbar slider, switch, switch > slider,
progressbar trough, progressbar progress, scale trough, scale highlight,
windowcontrols button, tabbox tab, tab, .navigation-sidebar > row,
placessidebar row, searchbar entry, .linked > *, viewswitcher button,
dialog.alert .dialog-contents, window.dialog.message, .background.csd,
window.csd, window.solid-csd, sheet, floating-sheet > sheet, banner > revealer > widget,
checkbutton check, check, .path-bar-box, .nautilus-path-bar, .path-bar button,
searchbar > revealer > box entry {{ border-radius: 0; }}
radio, checkbutton radio, scale slider, button.circular, avatar {{ border-radius: 999px; }}

{PAH_CSS}
/* Odak halkası lavanta */
*:focus-visible {{ outline-color: {P['frame']}; outline-width: 1px; }}
"""

GTK3_COLORS = f"""@define-color accent_bg_color {P['accent_bg']};
@define-color accent_fg_color {P['accent_fg']};
@define-color accent_color {P['accent']};
@define-color destructive_bg_color {P['destructive']};
@define-color destructive_color {P['destructive']};
@define-color success_color {P['success']};
@define-color warning_color {P['warning']};
@define-color error_color {P['destructive']};
@define-color window_bg_color {P['window_bg']};
@define-color window_fg_color {P['fg']};
@define-color view_bg_color {P['view_bg']};
@define-color view_fg_color {P['fg']};
@define-color headerbar_bg_color {P['headerbar_bg']};
@define-color headerbar_fg_color {P['fg']};
@define-color headerbar_backdrop_color {P['window_bg']};
@define-color headerbar_border_color {P['line']};
@define-color sidebar_bg_color {P['sidebar_bg']};
@define-color sidebar_fg_color {P['fg']};
@define-color sidebar_backdrop_color {P['window_bg']};
@define-color card_bg_color {P['card_bg']};
@define-color card_fg_color {P['fg']};
@define-color dialog_bg_color {P['popover_bg']};
@define-color dialog_fg_color {P['fg']};
@define-color popover_bg_color {P['popover_bg']};
@define-color popover_fg_color {P['fg']};
@define-color borders {P['line']};
"""

GTK3_CSS = f"""/* Mor — üretildi: ~/.local/src/mor-theme/build.py, elle düzenleme */
@import url("file://{ADW_GTK3}");
{GTK3_COLORS}
button, entry, spinbutton, combobox button, .linked > *, popover, menu, .menu,
tooltip, frame, scrollbar slider, switch, switch slider, progressbar trough,
progressbar progress, scale trough, scale highlight, list, row, notebook tab,
decoration, window, .titlebar, headerbar, check {{ border-radius: 0; }}
radio, scale slider, button.circular {{ border-radius: 999px; }}
placessidebar row:selected, .navigation-sidebar row:selected {{
  background-color: rgba(168, 132, 255, 0.12); box-shadow: inset 2px 0 {P['accent']}; color: {P['fg']};
}}
"""


# ---------- Shell: Orchis'i mora çek ----------

HEDEF_TON = 258 / 360  # #a884ff'nin tonu


def ton(r, g, b):
    """Doygun rengi lavanta tonuna, griyi hafif mora çeker; açıklığı korur."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if s > 0.2:
        h, s = HEDEF_TON, min(1.0, s * 1.05)
    elif l < 0.5:
        h, s = HEDEF_TON, 0.28  # koyu gri -> mor-siyah (ada camı #1b162c gibi)
    elif l < 0.92:
        h, s = HEDEF_TON, 0.12
    return tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, l, s))


def hex_degis(m):
    v = m.group(1)
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    r, g, b = ton(*(int(v[i:i + 2], 16) for i in (0, 2, 4)))
    return f"#{r:02x}{g:02x}{b:02x}"


def rgba_degis(m):
    r, g, b = (int(x) for x in m.group(1, 2, 3))
    if (r, g, b) in ((255, 255, 255), (0, 0, 0)):
        return m.group(0)  # saydam beyaz/siyah katmanlar kalsın
    r, g, b = ton(r, g, b)
    return f"rgba({r}, {g}, {b}, {m.group(4)})"


def renklendir(metin):
    metin = re.sub(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", hex_degis, metin)
    return re.sub(r"rgba\(\s*(\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\s*\)", rgba_degis, metin)


def kare(metin):
    # Küçük yarıçaplar sıfır; yuvarlak öğeler (>=50px, düğme halkaları, anahtarlar) kalır.
    def f(m):
        n = float(m.group(1))
        return m.group(0) if n >= 50 else "border-radius: 0"
    return re.sub(r"border-radius:\s*([\d.]+)px", f, metin)


SHELL_EK = f"""
/* Mor ekleri */
/* Orchis'in #panel margin'i (3px) Dinamik Ada'nın "panel" adlı kutularına geçiyor; gizli
   göstergeler (Etkinlikler, erişilebilirlik, klavye) sıfır yerine 6px kalıp boş kutu oluyordu. */
#panel {{ background-color: rgba(18, 15, 27, 0.72); margin: 0; }}
.popup-menu-content, .candidate-popup-content, .modal-dialog, .quick-settings,
.message-list, .calendar, .datemenu-popover {{
  border: 1px solid {P['line']};
}}
.app-well-app:focus .overview-icon, .grid-search-result:focus .overview-icon {{
  border: 1px solid {P['frame']};
}}
"""


def koyu_menu(metin):
    """Orchis 'Dark' bile hızlı ayar alt menülerini (Güç, Wi-Fi listesi…) beyaz zemin + siyah
    yazıyla !important çiziyor; Dinamik Ada zemini koyu cama çevirince yazı siyah kalıyordu
    (Umut, 2026-10-26). Bu bloklarda siyah→açık lavanta-beyaz, beyaz zemin→menü moru."""
    def blok(m):
        sec, govde = m.group(1), m.group(2)
        if "quick-toggle-menu" not in sec:
            return m.group(0)
        def rgba(mm):
            prop, a = mm.group(1), float(mm.group(2))
            if "background" in prop or "border" in prop:
                return f"{prop}: rgba(255, 255, 255, {round(a * 0.8, 2)})"
            return f"{prop}: rgba(238, 235, 247, {min(1.0, round(a + 0.2, 2))})"
        govde = re.sub(r"([\w-]+):\s*rgba\(0, 0, 0, ([\d.]+)\)", rgba, govde)
        govde = re.sub(r"background-color:\s*white", f"background-color: {P['popover_bg']}", govde)
        return sec + "{" + govde + "}"
    return re.sub(r"([^{}]+)\{([^}]*)\}", blok, metin)


def shell():
    hedef = OUT / "gnome-shell"
    if hedef.exists():
        shutil.rmtree(hedef)
    shutil.copytree(SHELL_SRC, hedef)
    for f in hedef.rglob("*"):
        if f.suffix in (".css", ".svg"):
            t = renklendir(f.read_text())
            if f.suffix == ".css":
                t = koyu_menu(kare(t))
                if f.name == "gnome-shell.css":
                    t += SHELL_EK
            f.write_text(recolor_css(t))


def main():
    (OUT / "gtk-3.0").mkdir(parents=True, exist_ok=True)
    (OUT / "gtk-4.0").mkdir(parents=True, exist_ok=True)
    (OUT / "index.theme").write_text(
        "[Desktop Entry]\nType=X-GNOME-Metatheme\nName=Mor\nComment=Umut'un mor cam teması\n"
        "\n[X-GNOME-Metatheme]\nGtkTheme=Mor\nIconTheme=Mor\n")
    for n in ("gtk.css", "gtk-dark.css"):
        (OUT / "gtk-3.0" / n).write_text(recolor_css(GTK3_CSS))
        (OUT / "gtk-4.0" / n).write_text(recolor_css(GTK4_CSS))
    for n in ("gtk.css", "gtk-dark.css"):
        p = GTK4 / n
        if p.is_symlink() or p.exists():
            p.unlink()
        p.write_text(recolor_css(GTK4_CSS))
    shell()
    print("Mor teması yazıldı:", OUT, GTK4)


if __name__ == "__main__":
    main()

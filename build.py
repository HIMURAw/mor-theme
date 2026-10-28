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

from tema import current, recolor_css  # the chosen colour theme (tema-rengi); violet = unchanged

# Glass (cam) changes shape as well as colour: rounded frosted glass from the Cam Panel design
# instead of the 45° chamfers. Every other theme keeps the chamfered, square Mor build untouched.
ROUND = bool(current().get("round"))

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


# ---------- Glass (cam): rounded white frost, from the Cam Panel design ----------
# GTK has no backdrop blur, so the "glass" is a cool, near-opaque night surface with white
# overlays on top (the panel's .glass recipe: 160° white gradient, white .17 hairline, inset
# top highlight). Shapes: buttons/tabs/toggles pill, entries and rows 12px, cards 22px,
# popovers 18px, windows 12px. These colours are final: the cam CSS is not run through recolor().
C = {
    "window_bg": "#141824", "view_bg": "#11141e", "headerbar_bg": "#171b28",
    "sidebar_bg": "#151925", "popover_bg": "#1b1f2d", "dialog_bg": "#1b1f2d",
    "ink": "#f4f1ff", "ink2": "rgba(244, 241, 255, 0.66)", "ink3": "rgba(244, 241, 255, 0.42)",
    "accent": "#8fb4ff", "accent_fg": "#101a33", "accent_hover": "#a3c2ff", "accent_active": "#7ba3f2",
    "good": "#6fe0a6", "bad": "#ff8f8f", "bad_fg": "#2b0f14", "warm": "#f0a868",
    "line": "rgba(255, 255, 255, 0.10)", "line_hi": "rgba(255, 255, 255, 0.17)",
    "fill": "rgba(255, 255, 255, 0.08)", "hover": "rgba(255, 255, 255, 0.10)",
    "sel": "rgba(255, 255, 255, 0.16)",
    "frost": "linear-gradient(160deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.085) 40%)",
    "hi": "inset 0 1px 0 rgba(255, 255, 255, 0.18)",
    "sel_hi": "inset 0 1px 0 rgba(255, 255, 255, 0.20)",
    "shadow": "0 20px 50px -20px rgba(10, 8, 30, 0.35)",
}

ROUND_CSS = f"""/* Glass: rounded shapes */
button, dropdown > button, combobox > box > button, menubutton > button, splitbutton > button,
splitbutton > menubutton > button, viewswitcher button, tabbox tab, tab, windowcontrols button,
switch, switch > slider, progressbar trough, progressbar progress, scale trough, scale highlight,
scrollbar slider, radio, checkbutton radio, scale slider, button.circular, avatar, .linked > *,
toast, .osd {{ border-radius: 999px; }}
entry, spinbutton, searchbar entry, searchbar > revealer > box entry, .path-bar-box, .nautilus-path-bar,
.path-bar button, row, menu, .menu, frame, banner > revealer > widget {{ border-radius: 12px; }}
checkbutton check, check {{ border-radius: 6px; }}
tooltip {{ border-radius: 10px; }}
popover > contents, popover.menu > contents {{ border-radius: 18px; }}
popover modelbutton, popover.menu modelbutton {{ border-radius: 10px; }}
.card, list.boxed-list, .boxed-list, dialog.alert .dialog-contents, window.dialog.message,
sheet, floating-sheet > sheet {{ border-radius: 22px; }}
list.boxed-list > row:first-child, .boxed-list > row:first-child {{ border-top-left-radius: 22px; border-top-right-radius: 22px; }}
list.boxed-list > row:last-child, .boxed-list > row:last-child {{ border-bottom-left-radius: 22px; border-bottom-right-radius: 22px; }}
list.boxed-list > row:not(:first-child), .boxed-list > row:not(:first-child) {{ border-top-left-radius: 0; border-top-right-radius: 0; }}
list.boxed-list > row:not(:last-child), .boxed-list > row:not(:last-child) {{ border-bottom-left-radius: 0; border-bottom-right-radius: 0; }}
.linked:not(.vertical) > *:not(:first-child) {{ border-top-left-radius: 0; border-bottom-left-radius: 0; }}
.linked:not(.vertical) > *:not(:last-child) {{ border-top-right-radius: 0; border-bottom-right-radius: 0; }}

/* Glass: frost surfaces */
button {{ background-color: {C['fill']}; box-shadow: {C['hi']}; color: {C['ink']}; }}
button.flat, headerbar button, .toolbar button, toolbarview > .top button, spinbutton > button,
.path-bar button, searchbar button, popover button.flat, columnview > header button,
columnview header > row > button, columnview > header > row > button, .column-header {{
  background-color: transparent; box-shadow: none; }}
button:hover, button.flat:hover, headerbar button:hover {{ background-color: {C['hover']}; }}
button:active, button:checked, button.flat:checked, headerbar button:checked {{
  background-color: {C['sel']}; box-shadow: {C['sel_hi']}; }}
button.suggested-action, button.default {{ background-color: {C['accent']}; color: {C['accent_fg']}; box-shadow: none; }}
button.suggested-action:hover {{ background-color: {C['accent_hover']}; }}
button.suggested-action:active {{ background-color: {C['accent_active']}; }}
button.destructive-action {{ background-color: {C['bad']}; color: {C['bad_fg']}; box-shadow: none; }}
button.destructive-action:hover {{ background-color: #ffa3a3; }}
button:disabled {{ opacity: 0.5; }}

entry, searchbar entry, spinbutton, .path-bar-box, .nautilus-path-bar {{
  background-color: rgba(255, 255, 255, 0.07); border: 1px solid {C['line_hi']}; box-shadow: none; outline: none; }}
entry:focus-within, spinbutton:focus-within {{ border-color: {C['accent']}; background-color: rgba(255, 255, 255, 0.09); }}

.card, list.boxed-list, .boxed-list {{
  background-color: rgba(255, 255, 255, 0.04); background-image: {C['frost']};
  border: 1px solid {C['line_hi']}; box-shadow: {C['hi']}; }}
.card.activatable:hover, list.boxed-list > row.activatable:hover {{ background-color: {C['hover']}; }}

popover > contents, popover.menu > contents {{
  background-color: {C['popover_bg']}; background-image: {C['frost']};
  border: 1px solid {C['line_hi']}; box-shadow: {C['hi']}, 0 4px 14px rgba(0, 0, 0, 0.3); }}
popover > arrow {{ background-color: {C['popover_bg']}; border-color: {C['line_hi']}; }}
popover modelbutton:hover, popover.menu modelbutton:hover, popover.menu modelbutton:selected {{ background-color: {C['hover']}; }}
tooltip, tooltip.background {{ background-color: rgba(18, 15, 36, 0.92); border: 1px solid {C['line_hi']}; color: {C['ink']}; }}

.navigation-sidebar > row, placessidebar row {{ border-radius: 999px; }}
.navigation-sidebar > row:hover, placessidebar row:hover {{ background-color: {C['hover']}; }}
.navigation-sidebar > row:selected, placessidebar row:selected {{
  background-color: {C['sel']}; box-shadow: {C['sel_hi']}; color: {C['ink']}; }}

gridview > child {{ border-radius: 14px; }}
gridview > child:hover {{ background-color: {C['hover']}; }}
gridview > child:selected, columnview > listview > row:selected, listview > row:selected,
list > row:selected {{ background-color: {C['sel']}; box-shadow: {C['sel_hi']}; color: {C['ink']}; }}
columnview > listview > row, listview > row {{ border-radius: 10px; }}
gridview > child .thumbnail, .icon-ui-labels-box {{ border-radius: 10px; }}

switch {{ background-color: rgba(255, 255, 255, 0.14); border: none; }}
switch:checked {{ background-color: {C['accent']}; }}
switch > slider {{ background-color: {C['ink']}; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35); }}
progressbar trough, scale trough {{ background-color: rgba(255, 255, 255, 0.10); }}
progressbar progress, scale highlight {{ background-color: {C['accent']}; }}
tabbox tab:selected, tab:selected, viewswitcher button:checked {{ background-color: {C['sel']}; box-shadow: {C['sel_hi']}; }}

/* Window buttons: round, quiet; close turns soft red on hover */
windowcontrols button {{ background-color: transparent; box-shadow: none; min-width: 28px; min-height: 28px; padding: 0; margin: 0 2px; }}
windowcontrols button image {{ background: none; box-shadow: none; padding: 5px; border-radius: 999px; }}
windowcontrols button:hover {{ background-color: {C['hover']}; }}
windowcontrols button.close:hover {{ background-color: {C['bad']}; color: {C['bad_fg']}; }}

/* Nautilus list view: thin rows like Explorer "Details" (same as Mor), rounded selection */
.nautilus-list-view columnview > listview > row {{ min-height: 0; padding-top: 0; padding-bottom: 0; margin-left: 8px; margin-right: 8px; }}
.nautilus-list-view columnview > listview > row > cell {{ padding: 0; min-height: 0; }}
.nautilus-list-view .nautilus-view-cell, .nautilus-list-view.compact .nautilus-view-cell {{ padding: 2px 8px; min-height: 22px; }}
.nautilus-list-view button.star {{ min-height: 0; min-width: 0; padding: 0 4px; margin: 0; }}
.nautilus-list-view columnview > listview > row:hover {{ background-color: {C['hover']}; }}
.nautilus-list-view columnview > header > row > button {{ padding: 4px 8px; min-height: 0; font-weight: 400; border-radius: 8px; }}
.nautilus-list-view .thumbnail, .nautilus-list-view image {{ -gtk-icon-size: 16px; }}
"""

GTK4_CAM = f"""/* Mor (Glass) — üretildi: ~/.local/src/mor-theme/build.py, elle düzenleme */
:root {{
  --window-radius: 12px;
  --accent-bg-color: {C['accent']};
  --accent-fg-color: {C['accent_fg']};
  --accent-color: {C['accent']};
  --destructive-bg-color: {C['bad']};
  --destructive-fg-color: {C['bad_fg']};
  --destructive-color: {C['bad']};
  --success-bg-color: {C['good']};
  --success-fg-color: #0d2a1c;
  --success-color: {C['good']};
  --warning-bg-color: {C['warm']};
  --warning-fg-color: #2a1a08;
  --warning-color: {C['warm']};
  --error-bg-color: {C['bad']};
  --error-fg-color: {C['bad_fg']};
  --error-color: {C['bad']};

  --window-bg-color: {C['window_bg']};
  --window-fg-color: {C['ink']};
  --view-bg-color: {C['view_bg']};
  --view-fg-color: {C['ink']};
  --headerbar-bg-color: {C['headerbar_bg']};
  --headerbar-fg-color: {C['ink']};
  --headerbar-backdrop-color: {C['window_bg']};
  --headerbar-border-color: {C['line']};
  --headerbar-shade-color: {C['line']};
  --sidebar-bg-color: {C['sidebar_bg']};
  --sidebar-fg-color: {C['ink']};
  --sidebar-backdrop-color: {C['window_bg']};
  --sidebar-border-color: {C['line']};
  --sidebar-shade-color: {C['line']};
  --secondary-sidebar-bg-color: {C['window_bg']};
  --secondary-sidebar-fg-color: {C['ink']};
  --secondary-sidebar-backdrop-color: {C['window_bg']};
  --secondary-sidebar-border-color: {C['line']};
  --card-bg-color: rgba(255, 255, 255, 0.085);
  --card-fg-color: {C['ink']};
  --card-shade-color: rgba(10, 8, 30, 0.35);
  --dialog-bg-color: {C['dialog_bg']};
  --dialog-fg-color: {C['ink']};
  --popover-bg-color: {C['popover_bg']};
  --popover-fg-color: {C['ink']};
  --popover-shade-color: rgba(10, 8, 30, 0.35);
  --thumbnail-bg-color: {C['popover_bg']};
  --thumbnail-fg-color: {C['ink']};
  --overview-bg-color: {C['view_bg']};
  --overview-fg-color: {C['ink']};
  --border-color: {C['line_hi']};
  --scrollbar-outline-color: rgba(0, 0, 0, 0.4);
}}

{ROUND_CSS}
/* Focus ring: accent, 2px */
*:focus-visible {{ outline-color: {C['accent']}; outline-width: 2px; }}
"""

GTK3_CAM = f"""/* Mor (Glass) — üretildi: ~/.local/src/mor-theme/build.py, elle düzenleme */
@import url("file://{ADW_GTK3}");
@define-color accent_bg_color {C['accent']};
@define-color accent_fg_color {C['accent_fg']};
@define-color accent_color {C['accent']};
@define-color destructive_bg_color {C['bad']};
@define-color destructive_fg_color {C['bad_fg']};
@define-color destructive_color {C['bad']};
@define-color success_color {C['good']};
@define-color warning_color {C['warm']};
@define-color error_color {C['bad']};
@define-color window_bg_color {C['window_bg']};
@define-color window_fg_color {C['ink']};
@define-color view_bg_color {C['view_bg']};
@define-color view_fg_color {C['ink']};
@define-color headerbar_bg_color {C['headerbar_bg']};
@define-color headerbar_fg_color {C['ink']};
@define-color headerbar_backdrop_color {C['window_bg']};
@define-color headerbar_border_color {C['line']};
@define-color sidebar_bg_color {C['sidebar_bg']};
@define-color sidebar_fg_color {C['ink']};
@define-color sidebar_backdrop_color {C['window_bg']};
@define-color card_bg_color rgba(255, 255, 255, 0.085);
@define-color card_fg_color {C['ink']};
@define-color dialog_bg_color {C['dialog_bg']};
@define-color dialog_fg_color {C['ink']};
@define-color popover_bg_color {C['popover_bg']};
@define-color popover_fg_color {C['ink']};
@define-color borders {C['line_hi']};
button, combobox button, notebook tab, switch, switch slider, progressbar trough, progressbar progress,
scale trough, scale highlight, scrollbar slider, radio, scale slider, button.circular {{ border-radius: 999px; }}
entry, spinbutton, list, row, frame, menu, .menu {{ border-radius: 12px; }}
popover, tooltip {{ border-radius: 14px; }}
decoration, window, .titlebar, headerbar {{ border-radius: 12px 12px 0 0; }}
check {{ border-radius: 6px; }}
.linked:not(.vertical) > *:not(:first-child) {{ border-top-left-radius: 0; border-bottom-left-radius: 0; }}
.linked:not(.vertical) > *:not(:last-child) {{ border-top-right-radius: 0; border-bottom-right-radius: 0; }}
button {{ background-color: {C['fill']}; background-image: none; box-shadow: {C['hi']}; }}
button.flat, headerbar button, .titlebar button {{ background-color: transparent; box-shadow: none; }}
button:hover {{ background-color: {C['hover']}; }}
button:active, button:checked {{ background-color: {C['sel']}; box-shadow: {C['sel_hi']}; }}
button.suggested-action {{ background-color: {C['accent']}; color: {C['accent_fg']}; }}
button.destructive-action {{ background-color: {C['bad']}; color: {C['bad_fg']}; }}
entry {{ background-color: rgba(255, 255, 255, 0.07); border: 1px solid {C['line_hi']}; box-shadow: none; }}
entry:focus {{ border-color: {C['accent']}; }}
popover, menu, .menu {{ background-color: {C['popover_bg']}; border: 1px solid {C['line_hi']}; }}
placessidebar row, .navigation-sidebar row {{ border-radius: 999px; }}
placessidebar row:selected, .navigation-sidebar row:selected, list row:selected {{
  background-color: {C['sel']}; box-shadow: {C['sel_hi']}; color: {C['ink']};
}}
switch:checked, progressbar progress, scale highlight {{ background-color: {C['accent']}; }}
"""

# Orchis is rounded already (kare() is skipped for cam); these rules put the frost on top.
SHELL_CAM = f"""
/* Glass (cam) ekleri: frost surfaces, rounded, Cam Panel colours (not recoloured) */
#panel {{ background-color: rgba(18, 15, 36, 0.45); margin: 0; }}
.popup-menu .popup-menu-content, .candidate-popup-content, .modal-dialog, .quick-settings,
.datemenu-popover, .switcher-list, .workspace-switcher-container, .resize-popup, .osd-window,
.osd-monitor-label {{
  background-color: rgba(26, 23, 48, 0.92) !important;
  border: 1px solid {C['line_hi']} !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18);
  color: {C['ink']};
}}
.popup-menu .popup-menu-content, .candidate-popup-content, .switcher-list, .workspace-switcher-container,
.resize-popup, .osd-monitor-label {{ border-radius: 18px !important; }}
.quick-settings, .datemenu-popover, .modal-dialog {{ border-radius: 22px !important; }}
.osd-window {{ border-radius: 999px !important; }}
.popup-menu .popup-menu-item {{ border-radius: 12px; color: {C['ink']} !important; }}
.popup-menu .popup-menu-item:hover, .popup-menu .popup-menu-item:focus, .popup-menu .popup-menu-item.selected {{
  background-color: {C['hover']} !important; }}
.popup-menu .popup-menu-item:checked, .popup-menu .popup-menu-item:checked:hover,
.popup-menu .popup-menu-item:checked:focus, .popup-menu .popup-menu-item:checked.selected,
.popup-menu .popup-menu-item:checked:active {{
  background-color: {C['sel']} !important; color: {C['ink']} !important; }}
.popup-sub-menu {{ background-color: rgba(255, 255, 255, 0.05) !important; border-radius: 0 0 12px 12px; }}
.quick-toggle {{ background-color: {C['fill']} !important; color: {C['ink']} !important; }}
.quick-toggle:hover {{ background-color: {C['sel']} !important; }}
.quick-toggle:checked, .quick-toggle:checked:hover, .quick-toggle:checked:active,
.quick-toggle-has-menu .quick-toggle-menu-button:checked,
.quick-toggle-has-menu .quick-toggle-menu-button:checked:hover {{
  background-color: {C['accent']} !important; color: {C['accent_fg']} !important; }}
.quick-toggle-menu {{
  background-color: rgba(255, 255, 255, 0.06) !important; color: {C['ink']} !important;
  border: 1px solid {C['line']}; border-radius: 18px !important; }}
.quick-toggle-menu .popup-menu-item, .quick-toggle-menu .header .title,
.quick-toggle-menu .header .subtitle {{ color: {C['ink']} !important; }}
.slider {{ -barlevel-active-background-color: {C['accent']}; -barlevel-background-color: rgba(255, 255, 255, 0.16); }}
.modal-dialog .modal-dialog-button, .button {{ border-radius: 999px; }}
.app-well-app:focus .overview-icon, .grid-search-result:focus .overview-icon {{ border: 2px solid {C['accent']}; }}
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
                t = koyu_menu(t if ROUND else kare(t))
                if f.name == "gnome-shell.css":
                    t += SHELL_EK
            t = recolor_css(t)
            if ROUND and f.name == "gnome-shell.css":
                t += SHELL_CAM
            f.write_text(t)


def main():
    (OUT / "gtk-3.0").mkdir(parents=True, exist_ok=True)
    (OUT / "gtk-4.0").mkdir(parents=True, exist_ok=True)
    (OUT / "index.theme").write_text(
        "[Desktop Entry]\nType=X-GNOME-Metatheme\nName=Mor\nComment=Umut'un mor cam teması\n"
        "\n[X-GNOME-Metatheme]\nGtkTheme=Mor\nIconTheme=Mor\n")
    gtk3, gtk4 = (GTK3_CAM, GTK4_CAM) if ROUND else (recolor_css(GTK3_CSS), recolor_css(GTK4_CSS))
    for n in ("gtk.css", "gtk-dark.css"):
        (OUT / "gtk-3.0" / n).write_text(gtk3)
        (OUT / "gtk-4.0" / n).write_text(gtk4)
    for n in ("gtk.css", "gtk-dark.css"):
        p = GTK4 / n
        if p.is_symlink() or p.exists():
            p.unlink()
        p.write_text(gtk4)
    shell()
    print("Mor teması yazıldı:", OUT, GTK4)


if __name__ == "__main__":
    main()

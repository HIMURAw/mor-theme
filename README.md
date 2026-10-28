# Mor

A GTK 3 / GTK 4 / GNOME Shell theme in the violet glass of
[Dynamic Island](https://github.com/HIMURAw/gnome-dynamic-island) and
[Glass Dock](https://github.com/HIMURAw/gnome-glass-dock): dark violet surfaces, lavender
accents, 45° cut corners and a thin lavender line on window edges.

Part of [himura-desktop](https://github.com/HIMURAw/himura-desktop), which installs the
whole set with one command.

## Colour themes

`tema-rengi` switches the whole desktop between colour themes in one go:

```bash
tema-rengi              # list the themes
tema-rengi turkuaz      # turquoise | yesil (green) | mavi (blue) | mor (violet) | gri (grey) | cam (glass: dusk lake wallpaper, soft blue)
```

It rebuilds the GTK and Shell theme, sets the libadwaita accent, tints your wallpaper, the
[Mor icons](https://github.com/HIMURAw/mor-icons), Zen Browser and Spotify (Spicetify), and
writes `~/.config/tema/current.json`, which Dynamic Island, Glass Dock, Glass Widgets,
Glass Windows and Glass Files watch to change at once.

The sources stay violet. Every part runs its colours through one rule (`tema.py`): colours
in the violet family turn to the chosen hue, everything else (white text, red warnings,
green status) is left alone.

## Install

```bash
git clone https://github.com/HIMURAw/mor-theme ~/.local/src/mor-theme
python3 ~/.local/src/mor-theme/build.py
gsettings set org.gnome.desktop.interface gtk-theme Mor
gsettings set org.gnome.shell.extensions.user-theme name Mor
ln -s ~/.local/src/mor-theme/tema-rengi ~/.local/bin/tema-rengi
```

Needs: GNOME 50, Python 3, the User Themes extension, and two themes it builds on:
[adw-gtk3](https://github.com/lassekongo83/adw-gtk3) (`adw-gtk3-dark`) and
[Orchis](https://github.com/vinceliuice/Orchis-theme) (`Orchis-Purple-Dark`, for the
Shell). `tema-rengi` also uses ImageMagick for the wallpaper.

Optional:

- **Wallpaper:** put a violet PNG in `sablon/duvar/`; `tema-rengi` tints it per theme.
- **Zen Browser:** make a `chrome` folder in your Zen profile and enable
  `toolkit.legacyUserProfileCustomizations.stylesheets` in `about:config`. Existing
  `userChrome.css` files that are not ours are never overwritten.
- **Spotify:** with [Spicetify](https://spicetify.app) installed, `tema-rengi` writes a
  `Mor` theme; turn it on with
  `spicetify config current_theme Mor color_scheme Mor inject_theme_js 1 && spicetify apply`.

## What it writes

- `~/.themes/Mor/gtk-3.0` and `~/.themes/Mor/gnome-shell`
- `~/.config/gtk-4.0/gtk.css` (libadwaita apps read their colours from here; back up your
  own first if you have one)

## License

GPL-3.0. The Shell theme is derived from Orchis (GPL-3.0).

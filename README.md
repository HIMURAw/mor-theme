# Mor

A dark GTK 3, GTK 4 / libadwaita and GNOME Shell theme in violet glass: dark violet
surfaces, lavender accents, 45° cut corners and a thin lavender line on window edges. It is
built on top of [Orchis](https://github.com/vinceliuice/Orchis-theme) (Shell) and
[adw-gtk3](https://github.com/lassekongo83/adw-gtk3) (GTK 3).

It also ships `tema-rengi`, a command that recolours the whole desktop in one go: six colour
themes, plus Zen Browser and Spotify.

<!-- screenshot: a GNOME desktop with Nautilus (libadwaita) and a GTK 3 app open side by side, Mor violet theme, Shell top bar and a quick-settings menu visible; no personal files, names or wallpaper text in view -->

## Easiest install

Through [himura-desktop](https://github.com/HIMURAw/himura-desktop), which installs the
packages, the two base themes, this theme and the [Mor icons](https://github.com/HIMURAw/mor-icons)
for you:

```bash
curl -fsSL https://raw.githubusercontent.com/HIMURAw/himura-desktop/main/install.sh | bash -s -- theme
```

Then log out and back in. The manual way is below.

## Requirements

- GNOME 50 (the theme is built for it; other versions are untested)
- Python 3, with Pillow (the icons need it)
- `sassc` (Orchis needs it to build)
- ImageMagick (`magick` or `convert`, only for tinting the wallpaper)
- The **User Themes** GNOME extension, enabled (Shell themes do not load without it)
- Two themes this one is built from:
  - [adw-gtk3](https://github.com/lassekongo83/adw-gtk3): `adw-gtk3-dark`
  - [Orchis](https://github.com/vinceliuice/Orchis-theme): `Orchis-Purple-Dark`
    (`./install.sh -t purple -c dark` in the Orchis repo)

  `build.py` looks for them in `~/.themes`, `~/.local/share/themes` and `/usr/share/themes`.
- Optional: a headless Chromium (only for drawing the `cam` theme's wallpaper, see below)

## Install by hand

```bash
git clone https://github.com/HIMURAw/mor-theme ~/.local/src/mor-theme
python3 ~/.local/src/mor-theme/build.py
gsettings set org.gnome.desktop.interface gtk-theme Mor
gsettings set org.gnome.shell.extensions.user-theme name Mor
mkdir -p ~/.local/bin
ln -s ~/.local/src/mor-theme/tema-rengi ~/.local/bin/tema-rengi
```

`~/.local/bin` must be on your `PATH` for the last step to give you the `tema-rengi` command.

To get the matching icons too, add [Mor icons](https://github.com/HIMURAw/mor-icons). Clone it
next to this folder, in `~/.local/src/mor-icons`; `tema-rengi` expects it there.

## Colour themes: `tema-rengi`

```bash
tema-rengi            # list the themes and mark the current one
tema-rengi turkuaz    # turquoise
tema-rengi yesil      # green
tema-rengi mavi       # blue
tema-rengi mor        # violet (the original)
tema-rengi gri        # grey
tema-rengi cam        # glass: soft blue, rounded frosted corners, a dusk-lake wallpaper
```

The names are Turkish (turkuaz = turquoise, yesil = green, mavi = blue, mor = violet,
gri = grey, cam = glass); English names such as `turquoise`, `green`, `blue`, `violet`,
`grey` and `glass` work too.

The sources stay violet. Every part runs its colours through one rule (`tema.py`): colours in
the violet family turn to the chosen hue (or to grey), everything else (white text, red
warnings, green status) is left alone. `cam` also changes the shape: rounded frosted glass
instead of cut corners.

Add `--no-icons` to skip the icon rebuild: `tema-rengi mavi --no-icons`.

### What one `tema-rengi` run does

1. Writes the chosen name to `~/.config/tema/current.json`. The other parts of the
   [himura-desktop](https://github.com/HIMURAw/himura-desktop) set (Dynamic Island, Glass Dock,
   Glass Widgets, Glass Windows, Glass Files) watch this file and change colour at once.
2. Runs `build.py`, which regenerates the GTK 3, GTK 4 and Shell theme, then makes GTK and
   the Shell reload them (it briefly switches GTK to Adwaita and back to Mor, and blanks and
   restores the Shell theme name).
3. Sets the libadwaita accent colour.
4. Tints your wallpaper (see below) and sets it as the desktop and lock-screen picture.
5. Rewrites the Zen Browser and Spotify themes, if you have them set up (see below).
6. Unless `--no-icons`, rebuilds [Mor icons](https://github.com/HIMURAw/mor-icons) in the
   background (2-3 minutes) and sends a notification when they are in place. Only one icon
   build runs at a time; the log is `~/.cache/tema-rengi.log`.

## What it writes and changes

Files:

- `~/.themes/Mor/`: `index.theme`, `gtk-3.0/`, `gtk-4.0/` and `gnome-shell/`
- `~/.config/gtk-4.0/gtk.css` and `gtk-dark.css`: libadwaita apps read their colours from
  here. **Files of those names are replaced.** The himura-desktop installer backs up your
  own `gtk.css` first; if you install by hand, copy yours away before running `build.py`.
- `~/.config/tema/current.json`: the chosen colour theme
- `~/.local/share/backgrounds/tema-<theme>.png`: the tinted wallpaper (for the themes that
  need tinting; see below)
- `~/.cache/tema-rengi.log` and `~/.cache/tema-rengi-icons.lock`: icon build log and lock
- If you use Zen or Spotify: the files listed under Optional extras

gsettings keys:

- `org.gnome.desktop.interface`: `gtk-theme`, `accent-color`, `icon-theme` (icons)
- `org.gnome.shell.extensions.user-theme`: `name`
- `org.gnome.desktop.background`: `picture-uri`, `picture-uri-dark`
- `org.gnome.desktop.screensaver`: `picture-uri`

## Optional extras

- **Wallpaper:** put a violet PNG in `sablon/duvar/` inside this folder (not shipped,
  git-ignored). `tema-rengi` tints the first PNG there to each colour theme. The `cam` theme
  uses its own picture, `sablon/duvar/cam.png`; if that is missing, it is drawn from
  `sablon/sahne/cam.html` with any headless Chromium found on the system. With no wallpaper
  available, the wallpaper step is skipped.
- **Zen Browser:** create a `chrome` folder in your Zen profile (`~/.zen/<profile>/chrome`,
  or the Flatpak equivalent) and enable `toolkit.legacyUserProfileCustomizations.stylesheets`
  in `about:config`. `tema-rengi` then writes `userChrome.css` and `userContent.css` there
  (plus a backdrop image for `cam`). An existing `userChrome.css` that is not ours is never
  overwritten. Restart Zen to see the change.
- **Spotify:** with [Spicetify](https://spicetify.app) installed (`~/.spicetify/spicetify`),
  `tema-rengi` writes a `Mor` theme to `~/.config/spicetify/Themes/Mor` and runs
  `spicetify refresh`. Turn it on once with:

  ```bash
  spicetify config current_theme Mor color_scheme Mor inject_theme_js 1 && spicetify apply
  ```

  Restart Spotify to see later colour changes.

## Undo

If you installed through himura-desktop, run this from its folder:

```bash
./uninstall.sh theme
```

By hand:

```bash
gsettings reset org.gnome.desktop.interface gtk-theme
gsettings reset org.gnome.desktop.interface icon-theme
gsettings reset org.gnome.desktop.interface accent-color
gsettings reset org.gnome.shell.extensions.user-theme name
rm -rf ~/.themes/Mor ~/.config/tema ~/.local/bin/tema-rengi
rm -f ~/.config/gtk-4.0/gtk.css ~/.config/gtk-4.0/gtk-dark.css   # then put your own back, if you had one
```

The wallpaper is not reset; pick your old one in Settings. The Zen and Spotify files stay
until you delete them (`~/.config/spicetify/Themes/Mor`, and `userChrome.css` /
`userContent.css` in your Zen `chrome` folder).

## Tweaking

The palette is in one place, `PALET` in `build.py`; change it and run
`python3 ~/.local/src/mor-theme/build.py` again. The colour themes are defined in `tema.py`.

## License

GPL-3.0, see [LICENSE](LICENSE). The Shell theme is derived from Orchis (GPL-3.0).

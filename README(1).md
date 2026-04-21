# PinView — Always-on-top Image Overlay

A tiny, fast Windows utility that pins any image above all other windows
so you can read a book, follow a diagram, or reference a screenshot
without ever switching tabs.

---

## Quick Start (no compile needed)

```
pip install pillow pywin32
python pinview.py
```

## Build a standalone .exe (no Python needed afterwards)

Double-click **build.bat** — it produces `dist\PinView.exe`.
Copy that single file anywhere; no installer required.

---

## Features

| Feature | How |
|---|---|
| **Open image file** | Click 📂 or Ctrl+O |
| **Paste screenshot** | Click 📋 or Ctrl+V — also auto-detects clipboard |
| **Auto screenshot detection** | Takes screenshot → overlay appears automatically |
| **Opacity** | Slider (10 – 100 %) |
| **Zoom** | Slider (10 – 500 %) or scroll wheel |
| **Rotate 90°** | ↺ button |
| **Flip H / V** | ⇄ / ⇅ buttons |
| **Lock position** | 🔓 Lock button — prevents accidental drag |
| **Fullscreen view** | ⛶ button — press Esc or click to exit |
| **Fit window to image** | ⊡ Fit button |
| **Resize window** | Drag bottom-right ◢ grip |
| **Move window** | Drag toolbar or image area |
| **Collapse controls** | Click — button |
| **Always on top** | Always — reads your book underneath |
| **Quit** | ✕ button or Esc |

---

## Requirements

- Windows 10/11
- Python 3.8+ (only for script mode)
- `pip install pillow pywin32`

---

## Tips

- Take a screenshot with **Win+Shift+S** (or any tool) → PinView
  detects it instantly and loads it.
- Lower opacity (≈40–60%) lets you see both the overlay and your
  document simultaneously.
- Use scroll wheel to zoom in on fine details without resizing the window.
- Lock position once placed so you don't accidentally drag it.

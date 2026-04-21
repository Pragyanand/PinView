<![CDATA[<div align="center">

# 📌 PinView

### Pin any image on top of everything — forever visible.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?logo=windows)](https://github.com/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)](https://github.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

**A tiny, fast, open-source Windows overlay tool that pins any image above all other windows.**  
Reference a diagram while coding. Read a book while taking notes. Keep a screenshot visible while working.  
No tab-switching. No alt-tabbing. Just pin it and forget it.

[**⬇ Download Latest Release**](../../releases/latest) · [Report Bug](../../issues) · [Request Feature](../../issues)

---

</div>

## ✨ Why PinView?

Ever needed to glance at a reference image, a diagram, or a screenshot while working — but hated constantly switching windows? **PinView** solves this in one click:

- 🖼️ **Open any image** or **paste a screenshot** and it stays pinned on top of everything
- 📋 **Auto-detects clipboard** — take a screenshot with `Win+Shift+S` and PinView loads it instantly
- 👻 **Adjust window opacity** — the entire overlay becomes transparent so you can see your work underneath (sweet spot: 40–60%)
- 🔍 **Zoom & rotate** without resizing the window
- 🔒 **Lock position** so you never accidentally drag it away
- ⚡ **Portable EXE** — no installation, no Python needed. Just download and run.

---

## 🚀 Quick Start

### Option 1: Download the EXE (Recommended)

1. Go to the [**Releases**](../../releases/latest) page
2. Download `PinView.exe`
3. Double-click to run — that's it!

> No installation. No dependencies. A single portable file.

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/PinView.git
cd PinView

# Install dependencies
pip install pillow pywin32

# Run
python pinview.py
```

### Option 3: Build Your Own EXE

```bash
# Just double-click build.bat, or run:
pip install pillow pywin32 pyinstaller
pyinstaller --onefile --windowed --name PinView pinview.py
```

The EXE will appear in the `dist/` folder.

---

## 🎯 Features

| Feature | How | Shortcut |
|:--------|:----|:--------:|
| **Open image file** | Click 📂 or use dialog | `Ctrl+O` |
| **Paste from clipboard** | Click 📋 or paste directly | `Ctrl+V` |
| **Auto screenshot detection** | Take a screenshot → appears automatically | — |
| **Adjust opacity** | Slider (10–100%) or keyboard | `Shift+[` / `Shift+]` |
| **Zoom in/out** | Slider (10–500%), scroll wheel, or keyboard | `Scroll` / `=` / `-` |
| **Rotate 90°** | Click ↺ button | `R` |
| **Flip horizontal** | Click ⇄ button | `H` |
| **Flip vertical** | Click ⇅ button | `V` |
| **Fit window to image** | Click ⊡ Fit button | `F` |
| **Fullscreen view** | Click ⛶ button (Esc to exit) | `Enter` |
| **Lock position** | Prevent accidental dragging | `L` |
| **Toggle controls** | Show/hide the control panel | `C` |
| **Minimize** | Minimize to taskbar | `M` |
| **Show shortcuts** | Opens shortcuts reference panel | `?` or `F1` |
| **Move window** | Drag toolbar or image area | — |
| **Resize window** | Drag the ◢ corner grip | — |
| **Quit** | Close PinView | `Escape` |

---

## 💡 Use Cases

- 📖 **Reading a book/PDF** while taking notes in another app
- 🎨 **UI/UX reference** — keep a mockup visible while coding the implementation
- 📊 **Diagrams & flowcharts** — pin architecture diagrams while writing code
- 📝 **Meeting notes** — keep an agenda or screenshot visible during video calls
- 🖥️ **Multi-monitor supplement** — create a virtual "second screen" overlay on a single monitor
- 🎮 **Game guides** — keep a map or walkthrough pinned over your game

---

## 🖥️ System Requirements

| Requirement | Details |
|:------------|:--------|
| **OS** | Windows 10 / 11 |
| **Runtime** | None (standalone EXE) |
| **Python** | 3.8+ (only if running from source) |
| **Dependencies** | `pillow`, `pywin32` (only if running from source) |

---

## 📁 Project Structure

```
PinView/
├── pinview.py        # Main application (single-file, ~650 lines)
├── build.bat         # One-click build script → produces PinView.exe
├── PinView.spec      # PyInstaller configuration
├── README.md         # This file
├── LICENSE           # MIT License
└── dist/
    └── PinView.exe   # Portable executable (ready to use)
```

---

## 🤝 Contributing

Contributions are welcome! Whether it's a bug fix, new feature, or documentation improvement — every PR matters.

1. **Fork** the repository
2. **Create** your feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m "Add amazing feature"`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Ideas for Contributions

- [ ] Multi-image support (pin several images at once)
- [ ] Hotkey to capture screen region directly
- [ ] Save/restore window position & last image on restart
- [ ] Image annotation (draw arrows, circles, text)
- [ ] Color picker from pinned image
- [ ] macOS / Linux support

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software for any purpose.

---

## ⭐ Support

If PinView helps you, consider:

- ⭐ **Starring** this repository — it helps others discover PinView
- 🐛 **Reporting bugs** via [Issues](../../issues)
- 💡 **Suggesting features** via [Issues](../../issues)
- 🔀 **Contributing** code improvements

---

<div align="center">

**Made with ❤️ for productivity enthusiasts**

*Stop alt-tabbing. Start pinning.*

</div>
]]>

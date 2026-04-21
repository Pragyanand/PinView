<div align="center">

# PinView

### Pin any image on top of everything — forever visible.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?logo=windows)](https://github.com/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-red)](https://github.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

**A tiny, fast, open-source Windows overlay tool that pins any image above all other windows.**  
Reference a diagram while coding. Read a book while taking notes. Keep a screenshot visible while working.  
No tab-switching. No alt-tabbing. Just pin it and forget it.

[**Download Latest Release**](../../releases/latest) · [Report Bug](../../issues) · [Request Feature](../../issues)

---

</div>

## Why PinView?

Ever needed to glance at a reference image, a diagram, or a screenshot while working — but hated constantly switching windows? PinView solves this in one click:

- Open any image or paste a screenshot and it stays pinned on top of everything
- Auto-detects clipboard — take a screenshot with `Win+Shift+S` and PinView loads it instantly
- Adjust opacity — see through the overlay to your work underneath (recommended: 40–60%)
- Zoom and rotate without resizing the window
- Lock position so you never accidentally drag it away
- Portable EXE — no installation, no Python needed. Just download and run

---

## Quick Start

### Option 1: Download the EXE (Recommended)

1. Go to the [Releases](../../releases/latest) page  
2. Download `PinView.exe`  
3. Double-click to run — that's it

No installation. No dependencies. A single portable file.

---

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/PinView.git
cd PinView

# Install dependencies
pip install pillow pywin32

# Run
python pinview.py

"""
PinView - Always-on-top image overlay for Windows
v2 – working minimize, tooltips on every button, shortcuts panel
"""

import tkinter as tk
from tkinter import filedialog, ttk
import threading
import time
import io

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import win32clipboard
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


# ─────────────────────────────────────────────
#  Tooltip
# ─────────────────────────────────────────────

class Tooltip:
    DELAY = 500

    def __init__(self, widget, title, shortcut=""):
        self.widget = widget
        self.title = title
        self.shortcut = shortcut
        self._win = None
        self._job = None
        widget.bind("<Enter>",       self._schedule, add="+")
        widget.bind("<Leave>",       self._cancel,   add="+")
        widget.bind("<ButtonPress>", self._cancel,   add="+")

    def _schedule(self, _=None):
        self._cancel()
        self._job = self.widget.after(self.DELAY, self._show)

    def _cancel(self, _=None):
        if self._job:
            self.widget.after_cancel(self._job)
            self._job = None
        self._hide()

    def _show(self):
        if self._win:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._win = tw = tk.Toplevel(self.widget)
        tw.overrideredirect(True)
        tw.attributes("-topmost", True)
        f = tk.Frame(tw, bg="#1c1c1c",
                     highlightbackground="#3a3a3a", highlightthickness=1)
        f.pack()
        tk.Label(f, text=self.title, bg="#1c1c1c", fg="#eeeeee",
                 font=("Segoe UI", 9), padx=7, pady=3).pack(anchor="w")
        if self.shortcut:
            tk.Label(f, text=self.shortcut, bg="#1c1c1c", fg="#666666",
                     font=("Segoe UI", 8), padx=7, pady=2).pack(anchor="w")
        tw.update_idletasks()
        sw = tw.winfo_screenwidth()
        if x + tw.winfo_width() > sw:
            x = sw - tw.winfo_width() - 4
        tw.geometry(f"+{x}+{y}")

    def _hide(self):
        if self._win:
            self._win.destroy()
            self._win = None


# ─────────────────────────────────────────────
#  Shortcuts panel
# ─────────────────────────────────────────────

SHORTCUTS = [
    ("FILE",          None),
    ("Open image file",       "Ctrl + O"),
    ("Paste / load screenshot", "Ctrl + V"),
    ("IMAGE",         None),
    ("Rotate 90° clockwise",  "R"),
    ("Flip horizontal",       "H"),
    ("Flip vertical",         "V"),
    ("Fit window to image",   "F"),
    ("Fullscreen view",       "Enter"),
    ("VIEW",          None),
    ("Zoom in",               "Scroll ↑  or  ="),
    ("Zoom out",              "Scroll ↓  or  –"),
    ("Increase opacity",      "Shift + ]"),
    ("Decrease opacity",      "Shift + ["),
    ("WINDOW",        None),
    ("Move window",           "Drag toolbar / image"),
    ("Resize window",         "Drag ◢ corner"),
    ("Minimise",              "M"),
    ("Toggle controls panel", "C"),
    ("Lock / unlock position","L"),
    ("Show this panel",       "?  or  F1"),
    ("Quit",                  "Escape"),
]


def show_shortcuts_window(parent):
    win = tk.Toplevel(parent)
    win.title("PinView – Shortcuts")
    win.attributes("-topmost", True)
    win.configure(bg="#141414")
    win.resizable(False, False)

    tk.Label(win, text="⌨  Keyboard Shortcuts",
             bg="#141414", fg="#dddddd",
             font=("Segoe UI Semibold", 11),
             pady=10).grid(row=0, column=0, columnspan=2,
                           sticky="w", padx=14)

    for i, (label, key) in enumerate(SHORTCUTS, start=1):
        if key is None:
            tk.Label(win, text=label, bg="#141414", fg="#444444",
                     font=("Segoe UI", 7, "bold"),
                     pady=4).grid(row=i, column=0, columnspan=2,
                                  sticky="w", padx=14, pady=(8, 0))
        else:
            tk.Label(win, text=label, bg="#141414", fg="#aaaaaa",
                     font=("Segoe UI", 9),
                     anchor="w").grid(row=i, column=0,
                                      sticky="w", padx=(20, 6), pady=1)
            tk.Label(win, text=key, bg="#1e1e1e", fg="#dddddd",
                     font=("Courier New", 9), padx=5, pady=1,
                     relief="flat").grid(row=i, column=1,
                                         sticky="e", padx=(6, 14), pady=1)

    close_row = len(SHORTCUTS) + 1
    tk.Button(win, text="Close  (Esc)", command=win.destroy,
              bg="#2a2a2a", fg="#aaaaaa", relief="flat",
              font=("Segoe UI", 9), pady=6, cursor="hand2",
              activebackground="#3a3a3a", activeforeground="#fff",
              bd=0).grid(row=close_row, column=0, columnspan=2,
                         padx=14, pady=12, sticky="ew")

    win.bind("<Escape>", lambda e: win.destroy())
    win.bind("<F1>",     lambda e: win.destroy())
    win.bind("?",        lambda e: win.destroy())

    win.update_idletasks()
    px, py = parent.winfo_x(), parent.winfo_y()
    pw, ph = parent.winfo_width(), parent.winfo_height()
    ww, wh = win.winfo_width(), win.winfo_height()
    win.geometry(f"+{px + (pw - ww)//2}+{py + (ph - wh)//2}")


# ─────────────────────────────────────────────
#  Clipboard helper
# ─────────────────────────────────────────────

def get_clipboard_image():
    if WIN32_AVAILABLE:
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                data = win32clipboard.GetClipboardData(win32con.CF_DIB)
                win32clipboard.CloseClipboard()
                return Image.open(io.BytesIO(data))
            win32clipboard.CloseClipboard()
        except Exception:
            pass
    return None


# ─────────────────────────────────────────────
#  Main app
# ─────────────────────────────────────────────

class PinView:
    MIN_W, MIN_H = 120, 80
    TOOLBAR_H = 32

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PinView")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1a1a1a")
        self.root.minsize(self.MIN_W, self.MIN_H)

        self.pil_image   = None
        self.tk_image    = None
        self.opacity     = 0.92
        self.zoom        = 1.0
        self.flip_h      = False
        self.flip_v      = False
        self.locked      = False
        self._rotate_angle     = 0
        self._drag_start       = None
        self._resize_start     = None
        self._last_clip_key    = None
        self._clipboard_watch  = True
        self._minimized        = False
        self._pre_min_geom     = None
        self._controls_visible = True

        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        W, H = 340, 295
        self.root.geometry(f"{W}x{H}+{sw-W-24}+{sh-H-52}")

        self._build_ui()
        self._bind_keys()
        self._start_clipboard_watcher()
        self.root.mainloop()

    # ────────── UI ──────────────────────────────

    def _tbtn(self, parent, text, cmd, tip, shortcut=""):
        b = tk.Button(parent, text=text, command=cmd,
                      bg="#111111", fg="#cccccc", relief="flat",
                      font=("Segoe UI", 10), cursor="hand2",
                      activebackground="#2a2a2a", activeforeground="#ffffff",
                      bd=0, padx=5, pady=2)
        Tooltip(b, tip, shortcut)
        return b

    def _build_ui(self):
        # Toolbar
        self.toolbar = tk.Frame(self.root, bg="#111111", height=self.TOOLBAR_H)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.toolbar.pack_propagate(False)

        drag = tk.Label(self.toolbar, text="⠿ PinView",
                        bg="#111111", fg="#444444",
                        font=("Segoe UI", 9), cursor="fleur")
        drag.pack(side=tk.LEFT, padx=(6, 0))
        Tooltip(drag, "Drag to move  |  Lock with L")
        drag.bind("<ButtonPress-1>", self._on_drag_start)
        drag.bind("<B1-Motion>",     self._on_drag_motion)
        self.toolbar.bind("<ButtonPress-1>", self._on_drag_start)
        self.toolbar.bind("<B1-Motion>",     self._on_drag_motion)

        # Toolbar buttons  (right to left)
        self._tbtn(self.toolbar, "✕", self.root.destroy,
                   "Close PinView", "Escape"
                   ).pack(side=tk.RIGHT, padx=(0, 4))
        self._tbtn(self.toolbar, "▁", self._minimize,
                   "Minimise to taskbar", "M"
                   ).pack(side=tk.RIGHT, padx=1)
        self._tbtn(self.toolbar, "⛶", self._fullscreen_view,
                   "View fullscreen", "Enter"
                   ).pack(side=tk.RIGHT, padx=1)
        self._tbtn(self.toolbar, "?", self._show_shortcuts,
                   "Keyboard shortcuts", "? or F1"
                   ).pack(side=tk.RIGHT, padx=1)
        self._tbtn(self.toolbar, "📋", self._paste_clipboard,
                   "Paste image from clipboard", "Ctrl+V"
                   ).pack(side=tk.RIGHT, padx=1)
        self._tbtn(self.toolbar, "📂", self._open_file,
                   "Open image file", "Ctrl+O"
                   ).pack(side=tk.RIGHT, padx=1)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="#1a1a1a",
                                highlightthickness=0, cursor="fleur")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.placeholder = self.canvas.create_text(
            10, 10,
            text="📂  Open file  (Ctrl+O)\n"
                 "📋  Paste screenshot  (Ctrl+V)\n\n"
                 "Screenshots auto-detected",
            fill="#3a3a3a", font=("Segoe UI", 9),
            justify="center", anchor="center")

        # Controls panel
        self.ctrl_frame = tk.Frame(self.root, bg="#111111")
        self.ctrl_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ebtn = dict(bg="#1c1c1c", fg="#aaaaaa", relief="flat",
                    font=("Segoe UI", 8), cursor="hand2",
                    activebackground="#2a2a2a", activeforeground="#ffffff",
                    bd=0, padx=5, pady=3)

        # Sliders
        sr = tk.Frame(self.ctrl_frame, bg="#111111")
        sr.pack(fill=tk.X, padx=6, pady=(4, 2))

        op_icon = tk.Label(sr, text="👁", bg="#111111", fg="#555555",
                           font=("Segoe UI", 9))
        op_icon.pack(side=tk.LEFT)
        Tooltip(op_icon, "Opacity", "Shift+[  /  Shift+]")

        self.opacity_var = tk.DoubleVar(value=self.opacity)
        op_s = ttk.Scale(sr, from_=0.1, to=1.0, variable=self.opacity_var,
                         orient="horizontal", length=95,
                         command=self._on_opacity_change)
        op_s.pack(side=tk.LEFT, padx=(3, 0))
        Tooltip(op_s, "Opacity (10 – 100%)", "Shift+[  /  Shift+]")

        self.opacity_lbl = tk.Label(sr, text="92%", bg="#111111",
                                    fg="#555555", font=("Segoe UI", 8), width=4)
        self.opacity_lbl.pack(side=tk.LEFT, padx=(2, 8))

        zm_icon = tk.Label(sr, text="🔍", bg="#111111", fg="#555555",
                           font=("Segoe UI", 9))
        zm_icon.pack(side=tk.LEFT)
        Tooltip(zm_icon, "Zoom", "Scroll wheel  /  =  or  –")

        self.zoom_var = tk.DoubleVar(value=1.0)
        zm_s = ttk.Scale(sr, from_=0.1, to=5.0, variable=self.zoom_var,
                         orient="horizontal", length=95,
                         command=self._on_zoom_change)
        zm_s.pack(side=tk.LEFT, padx=(3, 0))
        Tooltip(zm_s, "Zoom (10 – 500%)", "Scroll wheel  /  =  or  –")

        self.zoom_lbl = tk.Label(sr, text="100%", bg="#111111",
                                 fg="#555555", font=("Segoe UI", 8), width=5)
        self.zoom_lbl.pack(side=tk.LEFT, padx=(2, 0))

        # Action buttons
        ar = tk.Frame(self.ctrl_frame, bg="#111111")
        ar.pack(fill=tk.X, padx=6, pady=(0, 5))

        def abtn(text, cmd, tip, sc=""):
            b = tk.Button(ar, text=text, command=cmd, **ebtn)
            Tooltip(b, tip, sc)
            return b

        abtn("↺ 90°",   self._rotate_cw,    "Rotate 90° clockwise", "R").pack(side=tk.LEFT, padx=2)
        abtn("⇄ H",     self._do_flip_h,    "Flip horizontal",      "H").pack(side=tk.LEFT, padx=2)
        abtn("⇅ V",     self._do_flip_v,    "Flip vertical",        "V").pack(side=tk.LEFT, padx=2)

        self.lock_btn = tk.Button(ar, text="🔓", command=self._toggle_lock, **ebtn)
        self.lock_btn.pack(side=tk.LEFT, padx=2)
        Tooltip(self.lock_btn, "Lock / unlock window position", "L")

        panel_b = tk.Button(ar, text="≡", command=self._toggle_controls, **ebtn)
        panel_b.pack(side=tk.LEFT, padx=2)
        Tooltip(panel_b, "Hide / show controls panel", "C")

        abtn("⊡ Fit",   self._fit_to_image, "Fit window to image",  "F").pack(side=tk.RIGHT, padx=2)

        # Resize grip
        self.grip = tk.Label(self.root, text="◢", bg="#111111", fg="#2c2c2c",
                             font=("Segoe UI", 10), cursor="size_nw_se")
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        Tooltip(self.grip, "Drag to resize window")
        self.grip.bind("<ButtonPress-1>", self._on_resize_start)
        self.grip.bind("<B1-Motion>",     self._on_resize_motion)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Horizontal.TScale", background="#111111",
                        troughcolor="#2a2a2a", sliderlength=10, sliderrelief="flat")

    # ────────── Key bindings ─────────────────────

    def _bind_keys(self):
        r = self.root
        r.bind("<Control-o>",    lambda e: self._open_file())
        r.bind("<Control-v>",    lambda e: self._paste_clipboard())
        r.bind("r",              lambda e: self._rotate_cw())
        r.bind("R",              lambda e: self._rotate_cw())
        r.bind("h",              lambda e: self._do_flip_h())
        r.bind("H",              lambda e: self._do_flip_h())
        r.bind("v",              lambda e: self._do_flip_v())
        r.bind("f",              lambda e: self._fit_to_image())
        r.bind("F",              lambda e: self._fit_to_image())
        r.bind("<Return>",       lambda e: self._fullscreen_view())
        r.bind("l",              lambda e: self._toggle_lock())
        r.bind("L",              lambda e: self._toggle_lock())
        r.bind("c",              lambda e: self._toggle_controls())
        r.bind("C",              lambda e: self._toggle_controls())
        r.bind("m",              lambda e: self._minimize())
        r.bind("M",              lambda e: self._minimize())
        r.bind("<question>",     lambda e: self._show_shortcuts())
        r.bind("<F1>",           lambda e: self._show_shortcuts())
        r.bind("<Escape>",       lambda e: self.root.destroy())
        r.bind("<equal>",        lambda e: self._zoom_step(1.1))
        r.bind("<minus>",        lambda e: self._zoom_step(0.9))
        r.bind("<bracketright>", lambda e: self._opacity_step(0.05))
        r.bind("<bracketleft>",  lambda e: self._opacity_step(-0.05))
        self.canvas.bind("<MouseWheel>",     self._on_mousewheel)
        self.canvas.bind("<Configure>",      self._on_canvas_resize)
        self.canvas.bind("<ButtonPress-1>",  self._on_drag_start)
        self.canvas.bind("<B1-Motion>",      self._on_drag_motion)

    # ────────── Image ────────────────────────────

    def _open_file(self):
        path = filedialog.askopenfilename(
            title="Open image – PinView",
            filetypes=[("Images",
                        "*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff *.ico"),
                       ("All files", "*.*")])
        if not path:
            return
        try:
            self._set_image(Image.open(path).convert("RGBA"))
        except Exception as ex:
            self._show_error(str(ex))

    def _paste_clipboard(self):
        img = get_clipboard_image()
        if img:
            self._set_image(img.convert("RGBA"))
        else:
            self._show_error("No image found in clipboard")

    def _set_image(self, pil_img):
        self.pil_image = pil_img
        self._rotate_angle = 0
        self.flip_h = self.flip_v = False
        self.zoom = 1.0
        self.zoom_var.set(1.0)
        self.zoom_lbl.config(text="100%")
        # Brief blue flash = new image loaded
        self.root.configure(bg="#2a4e7a")
        self.root.after(140, lambda: self.root.configure(bg="#1a1a1a"))
        self._render_image()

    def _render_image(self):
        if self.pil_image is None:
            return
        img = self.pil_image.copy()
        if self.flip_h:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if self.flip_v:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if self._rotate_angle:
            img = img.rotate(-self._rotate_angle, expand=True)

        cw = max(self.canvas.winfo_width(), 10)
        ch = max(self.canvas.winfo_height(), 10)
        ow, oh = img.size
        scale = min(cw / ow, ch / oh) * self.zoom
        nw = max(1, int(ow * scale))
        nh = max(1, int(oh * scale))
        img = img.resize((nw, nh), Image.LANCZOS)

        if img.mode == "RGBA":
            r2, g, b, a = img.split()
            a = a.point(lambda x: int(x * self.opacity))
            img.putalpha(a)

        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.delete("img")
        self.canvas.itemconfigure(self.placeholder, state="hidden")
        self.canvas.create_image(cw // 2, ch // 2,
                                  image=self.tk_image,
                                  anchor="center", tags="img")

    # ────────── Controls ─────────────────────────

    def _on_opacity_change(self, val):
        self.opacity = float(val)
        self.opacity_lbl.config(text=f"{int(self.opacity*100)}%")
        self._render_image()

    def _opacity_step(self, d):
        v = max(0.1, min(1.0, self.opacity + d))
        self.opacity_var.set(v)
        self._on_opacity_change(v)

    def _on_zoom_change(self, val):
        self.zoom = float(val)
        self.zoom_lbl.config(text=f"{int(self.zoom*100)}%")
        self._render_image()

    def _zoom_step(self, f):
        v = max(0.1, min(5.0, self.zoom * f))
        self.zoom_var.set(v)
        self._on_zoom_change(v)

    def _on_mousewheel(self, e):
        self._zoom_step(1.1 if e.delta > 0 else 0.9)

    def _on_canvas_resize(self, e):
        self._render_image()
        self.canvas.coords(self.placeholder, e.width // 2, e.height // 2)

    def _rotate_cw(self):
        self._rotate_angle = (self._rotate_angle + 90) % 360
        self._render_image()

    def _do_flip_h(self):
        self.flip_h = not self.flip_h
        self._render_image()

    def _do_flip_v(self):
        self.flip_v = not self.flip_v
        self._render_image()

    def _toggle_lock(self):
        self.locked = not self.locked
        self.lock_btn.config(
            text="🔒" if self.locked else "🔓",
            fg="#ff9944" if self.locked else "#aaaaaa")

    def _fit_to_image(self):
        if not self.pil_image:
            return
        self.zoom = 1.0
        self.zoom_var.set(1.0)
        self.zoom_lbl.config(text="100%")
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = self.pil_image.size
        ctrl_h = self.ctrl_frame.winfo_height() if self._controls_visible else 0
        nw = min(w, int(sw * 0.85))
        nh = min(h + self.TOOLBAR_H + ctrl_h + 10, int(sh * 0.85))
        self.root.geometry(f"{nw}x{nh}")
        self._render_image()

    def _toggle_controls(self):
        if self._controls_visible:
            self.ctrl_frame.pack_forget()
            self._controls_visible = False
        else:
            self.ctrl_frame.pack(side=tk.BOTTOM, fill=tk.X)
            self._controls_visible = True

    def _fullscreen_view(self):
        if not self.pil_image:
            return
        fs = tk.Toplevel(self.root)
        fs.attributes("-fullscreen", True)
        fs.attributes("-topmost", True)
        fs.configure(bg="black")
        sw, sh = fs.winfo_screenwidth(), fs.winfo_screenheight()
        img = self.pil_image.copy()
        img.thumbnail((sw, sh), Image.LANCZOS)
        tki = ImageTk.PhotoImage(img)
        lbl = tk.Label(fs, image=tki, bg="black")
        lbl.image = tki
        lbl.pack(expand=True)
        tk.Label(fs, text="Esc or click to close",
                 bg="black", fg="#2e2e2e",
                 font=("Segoe UI", 9)).pack(side=tk.BOTTOM, pady=4)
        fs.bind("<Escape>",      lambda e: fs.destroy())
        fs.bind("<ButtonPress>", lambda e: fs.destroy())

    def _show_shortcuts(self):
        show_shortcuts_window(self.root)

    def _show_error(self, msg):
        self.canvas.itemconfigure(
            self.placeholder,
            text=f"⚠  {msg[:80]}",
            state="normal", fill="#cc4444")
        self.root.after(3000, lambda: self.canvas.itemconfigure(
            self.placeholder,
            text="📂  Open file  (Ctrl+O)\n"
                 "📋  Paste screenshot  (Ctrl+V)\n\n"
                 "Screenshots auto-detected",
            fill="#3a3a3a"))

    # ────────── Minimize (fixed) ─────────────────

    def _minimize(self):
        """
        Borderless windows can't iconify normally.
        We briefly restore the OS titlebar, iconify, then re-apply
        overrideredirect once the user clicks the taskbar button to restore.
        """
        if self._minimized:
            return
        self._minimized = True
        self._pre_min_geom = self.root.geometry()
        self.root.overrideredirect(False)   # give window a titlebar temporarily
        self.root.update_idletasks()
        self.root.iconify()                 # now Windows can minimize it

        def _poll_restore():
            if self.root.state() == "iconic":
                self.root.after(120, _poll_restore)
            else:
                self.root.overrideredirect(True)
                self.root.attributes("-topmost", True)
                if self._pre_min_geom:
                    self.root.geometry(self._pre_min_geom)
                self.root.lift()
                self._minimized = False

        self.root.after(250, _poll_restore)

    # ────────── Drag / resize ────────────────────

    def _on_drag_start(self, e):
        if self.locked:
            return
        self._drag_start = (e.x_root - self.root.winfo_x(),
                             e.y_root - self.root.winfo_y())

    def _on_drag_motion(self, e):
        if self.locked or not self._drag_start:
            return
        dx, dy = self._drag_start
        self.root.geometry(f"+{e.x_root-dx}+{e.y_root-dy}")

    def _on_resize_start(self, e):
        self._resize_start = (e.x_root, e.y_root,
                               self.root.winfo_width(), self.root.winfo_height())

    def _on_resize_motion(self, e):
        if not self._resize_start:
            return
        x0, y0, w0, h0 = self._resize_start
        nw = max(self.MIN_W, w0 + e.x_root - x0)
        nh = max(self.MIN_H, h0 + e.y_root - y0)
        self.root.geometry(f"{nw}x{nh}")
        self._render_image()

    # ────────── Clipboard watcher ────────────────

    def _start_clipboard_watcher(self):
        def watch():
            while self._clipboard_watch:
                try:
                    img = get_clipboard_image()
                    if img:
                        key = img.size
                        if key != self._last_clip_key:
                            self._last_clip_key = key
                            self.root.after(
                                0, lambda i=img: self._set_image(i.convert("RGBA")))
                except Exception:
                    pass
                time.sleep(1.0)
        threading.Thread(target=watch, daemon=True).start()


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    if not PIL_AVAILABLE:
        import tkinter.messagebox as mb
        mb.showwarning(
            "PinView – Missing dependency",
            "Pillow is not installed.\n\n"
            "Run:  pip install pillow pywin32\n\n"
            "PinView will launch in limited mode.")
    PinView()

"""Environment fixes for the tkinterweb reading pane.

Both are applied once, defensively, and become no-ops if the underlying
condition does not apply or tkinterweb's internals move in a future release.
"""

import tkinter
from tkinter import ttk

# 1x1 transparent PNG, used to probe whether Tk can decode PNG from inline data.
_PROBE_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06"
    b"\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05"
    b"\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

# tkinterweb hands these straight to tkinter.PhotoImage as an optimisation.
_TK_FAST_PATH = ("image/png", "image/gif", "image/ppm", "image/pgm")

_image_fix_applied = False
_scrollbar_style_ready = False


def _tk_can_decode_png() -> bool:
    """Tests whether this Tk build accepts PNG bytes via PhotoImage(data=...).

    Requires an existing Tk root, so call this from inside a widget.
    """
    try:
        image = tkinter.PhotoImage(data=_PROBE_PNG)
    except tkinter.TclError:
        return False

    image.__del__ = lambda *_: None  # avoid a teardown warning on the throwaway
    return True


def apply_image_fix():
    """Routes PNG/GIF decoding through Pillow when Tk cannot handle it itself.

    Several Tk 8.6 builds -- including the one shipped with Python 3.14 on
    Windows -- fail with "couldn't recognize image data" when given PNG bytes
    through PhotoImage(data=...), even base64-encoded. tkinterweb takes that
    path deliberately because tkinter.PhotoImage has less overhead than
    Pillow's, so every PNG in a note renders as alt text instead.

    Rather than reimplement decoding, this relabels the mimetype so tkinterweb
    falls into its own Pillow branch, which handles the same bytes correctly.
    Pillow is already a hard dependency of this project.
    """
    global _image_fix_applied

    if _image_fix_applied or _tk_can_decode_png():
        return

    try:
        from tkinterweb import imageutils
    except ImportError:
        return

    original = getattr(imageutils, "data_to_image", None)
    if original is None:
        print("Notes: tkinterweb.imageutils.data_to_image is missing; "
              "PNG images in notes may not render.")
        return

    def data_to_image(data, name, imagetype, data_is_image):
        # Pillow sniffs the real format from the bytes, so the substituted
        # label only needs to miss tkinterweb's fast-path tuple.
        if not data_is_image and imagetype in _TK_FAST_PATH:
            imagetype = "image/x-pillow-fallback"
        return original(data, name, imagetype, data_is_image)

    imageutils.data_to_image = data_to_image
    _image_fix_applied = True


def style_scrollbars(html_frame, colors):
    """Darkens the ttk scrollbars tkinterweb creates inside its frame.

    Windows' native ttk themes draw scrollbars themselves and ignore colour
    options, which leaves a bright strip down the side of the dark reading
    pane. Switching to the 'clam' theme makes them themable. Nothing else in
    this app uses ttk -- CustomTkinter draws its own widgets on canvases -- so
    the change is confined to the notes pane in practice.

    :param html_frame: The HtmlFrame whose scrollbars should be restyled.
    :param colors: {"trough", "thumb", "thumb_active"} hex strings.
    """
    global _scrollbar_style_ready

    style = ttk.Style()

    if not _scrollbar_style_ready:
        if "clam" not in style.theme_names():
            return
        if style.theme_use() != "clam":
            style.theme_use("clam")

        for orient in ("Vertical", "Horizontal"):
            style.configure(
                f"Notes.{orient}.TScrollbar",
                background=colors["thumb"],
                troughcolor=colors["trough"],
                bordercolor=colors["trough"],
                darkcolor=colors["thumb"],
                lightcolor=colors["thumb"],
                arrowcolor=colors["thumb_active"],
                relief="flat",
                borderwidth=0,
                arrowsize=12,
            )
            style.map(
                f"Notes.{orient}.TScrollbar",
                background=[("active", colors["thumb_active"])],
            )

        _scrollbar_style_ready = True

    for attribute, orient in (("_vsb", "Vertical"), ("_hsb", "Horizontal")):
        scrollbar = getattr(html_frame, attribute, None)
        if scrollbar is not None:
            try:
                scrollbar.configure(style=f"Notes.{orient}.TScrollbar")
            except tkinter.TclError:
                pass

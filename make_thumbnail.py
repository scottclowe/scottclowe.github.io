#!/usr/bin/env python3
"""
Make a web-optimized publication thumbnail.

Pipeline:
  1. Flatten any transparency onto a white background.
  2. Crop to content (trim the uniform border around the figure).
  3. Downscale (Lanczos) so the long side is <= 240px, matching the 240px
     thumbnail slot on publications.md so it displays 1:1. A high-resolution copy
     (long side <= 1200px) is also written to img/publications/hires/, which
     publications.md serves to high-density screens via srcset, so the figure
     stays sharp when zoomed in on a phone.
  4. Optionally pad with an even white margin (--margin; off by default),
     scaled proportionally for the high-resolution copy.
  5. Encode:
     - PNG (default): reduce to the smallest palette whose RMSE against the
       truecolor image is below a threshold (i.e. imperceptible), otherwise
       keep truecolor; then losslessly recompress with oxipng (max + Zopfli).
     - JPEG (--jpeg, for photos): progressive JPEG.

Usage:
  python make_thumbnail.py SOURCE KEY
  python make_thumbnail.py _thumbnail_candidates/Foo2026_Bar/fig1.png Foo2026_Bar
  python make_thumbnail.py photo.jpg Foo2026_Bar --jpeg

Writes img/publications/KEY.png (or .jpg) plus img/publications/hires/KEY.png
(or .jpg), and prints the `thumbnail:` value to put in _data/publications.yml.

Requires Pillow and numpy. For the final PNG recompression, install pyoxipng
(`pip install pyoxipng`) or have the `oxipng` CLI on your PATH; without
either the PNG is still written, just a little larger.
"""

import argparse
import io
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "publications")
HIRES_SUBDIR = "hires"
WHITE = (255, 255, 255)
PALETTE_SIZES = (8, 16, 32, 64, 128, 256)


def flatten(im, background=WHITE):
    """Return an RGB image, compositing any alpha channel onto background."""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, background + (255,))
        return Image.alpha_composite(bg, im).convert("RGB")
    return im.convert("RGB")


def crop_to_content(im, tolerance=12):
    """Trim the border around the content.

    The border colour is taken from the top-left pixel, so this works for
    non-white backgrounds too. Pixels differing from it by more than
    tolerance (on any channel, 0-255) count as content.
    """
    arr = np.asarray(im, dtype=np.int16)
    bg = arr[0, 0]
    mask = (np.abs(arr - bg) > tolerance).any(axis=2)
    if not mask.any():
        return im
    rows = np.flatnonzero(mask.any(axis=1))
    cols = np.flatnonzero(mask.any(axis=0))
    return im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))


def resize_and_pad(im, max_size, margin, background=WHITE):
    """Downscale so the padded image fits in max_size, then add an even margin."""
    inner = max_size - 2 * margin
    scale = min(1.0, inner / max(im.size))
    if scale < 1.0:
        new_size = tuple(max(1, round(d * scale)) for d in im.size)
        im = im.resize(new_size, Image.LANCZOS)
    if margin > 0:
        padded = Image.new("RGB", (im.width + 2 * margin, im.height + 2 * margin), background)
        padded.paste(im, (margin, margin))
        im = padded
    return im


def rmse(a, b):
    a = np.asarray(a.convert("RGB"), dtype=np.float64)
    b = np.asarray(b.convert("RGB"), dtype=np.float64)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def png_bytes(im):
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def best_png(im, max_rmse):
    """Return (image, description) for the smallest acceptable PNG encoding."""
    candidates = [(len(png_bytes(im)), im, "truecolor")]
    # Note: Pillow's LIBIMAGEQUANT method returns garbage for RGB input on some
    # builds, so stick to the built-in quantizers.
    for method, mname in ((Image.Quantize.MEDIANCUT, "median-cut"), (Image.Quantize.FASTOCTREE, "octree")):
        for n in PALETTE_SIZES:
            q = im.quantize(colors=n, method=method)
            err = rmse(im, q)
            if err <= max_rmse:
                candidates.append((len(png_bytes(q)), q, f"{n}-colour {mname} palette, RMSE {err:.2f}"))
    _, best, desc = min(candidates, key=lambda c: c[0])
    return best, desc


def oxipng(path):
    """Losslessly recompress a PNG in place. Returns a short status string."""
    try:
        import oxipng as pyoxipng
        pyoxipng.optimize(path, level=6, strip=pyoxipng.StripChunks.safe(),
                          deflate=pyoxipng.Deflaters.zopfli(15))
        return "pyoxipng (max + Zopfli)"
    except ImportError:
        pass
    exe = shutil.which("oxipng")
    if exe:
        subprocess.run([exe, "-o", "max", "--strip", "safe", "--zopfli", "-q", path], check=True)
        return "oxipng CLI (max + Zopfli)"
    return None


def encode(im, out_path, args):
    """Write im to out_path as PNG or JPEG, per args, and report the result."""
    if args.jpeg:
        im.save(out_path, format="JPEG", quality=args.quality, optimize=True, progressive=True)
        print(f"Encoding: progressive JPEG, quality {args.quality}")
    else:
        im, desc = best_png(im, args.max_rmse)
        im.save(out_path, format="PNG", optimize=True)
        print(f"Encoding: {desc}")
        status = oxipng(out_path)
        if status:
            print(f"Recompressed with {status}")
        else:
            print("Warning: oxipng not found (pip install pyoxipng); PNG not fully recompressed.", file=sys.stderr)
    print(f"Wrote {out_path} ({os.path.getsize(out_path):,} bytes)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="Source image (figure exported from the paper).")
    parser.add_argument("key", help="Citation key, e.g. Lin2026_KLShampoo. Used as the output filename.")
    parser.add_argument("--jpeg", action="store_true", help="Encode as progressive JPEG (for photos).")
    parser.add_argument("--max-size", type=int, default=240, help="Max long side in px, including margin (default: 240).")
    parser.add_argument("--hires-size", type=int, default=1200, help="Max long side in px of the high-resolution copy (default: 1200; 0 to skip it).")
    parser.add_argument("--hires-only", action="store_true", help="Only write the high-resolution copy (e.g. to add one for an existing thumbnail).")
    parser.add_argument("--margin", type=int, default=0, help="Even white margin in output px, added after cropping (default: 0, i.e. tight crop; East2025 uses 10).")
    parser.add_argument("--no-crop", action="store_true", help="Skip cropping to content.")
    parser.add_argument("--crop-tolerance", type=int, default=12, help="Border colour tolerance for cropping, 0-255 (default: 12).")
    parser.add_argument("--max-rmse", type=float, default=2.0, help="Max RMSE (0-255 scale) for palette reduction (default: 2.0).")
    parser.add_argument("--quality", type=int, default=85, help="JPEG quality (default: 85).")
    parser.add_argument("--out-dir", default=OUT_DIR, help="Output directory (default: img/publications); the high-resolution copy goes in its hires/ subdirectory.")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite an existing thumbnail.")
    args = parser.parse_args()

    ext = ".jpg" if args.jpeg else ".png"
    out_path = os.path.join(args.out_dir, args.key + ext)
    hires_path = os.path.join(args.out_dir, HIRES_SUBDIR, args.key + ext)
    outputs = []  # (path, max long side, margin)
    if not args.hires_only:
        outputs.append((out_path, args.max_size, args.margin))
    if args.hires_size > 0:
        outputs.append((hires_path, args.hires_size, round(args.margin * args.hires_size / args.max_size)))
    if not outputs:
        sys.exit("Nothing to write: --hires-only needs a non-zero --hires-size.")
    for path, _, _ in outputs:
        if os.path.exists(path) and not args.force:
            sys.exit(f"{path} already exists; use --force to overwrite.")

    im = flatten(Image.open(args.source))
    src_size = im.size
    if not args.no_crop:
        im = crop_to_content(im, args.crop_tolerance)
    crop_size = im.size

    for path, max_size, margin in outputs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        out = resize_and_pad(im, max_size, margin)
        print(f"\n{src_size[0]}x{src_size[1]} -> cropped {crop_size[0]}x{crop_size[1]} -> {out.width}x{out.height}")
        encode(out, path, args)

    if not args.hires_only:
        print(f"\n  thumbnail: /img/publications/{args.key}{ext}")


if __name__ == "__main__":
    main()

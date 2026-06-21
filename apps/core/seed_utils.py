"""Utilitaires partagés par les commandes de seed (images de couverture)."""
import io
from urllib.request import Request, urlopen

from django.core.files.base import ContentFile


def _gradient(color=(245, 166, 35)):
    """Repli local : dégradé sombre + halo or (charte du site)."""
    from PIL import Image, ImageDraw

    w, h = 1200, 675
    img = Image.new("RGB", (w, h), (10, 10, 10))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(10 + t * 120), int(10 + t * 70), int(5 + t * 10)))
    draw.ellipse([w - 360, -120, w + 120, 360], fill=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=82)
    return ContentFile(buf.getvalue(), name="cover.jpg")


def fetch_cover(seed, keywords="technology", w=1200, h=675):
    """Récupère une image de couverture EN LIGNE, pertinente par mots-clés.

    1) loremflickr : vraie photo en lien avec `keywords` (stable grâce à `lock`).
    2) placehold.co : image placeholder aux couleurs du site (repli réseau).
    3) dégradé local : ultime repli si aucun réseau n'est disponible.
    """
    import hashlib

    lock = int(hashlib.md5(str(seed).encode()).hexdigest(), 16) % 100000
    kw = keywords.replace(" ", "")
    sources = [
        f"https://loremflickr.com/{w}/{h}/{kw}?lock={lock}",
        f"https://placehold.co/{w}x{h}/0a0a0a/F5A623/jpg?text=Augustin+Idohou",
    ]
    for url in sources:
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urlopen(req, timeout=10).read()
            if data and len(data) > 2000:
                return ContentFile(data, name=f"{seed}.jpg")
        except Exception:
            continue
    return _gradient()

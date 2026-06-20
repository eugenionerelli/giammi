"""Prepara il guardaroba: copia anche gli abiti (overall) e calcola il colore
dominante di ogni capo, scrivendo un garments.json arricchito (id,label,category,file,color)."""
import json
import os
import shutil

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "backend/CatVTON/resource/demo/example")
WEB = os.path.join(ROOT, "web")
GDIR = os.path.join(WEB, "garments")
os.makedirs(GDIR, exist_ok=True)


def dominant_hex(path: str) -> str:
    img = Image.open(path).convert("RGB").resize((64, 64))
    a = np.asarray(img).reshape(-1, 3).astype(float)
    # escludi i pixel quasi-bianchi (sfondo/padding) per cogliere il colore del capo
    keep = ~((a[:, 0] > 235) & (a[:, 1] > 235) & (a[:, 2] > 235))
    a = a[keep] if keep.sum() > 50 else a
    med = np.median(a, axis=0).round().astype(int)
    return "#%02X%02X%02X" % (int(med[0]), int(med[1]), int(med[2]))


manifest = []
for i in range(1, 5):
    f = f"top_{i}.jpg"
    manifest.append({"id": f"top_{i}", "label": f"Top {i}", "category": "upper",
                     "file": f"garments/{f}", "color": dominant_hex(os.path.join(GDIR, f))})

overall = sorted(os.listdir(os.path.join(EX, "condition/overall")))
for i, src in enumerate(overall, 1):
    f = f"dress_{i}.jpg"
    shutil.copy(os.path.join(EX, "condition/overall", src), os.path.join(GDIR, f))
    manifest.append({"id": f"dress_{i}", "label": f"Abito {i}", "category": "overall",
                     "file": f"garments/{f}", "color": dominant_hex(os.path.join(GDIR, f))})

with open(os.path.join(WEB, "garments.json"), "w") as fh:
    json.dump(manifest, fh, ensure_ascii=False, indent=2)

print(f"{len(manifest)} capi:")
for m in manifest:
    print(" ", m["id"], m["category"], m["color"])

# 👗 Giammi — il tuo armadio virtuale con l'AI

**Provati i vestiti addosso senza toglierti il pigiama.** Carichi una tua foto, scegli un capo
dal guardaroba (o ne fotografi uno nuovo) e l'AI te lo fa indossare. In più ti analizza i colori
e ti suggerisce palette e look su misura. ✨

> 🤙 **Interamente _vibe coded_** da [@eugenionerelli](https://github.com/eugenionerelli)
> e **@gianmattiabarone** — due che programmano a sensazione, a colpi di idee, caffè ed entusiasmo. 🚀
> _(@gianmattiabarone si farà l'account GitHub a breve — benvenuto!)_

## Cosa fa
- 🧍 **Virtual try-on** — ti vedi indossare i capi (modello generativo open-source).
- 🎨 **Color analysis** — dalla foto stima sottotono pelle (ITA° in CIELAB), stagione e palette personale.
- 🧥 **Guardaroba** con filtri (maglie / pantaloni / abiti) e ⭐ sui capi che stanno bene con la tua palette.
- 📷 **Fotografa un capo** → sfondo rimosso automaticamente + categoria auto → finisce nel guardaroba.
- ☁️ / 💻 **Due motori** — GPU cloud gratuita (veloce) oppure **tutto in locale sul Mac** (privato).
- 🌗 Tema chiaro/scuro automatico, layout responsive desktop + smartphone, animazioni fluide.

## Stack
- **Frontend**: web-app in Preact (senza build) servita dal backend; gira nel browser, anche da iPhone in LAN.
- **Backend**: FastAPI su Apple Silicon (Metal/MPS). Try-on: **CatVTON** (locale) / **IDM-VTON** (cloud HF).
  Segmentazione: **segformer_b2_clothes** + **rembg**. Niente detectron2.

## Requisiti
- Mac **Apple Silicon** (M1 o superiore) per il try-on locale (GPU Metal). Senza Apple Silicon si può
  usare solo la modalità **cloud**.
- **Python 3.11**.

## Avvio
```bash
git clone <questo-repo> app-giammi
cd app-giammi/backend
python3.11 -m venv .venv
.venv/bin/pip install -r ../requirements.txt
git clone https://github.com/Zheng-Chong/CatVTON          # motore try-on (terze parti)
.venv/bin/python download_weights.py                       # pesi modello (~4 GB)
.venv/bin/python prep_wardrobe.py                          # guardaroba di esempio
.venv/bin/python -m uvicorn server:app --host 0.0.0.0 --port 8770
```
Apri **http://127.0.0.1:8770** sul Mac, oppure **http://<IP-del-Mac>:8770** dal telefono sulla stessa Wi-Fi.

## App iOS
Scaffold SwiftUI (WKWebView verso il server del Mac) in [`ios/`](ios/).

## Note oneste
- ☁️ Il **cloud** usa una GPU gratuita Hugging Face con quota limitata: quando finisce, l'app
  **passa automaticamente al locale e te lo dice**. Imposta `HF_TOKEN` per più quota.
- ⚖️ I motori try-on (CatVTON / IDM-VTON) hanno **licenza non commerciale**: progetto per
  imparare e divertirsi, non da vendere così com'è.
- 🔒 Nessuna API key nel repo: si usano variabili d'ambiente.

Fatto con tanto entusiasmo (e qualche `torch.mps.empty_cache()`) 💚

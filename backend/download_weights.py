"""Scarica SOLO i pesi necessari per il try-on CatVTON (SD1.5), cache dentro il progetto.

Evita di tirare giu' l'intero repo zhengchong/CatVTON (che include DensePose, SCHP,
Flux -> molti GB inutili per noi): prende solo la cartella mix-48k-1024.
"""
import os

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".hf-cache")
os.environ.setdefault("HF_HOME", CACHE)

from huggingface_hub import snapshot_download


def dir_size_gb(path: str) -> float:
    total = 0
    for root, _dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total / 1e9


def main() -> None:
    print(">> pesi try-on (mix-48k-1024) da zhengchong/CatVTON ...")
    mix = snapshot_download("zhengchong/CatVTON", allow_patterns=["mix-48k-1024/**"])
    print("   ->", mix)

    print(">> base inpainting (solo unet+scheduler) da booksforcharlie/stable-diffusion-inpainting ...")
    base = snapshot_download(
        "booksforcharlie/stable-diffusion-inpainting",
        allow_patterns=["unet/**", "scheduler/**", "model_index.json"],
    )
    print("   ->", base)

    print(">> VAE sd-vae-ft-mse ...")
    vae = snapshot_download(
        "stabilityai/sd-vae-ft-mse",
        allow_patterns=["config.json", "diffusion_pytorch_model.safetensors"],
    )
    print("   ->", vae)

    print(f"\nCache totale: {dir_size_gb(CACHE):.2f} GB in {CACHE}")
    # salvo i path per gli script successivi
    with open(os.path.join(os.path.dirname(__file__), "weights_paths.txt"), "w") as fh:
        fh.write(f"MIX={mix}\nBASE={base}\nVAE={vae}\n")
    print("Path salvati in weights_paths.txt")


if __name__ == "__main__":
    main()

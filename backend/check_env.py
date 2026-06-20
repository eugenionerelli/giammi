"""Sanity check dell'ambiente: verifica che PyTorch usi la GPU Metal (MPS)."""
import time
import torch


def main() -> None:
    print(f"torch          : {torch.__version__}")
    print(f"mps available  : {torch.backends.mps.is_available()}")
    print(f"mps built      : {torch.backends.mps.is_built()}")

    if not torch.backends.mps.is_available():
        print("\n[!] MPS non disponibile: la generazione girerebbe su CPU (lentissima).")
        return

    device = torch.device("mps")
    # piccolo matmul per confermare che il device calcola davvero
    a = torch.randn(2048, 2048, device=device)
    b = torch.randn(2048, 2048, device=device)
    torch.mps.synchronize()
    t0 = time.perf_counter()
    for _ in range(10):
        c = a @ b
    torch.mps.synchronize()
    dt = (time.perf_counter() - t0) / 10
    print(f"matmul 2048^2  : {dt * 1000:.1f} ms/iter su MPS  -> ok")
    print(f"result device  : {c.device}, sum={float(c.float().sum()):.1f}")


if __name__ == "__main__":
    main()

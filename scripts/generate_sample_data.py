"""Create tiny SYNTHETIC CSVs solely to test that everyone's code runs."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "sample"


def make_frame(n, rng):
    proto = rng.choice(["tcp", "udp", "icmp"], size=n, p=[0.55, 0.35, 0.10])
    service = rng.choice(["http", "dns", "ftp", "-"], size=n)
    state = rng.choice(["FIN", "CON", "INT"], size=n)
    dur = rng.exponential(scale=2.0, size=n)
    spkts = rng.poisson(12, size=n) + 1
    dpkts = rng.poisson(10, size=n) + 1
    sbytes = spkts * rng.integers(20, 1000, size=n)
    dbytes = dpkts * rng.integers(20, 1000, size=n)
    sttl = rng.choice([31, 64, 128, 255], size=n)
    dttl = rng.choice([31, 64, 128], size=n)
    rate = (spkts + dpkts) / np.maximum(dur, 0.1)
    ct_srv_src = rng.integers(1, 10, size=n)
    ct_dst_ltm = rng.integers(1, 15, size=n)
    signal = (proto == "icmp") * 0.8 + (state == "INT") * 1.2 + (rate > 60) * 1.1
    signal += (sttl == 255) * 0.8 + (ct_dst_ltm > 10) * 0.8 + rng.normal(0, 1.1, size=n)
    label = (signal > 1.35).astype(int)
    attack_cat = np.where(label == 1, "Generic", "Normal")
    return pd.DataFrame({
        "id": np.arange(1, n + 1), "dur": dur, "proto": proto,
        "service": service, "state": state, "spkts": spkts, "dpkts": dpkts,
        "sbytes": sbytes, "dbytes": dbytes, "rate": rate, "sttl": sttl,
        "dttl": dttl, "ct_srv_src": ct_srv_src, "ct_dst_ltm": ct_dst_ltm,
        "attack_cat": attack_cat, "label": label,
    })


def main():
    rng = np.random.default_rng(42)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    make_frame(500, rng).to_csv(DATA_DIR / "UNSW_NB15_training-set.csv", index=False)
    make_frame(120, rng).to_csv(DATA_DIR / "UNSW_NB15_testing-set.csv", index=False)
    print("Synthetic sample CSVs created in data/sample/ (500 train, 120 test).")
    print("These are NOT the real dataset. Do not use their scores in your final report.")


if __name__ == "__main__":
    main()

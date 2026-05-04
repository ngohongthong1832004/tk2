"""
Monitoring đơn giản:
- Log mỗi prediction request vào file `logs/predictions.log`
- Detect data drift đơn giản dựa trên độ dài trung bình của email
  + Tính baseline length từ dataset training (mean ± std)
  + Nếu mean length của requests gần đây lệch > 2*std => báo drift
"""
import os
import json
import logging
from datetime import datetime

import pandas as pd

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "predictions.log"),
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)


def log_prediction(text: str, predicted_label: str) -> None:
    logging.info(json.dumps({
        "time": datetime.utcnow().isoformat(),
        "text_length": len(text),
        "predicted_label": predicted_label,
        "text_preview": text[:80],
    }))


def compute_baseline(train_csv: str = "../1_DataPipeline/processed/clean_data.csv") -> dict:
    df = pd.read_csv(train_csv)
    lengths = df["text"].astype(str).str.len()
    return {"mean": float(lengths.mean()), "std": float(lengths.std())}


def detect_drift(recent_lengths: list[int], baseline: dict, k: float = 2.0) -> dict:
    if not recent_lengths:
        return {"drift": False, "reason": "no data"}

    recent_mean = sum(recent_lengths) / len(recent_lengths)
    diff = abs(recent_mean - baseline["mean"])
    threshold = k * baseline["std"]
    drift = diff > threshold

    return {
        "drift": bool(drift),
        "recent_mean": recent_mean,
        "baseline_mean": baseline["mean"],
        "threshold": threshold,
    }


if __name__ == "__main__":
    baseline = compute_baseline()
    print("Baseline:", baseline)

    sample_lengths = [200, 220, 250, 210, 230]
    print("Drift check:", detect_drift(sample_lengths, baseline))

# Yêu cầu 5: CI/CD & Monitoring

## 1. CI/CD Pipeline (GitHub Actions)
File: `.github/workflows/mlops.yml`

Các bước chạy tự động khi push code lên `main`:
1. Checkout code
2. Setup Python 3.10
3. Cài dependencies
4. **Run data pipeline** — chạy `data_pipeline.ipynb`
5. **Train model** — chạy `train.ipynb`
6. **Run tests** — chạy pytest

## 2. Monitoring
File: `monitoring.py`

- **Log prediction requests:** ghi mỗi request (thời gian, độ dài text, label dự đoán) vào `logs/predictions.log`.
- **Drift detection (đơn giản):** so sánh độ dài trung bình của email gần đây với baseline lấy từ tập training.
  - Nếu `|recent_mean - baseline_mean| > 2 * std` → cảnh báo drift.

## 3. Khi nào cần retrain model?

**Cần retrain khi xảy ra một trong các tình huống sau:**

1. **Phát hiện data drift** — phân phối dữ liệu đầu vào (vd: độ dài email trung bình) thay đổi đáng kể so với baseline → model cũ không còn đại diện.
2. **Performance giảm** — Precision / Recall / F1 trên tập giám sát giảm dưới ngưỡng cho phép (vd: F1 < 0.9).
3. **Có dữ liệu mới đáng kể** — thu thập đủ nhiều mẫu mới (vd: > 10% kích thước tập train ban đầu), đặc biệt là các loại spam mới chưa từng thấy.
4. **Định kỳ** — retrain theo lịch (vd: hàng tuần / hàng tháng) để đảm bảo model luôn cập nhật.
5. **Concept drift** — định nghĩa "spam" thay đổi (vd: kiểu lừa đảo mới xuất hiện), feedback từ người dùng cho thấy nhiều false positive/negative.

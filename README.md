# Project: MLOps Pipeline phân loại Email Spam

**Sinh viên:** Ngô Hồng Thông
**Dataset:** spamDataset.csv (5572 email, label ham/spam)

## Cấu trúc thư mục

```
ngohongthong/
├── spamDataset.csv
├── requirements.txt
├── 1_DataPipeline/
│   └── data_pipeline.ipynb       # Yêu cầu 1: clean + TF-IDF + lưu dataset
├── 2_ModelTraining/
│   ├── train.ipynb               # Yêu cầu 2: train NB + XGBoost + MLflow
│   └── mlflow_ui.png             # Ảnh chụp MLflow UI
├── 3_ModelRegistry/
│   └── registry.ipynb            # Yêu cầu 3: register + Staging/Production + so sánh
├── 4_ModelDeployment/
│   ├── app.ipynb                 # Yêu cầu 4: hướng dẫn deploy
│   └── app.py                    # FastAPI server
└── 5_CICD_Monitoring/
    ├── README.md                 # Giải thích + khi nào retrain
    ├── monitoring.py             # Log + drift detection
    ├── tests/test_pipeline.py    # Unit test cho CI
    └── .github/workflows/mlops.yml
```

## Cách chạy

```bash
pip install -r requirements.txt

# Yêu cầu 1: Data pipeline
jupyter notebook 1_DataPipeline/data_pipeline.ipynb

# Yêu cầu 2: Training
jupyter notebook 2_ModelTraining/train.ipynb
mlflow ui --backend-store-uri file:./2_ModelTraining/mlruns   # Chụp UI

# Yêu cầu 3: Registry
jupyter notebook 3_ModelRegistry/registry.ipynb

# Yêu cầu 4: Deployment
cd 4_ModelDeployment && uvicorn app:app --reload --port 8000

# Test API
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Free entry to win an iPhone"}'

# Yêu cầu 5: CI/CD chạy tự động khi push lên GitHub
```
# tk2

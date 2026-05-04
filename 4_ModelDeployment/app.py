import re
import joblib
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Spam Classifier API')

mlflow.set_tracking_uri("file:../2_ModelTraining/mlruns")
model = mlflow.pyfunc.load_model("models:/spam_classifier/Production")
vectorizer = joblib.load("../1_DataPipeline/processed/tfidf_vectorizer.pkl")


def clean_text(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


class Item(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Spam Classifier API is running"}


@app.post("/predict")
def predict(item: Item):
    x = vectorizer.transform([clean_text(item.text)])
    pred = int(model.predict(x)[0])
    label = "spam" if pred == 1 else "ham"
    return {"input": item.text, "predicted_label": label}

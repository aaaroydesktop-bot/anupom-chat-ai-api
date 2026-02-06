from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from transformers import pipeline
import torch
import torchvision.models as models
import torchvision.transforms as T
from PIL import Image

app = FastAPI(title="Simple AI API")

# ---------- NLP ----------
nlp = pipeline("sentiment-analysis")

class TextReq(BaseModel):
    text: str

@app.post("/nlp")
def nlp_api(req: TextReq):
    result = nlp(req.text)
    return {"text": req.text, "result": result}

# ---------- CNN ----------
cnn = models.resnet18(pretrained=True)
cnn.eval()

transform = T.Compose([
    T.Resize((224,224)),
    T.ToTensor()
])

@app.post("/cnn")
async def cnn_api(file: UploadFile = File(...)):
    img = Image.open(file.file).convert("RGB")
    x = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = cnn(x)

    return {"prediction_index": out.argmax().item()}

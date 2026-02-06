from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI(title="URL Viewer API")

class UrlReq(BaseModel):
    url: HttpUrl   # ✅ only valid http/https

@app.post("/view")
def view_url(req: UrlReq):
    start = time.time()

    try:
        r = requests.get(
            str(req.url),
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        elapsed = round((time.time() - start) * 1000, 2)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"
        meta = soup.find("meta", attrs={"name": "description"})
        description = meta["content"] if meta and meta.get("content") else ""

        return {
            "url": str(req.url),
            "status_code": r.status_code,
            "response_time_ms": elapsed,
            "title": title,
            "description": description,
            "server": r.headers.get("Server", "Unknown")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def root():
    return {"status": "URL Viewer API running"}

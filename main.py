from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import time

app = FastAPI(title="URL Viewer API")

class UrlReq(BaseModel):
    url: str

@app.post("/view")
def view_url(req: UrlReq):
    start = time.time()

    try:
        r = requests.get(
            req.url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        elapsed = round((time.time() - start) * 1000, 2)

        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"
        description = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            description = meta.get("content")

        return {
            "url": req.url,
            "status_code": r.status_code,
            "response_time_ms": elapsed,
            "title": title,
            "description": description,
            "server": r.headers.get("Server", "Unknown")
        }

    except Exception as e:
        return {
            "url": req.url,
            "error": str(e)
        }

@app.get("/")
def root():
    return {"status": "URL Viewer API running"}

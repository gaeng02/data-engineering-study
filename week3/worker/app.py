from fastapi import FastAPI, Request
from datetime import datetime
import pathlib, json

app = FastAPI()

LOG_DIR = pathlib.Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents = True, exist_ok = True)
LOG_FILE = LOG_DIR / "events.log"

def write_log (event : dict) :
    event["logged_at"] = datetime.now()
    with open(LOG_FILE, "a", encoding="utf-8") as f :
        f.write(json.dumps(event, ensure_ascii = False) + "\n")

@app.post("/login")
async def login (request : Request) :
    data = await request.json()
    write_log({"endpoint": "login", **data})
    return {"status": "ok"}

@app.post("/main")
async def main (request : Request) :
    data = await request.json()
    write_log({"endpoint": "main", **data})
    return {"status": "ok"}

@app.post("/home")
async def home (request: Request) :
    data = await request.json()
    write_log({"endpoint": "home", **data})
    return {"status": "ok"}

@app.post("/post/{post_id}")
async def post (post_id : int, request : Request) :
    data = await request.json()
    write_log({"endpoint": f"post_{post_id}", **data})
    return {"status": "ok"}

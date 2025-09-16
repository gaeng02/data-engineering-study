from fastapi import FastAPI, Request
from datetime import datetime
import pathlib, json

app = FastAPI()

LOG_DIR = pathlib.Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents = True, exist_ok = True)
LOG_FILE = LOG_DIR / "events.log"

def write_log (event : dict) :
    event["logged_at"] = datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a", encoding="utf-8") as f :
        f.write(json.dumps(event, ensure_ascii = False) + "\n")

@app.post("/login")
async def login (request : Request) :
    data = await request.json()
    
    # 수정 가능
    event = {
        "endpoint": "login",
        "ts": data.get("ts"),
        "user": data.get("user"),
        "password": data.get("password"),
        "action": data.get("action")
    }
    
    print("[WORKER] Received login:", event)
    write_log(event)
    return {"status": "ok"}

@app.post("/main")
async def main (request : Request) :
    data = await request.json()
    
    # 수정 가능
    event = {
        "endpoint": "main",
        "ts": data.get("ts"),
        "user": data.get("user"),
        "action": data.get("action")
    }
    
    print("[WORKER] Received main:", event)
    write_log(event)
    return {"status": "ok"}

@app.post("/home")
async def home (request: Request) :
    data = await request.json()
    
    # 수정 가능
    event = {
        "endpoint": "home",
        "ts": data.get("ts"),
        "user": data.get("user"),
        "action": data.get("action")
    }
    
    print("[WORKER] Received home:", event)
    write_log(event)
    return {"status": "ok"}

@app.post("/post/{post_id}")
async def post (post_id : int, request : Request) :
    data = await request.json()
    
    # 수정 가능
    event = {
        "endpoint": f"post_{post_id}",
        "ts": data.get("ts"),
        "user": data.get("user"),
        "action": data.get("action"),
        "post_id": data.get("post_id")
    }
    
    print("[WORKER] Received post:", event)
    write_log(event)
    return {"status": "ok"}

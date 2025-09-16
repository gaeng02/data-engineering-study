from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import requests, pathlib


app = FastAPI()
templates = Jinja2Templates(directory="templates")


BASE_DIR = pathlib.Path(__file__).resolve().parent
WORKERS_FILE = BASE_DIR / "config" / "workers.txt"

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents = True, exist_ok = True)
ERROR_LOG = LOG_DIR / "master_errors.log"


def _append_error (line : str) :
    with open(ERROR_LOG, "a", encoding="utf-8") as f :
        f.write(line.rstrip() + "\n")

def load_workers () -> dict[str, str] :
    workers : dict[str, str] = {}
    
    for raw in WORKERS_FILE.read_text(encoding="utf-8").splitlines() :
        line = raw.strip()
        if not line or line.startswith("#") :
            continue
        if "," not in line :
            raise ValueError(f"Invalid line (must be 'name,url'): {line}")
        name, url = [x.strip() for x in line.split(",", 1)]
        workers[name] = url.rstrip("/")
    return workers

WORKERS = load_workers()


def fanout (path : str, payload : dict, timeout_sec : float = 1.5) :
    
    for name, base in WORKERS.items() :
        url = f"{base}{path}"
        body = {**payload, "worker": name}
        try:
            resp = requests.post(url, json = body, timeout = timeout_sec)
            if (resp.status_code >= 400) :
                _append_error(f"{datetime.now()} | FAIL {name} {url} {resp.status_code} | payload={body}")
        except Exception as e :
            _append_error(f"{datetime.now()} | ERROR {name} {url} | {type(e).__name__}: {e} | payload={body}")

@app.get("/login", response_class = HTMLResponse)
def login_page (request : Request) :
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login (username : str = Form(...), password : str = Form(...)) :

    username = (username or "").strip() or "guest"
    # 실제로는 password 검증 및 저장 필요
    password = (password or "").strip() or "1234"
    
    fanout("/login", {
        "ts" : datetime.now(),
        "user": username,
        "password": password,
        "action": "login"
    })
    
    return RedirectResponse(f"/main?user={username}", status_code = 302)


@app.get("/main", response_class = HTMLResponse)
def main_page (request : Request, user : str = "guest") :
    fanout("/main", {
        "ts": datetime.now(),
        "user": user,
        "action": "view_main"
    })
    return templates.TemplateResponse("main.html", {"request": request, "user": user})


@app.get("/post/{post_id}", response_class = HTMLResponse)
def post_page (post_id : int, request : Request, user : str = "guest") :
    if post_id not in (1, 2, 3) :
        return HTMLResponse("Not Found", status_code = 404)

    fanout(f"/post/{post_id}", {
        "ts": datetime.now(),
        "user": user,
        "action": f"view_post_{post_id}",
        "post_id": post_id
    })

    return templates.TemplateResponse(
        "post.html",
        {"request": request, "user": user, "post_id": post_id, "when": datetime.now()},
    )


@app.get("/home")
def home(user : str = "guest") :
    fanout("/home", {
        "ts": datetime.now(),
        "user": user,
        "action": "click_home"
    })
    
    return RedirectResponse(f"/main?user={user}", status_code = 302)


import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .db import init_db, get_name, set_name
from datetime import datetime

app = FastAPI(title="xx FastAPI", version="1.0.0", root_path="/api")

class NamePayload(BaseModel):
    name: str

def read_container_id() -> str:
    # Try to parse from cgroup (works on many runtimes)
    try:
        with open("/proc/self/cgroup", "r") as f:
            for line in f:
                token = line.strip().split("/")[-1]
                if token and len(token) >= 12:
                    return token[-12:]
    except Exception:
        pass
    # Fallback to HOSTNAME (Pod name in k8s)
    return os.environ.get("HOSTNAME", "unknown")[:12]

@app.on_event("startup")
def startup():
    try:
        init_db()
    except Exception as e:
        # Let readiness probe handle retries
        print("DB init failed:", e)

@app.get("/healthz")
def healthz():
    return {"ok": True, "time": datetime.utcnow().isoformat() + "Z"}

@app.get("/name")
def api_get_name():
    try:
        return {"name": get_name()}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.put("/name")
def api_set_name(payload: NamePayload):
    try:
        set_name(payload.name)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/container")
def api_container():
    return {
        "container_id": read_container_id(),
        "pod_name": os.environ.get("POD_NAME", ""),
        "node_name": os.environ.get("NODE_NAME", ""),
        "time": datetime.utcnow().isoformat() + "Z"
    }

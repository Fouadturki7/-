import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from supabase import create_client, Client

app = FastAPI(title="Durr App Unified Backend")

# Database Connection Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

# Pydantic Models
class TaskCreate(BaseModel):
    user_id: str
    category_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    due_time: Optional[str] = None

class VoucherRedeem(BaseModel):
    user_id: str
    code: str

@app.get("/")
def read_root():
    return {"status": "Active", "system": "Durr Unified Backend Server"}

# --- Task Planner Endpoints ---
@app.get("/tasks/{user_id}")
def get_user_tasks(user_id: str):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection missing")
    response = supabase.table("user_tasks").select("*").eq("user_id", user_id).execute()
    return response.data

@app.post("/tasks/create")
def create_task(task: TaskCreate):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection missing")
    data = task.model_dump()
    response = supabase.table("user_tasks").insert(data).execute()
    return {"message": "Task created successfully", "data": response.data}

# --- Ads Endpoint (3-Second Banner) ---
@app.get("/ads/active")
def get_active_ads():
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection missing")
    response = supabase.table("app_advertisements").select("*").eq("is_active", True).execute()
    return response.data

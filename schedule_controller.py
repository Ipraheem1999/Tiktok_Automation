from fastapi import APIRouter, Form
import subprocess

router = APIRouter()

@router.post("/add")
def add_schedule(username: str = Form(...), video_path: str = Form(...), caption: str = Form(...), schedule_time: str = Form(...), tags: str = Form("")):
    args = [
        "python3", "tiktok_automation.py", "schedule", "add",
        username, video_path, caption, schedule_time
    ]
    if tags:
        args += ["--tags", tags]
    result = subprocess.run(args, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr}

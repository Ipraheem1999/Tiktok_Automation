from fastapi import APIRouter, Form
import subprocess

router = APIRouter()

@router.post("/add")
def add_account(username: str = Form(...), password: str = Form(...), country: str = Form(...), proxy: str = Form(None)):
    args = ["python3", "tiktok_automation.py", "account", "add", username, password, country]
    if proxy:
        args += ["--proxy", proxy]
    result = subprocess.run(args, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr}

from fastapi import APIRouter, Form
import subprocess

router = APIRouter()

@router.post("/add")
def add_proxy(country: str = Form(...), proxy: str = Form(...)):
    result = subprocess.run(
        ["python3", "tiktok_automation.py", "proxy", "add", country, proxy],
        capture_output=True,
        text=True
    )
    return {"stdout": result.stdout, "stderr": result.stderr}

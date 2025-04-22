from fastapi import APIRouter, Form
import subprocess

router = APIRouter()

@router.post("/test")
def test_engagement(username: str = Form(...), action: str = Form("random")):
    args = ["python3", "tiktok_automation.py", "engagement", "test", username, "--action", action]
    result = subprocess.run(args, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr}

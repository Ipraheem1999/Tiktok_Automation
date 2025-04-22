from fastapi import APIRouter, Form
import subprocess

router = APIRouter()

@router.post("/execute")
def execute(username: str = Form(None), random_engagement: bool = Form(False)):
    args = ["python3", "tiktok_automation.py", "run"]
    if username:
        args += ["--username", username]
    if random_engagement:
        args += ["--random-engagement"]
    args += ["--execute-posts"]
    result = subprocess.run(args, capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr}

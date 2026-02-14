import traceback
from fastapi import FastAPI
from pathlib import Path
# from api.v1.api_v1 import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.core_serial import core_serial_task

app = FastAPI()
# app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    try:
        print("Hello!")
        # core_serial_task()
    except Exception as e:
        traceback.print_exc()
        raise e
   
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")
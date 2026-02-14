import traceback
from fastapi import FastAPI, WebSocket
from pathlib import Path
import asyncio
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
        await core_serial_task()
    except Exception as e:
        traceback.print_exc()
        raise e

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        await websocket.send_text(f"Message text was: {data}")
        await asyncio.sleep(0.1)
   
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")

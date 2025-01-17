from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HealthStatus(BaseModel):
    status: str
    service: str
    
class VideoCaptureSvc:
    @app.get("/health", response_model=HealthStatus)
    async def health_check():
        return HealthStatus(status="ok", service="VideoCaptureService")
    
    def start(self):
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
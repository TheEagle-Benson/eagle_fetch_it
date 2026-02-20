from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import api, pages
from app.config import settings
import uvicorn 

app = FastAPI(
  title=settings.APP_NAME,
  description="Download videos and more from multiple platforms",
  version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.router, prefix="/api", tags=["API"])
app.include_router(pages.router, tags=["Pages"])

@app.get("/health")
def health_check():
  return {"status": "healthy"}

if __name__ == "__main__":
  uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
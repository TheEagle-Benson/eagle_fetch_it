from fastapi import APIRouter, HTTPException
from app.core.downloader import EagleFetchIt
from app.models.schemas import (
    VideoInfoRequest,
    VideoInfo,
    DownloadRequest,
    DownloadResponse
)
from app.core.validators import URLValidator

router = APIRouter()
downloader = EagleFetchIt()

@router.post("/video-info", response_model=VideoInfo)
async def get_video_info(request: VideoInfoRequest):
  url = str(request.url)

  if not URLValidator.is_valid_url(url):
    raise HTTPException(status_code=400, detail="Invalid URL")
  result = await downloader.get_video_info(url)
  if not result.success:
    raise HTTPException(status_code=400, detail=result.error)
  return result 

@router.post("/get-download-url", response_model=DownloadResponse)
async def get_download_url(request: DownloadRequest):
  url = str(request.url)
  format_id = request.format_id

  if not URLValidator.is_valid_url(url):
    raise HTTPException(status_code=400, detail="Invalid URL")
  
  result = await downloader.get_download_url(url, format_id)
  if not result['success']:
    raise HTTPException(status_code=400, detail=result['error'])
  return DownloadResponse(**result) 
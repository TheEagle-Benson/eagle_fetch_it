from pydantic import BaseModel, HttpUrl, Field

class VideoInfoRequest(BaseModel):
  url: HttpUrl = Field(..., description="URL of the video to download")

class FormatInfo(BaseModel):
  format_id: str = Field(..., description="Unique identifier for the video format")
  ext: str = Field(..., description="File extension of the video format")
  label: str = Field(..., description="Human-readable label for the video format")
  filesize: int|None = Field(None, description="Size of the video file in bytes, if available")
  resolution: str|None = Field(None, description="Resolution of the video format, if available")
  has_audio: bool = Field(..., description="Indicates if the video format includes audio")
  abr: int|None = Field(None, description="Audio bitrate in kbps, if available")

class VideoInfo(BaseModel):
    sucess: bool
    title: str|None = None
    thumbnail: str|None = None
    duration: int|None = None
    uploader: str|None = None
    platform: str|None = None
    description: str|None = None
    video_formats: list[FormatInfo] = []
    audio_formats: list[FormatInfo] = []
    error: str|None = None


class DownloadRequest(BaseModel):
    url: HttpUrl = Field(..., description="URL of the video to download")
    format_id: str = Field(..., description="Identifier of the video format to download")

class DownloadResponse(BaseModel):
    success: bool
    download_url: str|None = None
    title: str|None = None
    ext: str|None = None
    error: str|None = None
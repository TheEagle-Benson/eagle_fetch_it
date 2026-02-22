import yt_dlp
from app.models.schemas import FormatInfo, VideoInfo
from app.core.utils import format_filesize

class EagleFetchIt:
  def __init__(self):
    self.ydl_base_opts = {
      "quiet": True,
      "no_warnings": True,
      "extract_flat": False
    }

    async def get_video_info(self, url: str) -> VideoInfo:
      try:
        with yt_dlp.YoutubeDL(self.ydl_base_opts) as ydl:
          info = ydl.extract_info(url, download=False)
          formats_data = self._parse_formats(info.get("formats", []))

          return VideoInfo(
            sucess=True,
            title=info.get("title"),
            thumbnail=info.get("thumbnail"),
            duration=info.get("duration"),
            uploader=info.get("uploader") or info.get("channel"),
            platform=info.get("extractor_key"),
            description= info.get("description", "")[:200] + "..." if info.get("description") else None,
            video_formats=formats_data["video"],
            audio_formats=formats_data["audio"]
          )
      except Exception as e:
        return VideoInfo(sucess=False, error=str(e))
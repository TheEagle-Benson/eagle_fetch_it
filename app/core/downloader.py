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
            description=info.get("description", "")[:200] + "..." if info.get("description") else None,
            video_formats=formats_data["video"],
            audio_formats=formats_data["audio"]
          )
      except Exception as e:
        return VideoInfo(sucess=False, error=str(e))
      
    def _parse_formats(self, formats: list[dict]) -> dict[str, list[FormatInfo]]:
      video_formats = []
      audio_formats = []
      seen_video = set()
      seen_audio = set()

      for fmt in formats:
        ext = fmt.get("ext", "mp4")
        file_size = fmt.get("filesize")

        if fmt.get("vcodec") != "none" and fmt.get("height"):
          resolution = f"{fmt.get("height")}p"
          has_audio = fmt.get("acodec") != "none"

          key = f"{resolution}_{ext}"
          if key not in seen_video:
            seen_video.add(key)
            label = f"{resolution} {ext.upper()}"
            if file_size:
              label += f" - {format_filesize(file_size)}"
            video_formats.append(
              FormatInfo(
                format_id=fmt.get("format_id"),
                ext=ext,
                label=label,
                filesize=file_size,
                resolution=resolution,
                has_audio=has_audio
              )
            )
        elif fmt.get("acodec") != "none" and fmt.get("abr"):
          abr = fmt.get("abr", 0)
          key = f"{abr}_{ext}"
          if key not in seen_audio and abr > 0:
            seen_audio.add(key)
            label = f"{abr}kbps {ext.upper()}"
            if file_size:
              label += f" - {format_filesize(file_size)}"
            audio_formats.append(
              FormatInfo(
                format_id=fmt.get("format_id"),
                ext=ext,
                label=label,
                filesize=file_size,
                abr=int(abr)
              )
            )
      video_formats.sort(key=lambda x: int(x.resolution.replace("p", "")), reverse=True)
      audio_formats.sort(key=lambda x: x.abr or 0, reverse=True)
      return {"video": video_formats[:8], "audio": audio_formats[:4]}
    
    async def get_download_url(self, url: str, format_id: str) -> dict:
      ydl_opts = {
        **self.ydl_base_opts,
        "format": format_id
      }

      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
          info = ydl.extract_info(url, download=False)
          return {
            "success": True,
            "download_url": info["url"],
            "title": info["title"],
            "ext": info["ext"],
          }
        except Exception as e:
          return {"success": False, "error": str(e)}


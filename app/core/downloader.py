import yt_dlp
from app.models.schemas import FormatInfoAudio, FormatInfoVideo,  VideoInfo
from app.core.utils import format_filesize,format_duration

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
            success=True,
            title=info.get("title"),
            thumbnail=info.get("thumbnail"),
            duration=format_duration(info.get("duration")),
            uploader=info.get("uploader") or info.get("channel"),
            platform=info.get("extractor_key"),
            description=info.get("description"),
            video_formats=formats_data["video"],
            audio_formats=formats_data["audio"]
          )
      except Exception as e: 
        return VideoInfo(success=False, error=str(e))
      
  def _parse_formats(self, formats: list[dict]) -> dict[str, list[FormatInfoAudio|FormatInfoVideo]]:
      video_formats = []
      audio_formats = []

      for fmt in formats:
        ext = fmt.get("ext", "mp4")
        file_size = fmt.get("filesize")

        if fmt.get("vcodec") != "none" and fmt.get("height"):
          resolution = f"{fmt.get('height')}p"
          has_audio = fmt.get("acodec") != "none"
          print(fmt.get("acodec"))
          print(f"Processing video format: {resolution}, audio: {has_audio}, ext: {ext}, filesize: {file_size}")

          label = f"{resolution} {ext.upper()}"
          if file_size:
            label += f" - {format_filesize(file_size)}"
          video_formats.append(
            FormatInfoVideo(
              format_id=fmt.get("format_id"),
              ext=ext,
              label=label,
              filesize=format_filesize(file_size) if file_size else None,
              resolution=resolution,
              has_audio=has_audio
              )
            )
        elif fmt.get("acodec") != "none" and fmt.get("abr"):
          abr = fmt.get("abr", 0)
          label = f"{abr}kbps {ext.upper()}"
          if file_size:
            label += f" - {format_filesize(file_size)}"
          audio_formats.append(
            FormatInfoAudio(
              format_id=fmt.get("format_id"),
              ext=ext,
              label=label,
              filesize=format_filesize(file_size) if file_size else None,
              abr=int(abr)
              )
            )
      video_formats.sort(key=lambda x: (int(x.resolution.replace("p", "")), x.has_audio), reverse=True)
      audio_formats.sort(key=lambda x: x.abr or 0, reverse=True)
      return {"video": video_formats, "audio": audio_formats}
    
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
import yt_dlp
from app.models.schemas import FormatInfoAudio, FormatInfoVideo,  VideoInfo
from app.core.utils import format_filesize,format_duration, decode_base64, wrap_error_response

import logging

logger = logging.getLogger(__name__)

class EagleFetchIt: 
  def __init__(self):
    self.ydl_base_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'nocheckcertificate': True,
            
            
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; en_US)',
                'Accept-Language': 'en-US,en;q=0.9',
            },
            
            # ✅ Add age gate bypass
            'age_limit': None,
        }

  async def get_video_info(self, url: str) -> VideoInfo:
      cookies_path = decode_base64()
      if cookies_path:
        self.ydl_base_opts['cookiefile'] = cookies_path
        print(f"Using cookies from: {cookies_path}")
        logger.info(f"Using cookies from: {cookies_path}")
      else:
        print("No cookies found, proceeding without them.")
        logger.warning("No cookies found, proceeding without them.")
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
      except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        logger.error(f"DownloadError: {error_msg}")
        # user_friendly_msg = get_user_friendly_error(error_msg)
        # return VideoInfo(success=False, error={
        #   "error_": user_friendly_msg,
        #   "raw_error": error_msg
        # })
        error = wrap_error_response(error_msg)
        return VideoInfo(**error)
      except yt_dlp.utils.ExtractorError as e:
        error_msg = str(e)
        logger.error(f"ExtractorError: {error_msg}")
        # user_friendly_msg = get_user_friendly_error(error_msg)
        # return VideoInfo(success=False, error={
        #   "error_": user_friendly_msg,
        #   "raw_error": error_msg
        # })
        error = wrap_error_response(error_msg)
        return VideoInfo(**error)
      except Exception as e:
        print(f"Unexpected error: {str(e)}")
        error_msg = str(e)
        logger.error(f"DownloadError: {error_msg}")
        # user_friendly_msg = get_user_friendly_error(error_msg)
        # return VideoInfo(success=False, error={
        #   "error_": user_friendly_msg,
        #   "raw_error": error_msg
        # })
        error = wrap_error_response(error_msg)
        return VideoInfo(**error)
      
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
        except yt_dlp.utils.DownloadError as e:
          error_msg = str(e)
          logger.error(f"Download URL Error: {error_msg}")
          # user_friendly_msg = get_user_friendly_error(error_msg)
          error = wrap_error_response(error_msg)
          return VideoInfo(**error)
        except Exception as e:
          error_msg = str(e)
        logger.error(f"DownloadError: {error_msg}")
        # user_friendly_msg = get_user_friendly_error(error_msg)
        # return VideoInfo(success=False, error={
        #   "error_": user_friendly_msg,
        #   "raw_error": error_msg
        # })
        error = wrap_error_response(error_msg)
        return VideoInfo(**error)
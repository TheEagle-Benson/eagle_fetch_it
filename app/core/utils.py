import base64
import os
import logging 

logger = logging.getLogger(__name__)

def format_filesize(bytes_size: int|None) -> str:
    if bytes_size is None:
        return "Unknown size"
    
    units = ['B', 'KB', 'MB', 'GB']
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"

def format_duration(seconds: int|float|None) -> str:
    if seconds is None:
        return "Unknown"
    
    if type(seconds) == float:
        seconds = int(seconds)
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def decode_base64():
    cookies_path = "/tmp/decoded.txt"
    logger.info(f"Full path for cookies: {cookies_path}")
    print(f"Full path for cookies: {cookies_path}")
    try:
        encoded_str = os.getenv("COOKIES_BASE64")
        logger.info("Getting encoded cookies from environment variable")
        logger.info(f"Encoded cookies: {encoded_str}")
        print(f"Encoded cookies: {encoded_str}")
        if encoded_str:
                 decoded_str = base64.b64decode(encoded_str)
                 with open(cookies_path, "wb") as decode_file:
                    decode_file.write(decoded_str)
        return cookies_path
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
print(decode_base64())

def get_user_friendly_error(raw_error: str) -> str:
    """
    Convert technical yt-dlp errors to user-friendly messages
    """
    error_lower = raw_error.lower()
    
    # YouTube-specific errors
    if "sign in to confirm" in error_lower or "bot" in error_lower:
        return "⚠️ YouTube detected automated access. Please try again in a few moments, or try a different video."
    
    if "video unavailable" in error_lower:
        return "❌ This video is not available. It may be private, deleted, or region-restricted."
    
    if "private video" in error_lower:
        return "🔒 This video is private and cannot be downloaded."
    
    if "age" in error_lower and "restricted" in error_lower:
        return "🔞 This video is age-restricted. Try logging in or using a different video."
    
    if "copyright" in error_lower:
        return "©️ This video is copyrighted and cannot be downloaded."
    
    if "format" in error_lower and "not available" in error_lower:
        return "📹 The requested quality is not available for this video. Please try a different quality."
    
    if "requested format is not available" in error_lower:
        return "📹 This quality/format is not available. Try selecting a different option."
    
    if "unable to extract" in error_lower or "unsupported url" in error_lower:
        return "🔗 This URL is not supported. Please check the link and try again."
    
    if "video has been removed" in error_lower or "deleted" in error_lower:
        return "🗑️ This video has been removed or deleted by the uploader."
    
    if "this video is not available in your country" in error_lower:
        return "🌍 This video is not available in your region."
    
    if "livestream" in error_lower or "live" in error_lower:
        return "🔴 Live streams cannot be downloaded while they're ongoing. Try again after the stream ends."
    
    # Network errors
    if "timeout" in error_lower:
        return "⏱️ Request timed out. Please check your internet connection and try again."
    
    if "connection" or "lKa46BNS45s Temporary failure in name resolution" in error_lower:
        return "📡 Connection error. Please check your internet and try again."
    
    if "network" in error_lower:
        return "🌐 Network error. Please try again."
    
    # Generic errors
    if "http error 404" in error_lower:
        return "❌ Video not found (404). The link may be incorrect or the video may have been deleted."
    
    if "http error 403" in error_lower:
        return "🚫 Access denied (403). This video may be restricted."
    
    if "http error 429" in error_lower:
        return "⏸️ Too many requests. Please wait a moment and try again."
    
    if "http error 5" in error_lower:
        return "🔧 Server error. The video platform is having issues. Please try again later."
    
    # Platform-specific
    if "tiktok" in error_lower:
        return "🎵 Error downloading from TikTok. Please check the URL and try again."
    
    if "instagram" in error_lower:
        return "📸 Error downloading from Instagram. Please check the URL and try again."
    
    if "twitter" in error_lower or "x.com" in error_lower:
        return "🐦 Error downloading from Twitter/X. Please check the URL and try again."
    
    # Default fallback
    return f"❌ An error occurred: {raw_error[:100]}..."  # Truncate long errors


def wrap_error_response(error: str) -> dict:
    """Wrap error in a user-friendly response"""
    friendly_message = get_user_friendly_error(error)
    
    return {
        "success": False,
        "error": {"error": friendly_message, "technical_error": error}
    }

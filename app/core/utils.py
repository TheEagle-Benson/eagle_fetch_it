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

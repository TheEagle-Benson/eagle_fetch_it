import re

class URLValidator:
    PLATFORM_PATTERNS = {
        'youtube': [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)',
            r'youtube\.com\/shorts\/([a-zA-Z0-9_-]+)',
        ],
        'tiktok': [
            r'tiktok\.com\/@[\w.-]+\/video\/(\d+)',
            r'vm\.tiktok\.com\/([a-zA-Z0-9]+)',
        ],
        'instagram': [
            r'instagram\.com\/(?:p|reel)\/([a-zA-Z0-9_-]+)',
        ],
        'twitter': [
            r'(?:twitter|x)\.com\/\w+\/status\/(\d+)',
        ],
        'facebook': [
            r'facebook\.com\/.*\/videos\/(\d+)',
            r'fb\.watch\/([a-zA-Z0-9_-]+)',
        ],
    }
    
    @classmethod
    def detect_platform(cls, url: str) -> str|None:
        for platform, patterns in cls.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return platform
        return None
    
    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        return cls.detect_platform(url) is not None

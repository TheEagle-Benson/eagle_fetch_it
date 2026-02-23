from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
template = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return template.TemplateResponse(request=request, name="index.html", context={})

@router.get("/youtube", response_class=HTMLResponse)
async def youtube_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="youtube.html",
        context={
            "platform": "youtube",
            "platform_name": "Youtube",
            "description": "Download videos and audio from Youtube",
            "platform_logo_url": "/static/images/platform_logos/youtube.png"
        }
    )

@router.get("/facebook", response_class=HTMLResponse)
async def facebook_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="facebbok.html",
        context={
            "platform": "facebook",
            "platform_name": "Facebook",
            "description": "Download videos and reels from Facebook",
            "platform_logo_url": "/static/images/platform_logos/facebook.png"
        }
    )

@router.get("/instagram", response_class=HTMLResponse)
async def instagram_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="instagram.html",
        context={
            "platform": "instagram",
            "platform_name": "Instagram",
            "description": "Download videos and reels from Instagram",
            "platform_logo_url": "/static/images/platform_logos/instagram.png"
        }
    )

@router.get("/twitter_x", response_class=HTMLResponse)
async def twitter_x_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="x.html",
        context={
            "platform": "x",
            "platform_name": "X",
            "description": "Download videos from X",
            "platform_logo_url": "/static/images/platform_logos/x.png"
        }
    )

@router.get("/tiktok", response_class=HTMLResponse)
async def tiktok_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="tiktok.html",
        context={
            "platform": "tiktok",
            "platform_name": "TikTok",
            "description": "Download videos and audio from TikTok",
            "platform_logo_url": "/static/images/platform_logos/tiktok.png"
        }
    )
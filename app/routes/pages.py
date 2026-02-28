from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
template = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return template.TemplateResponse(request=request, name="pages/index.html")

@router.get("/youtube", response_class=HTMLResponse)
async def youtube_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/youtube.html",
        context={
            "platform": "youtube",
            "platform_name": "YouTube",
            "platform_icon": "/static/images/platform_logos/youtube.png",
            "description": "Download YouTube videos"
        }
    )

@router.get("/facebook", response_class=HTMLResponse)
async def facebook_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/facebook.html",
        context={
            "platform": "facebook",
            "platform_name": "Facebook",
            "platform_icon": "/static/images/platform_logos/facebook.png",
            "description": "Download Facebook videos"
        }
        )

@router.get("/instagram", response_class=HTMLResponse)
async def instagram_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/instagram.html",
        context={
            "platform": "instagram",
            "platform_name": "Instagram",
            "platform_icon": "/static/images/platform_logos/instagram.png",
            "description": "Download Instagram videos"
        }
    )

@router.get("/twitter_x", response_class=HTMLResponse)
async def twitter_x_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/twitter_x.html",
        context={
            "platform": "twitter_x",
            "platform_name": "X",
            "platform_icon": "/static/images/platform_logos/x.png",
            "description": "Download videos from tweets"
        }
    )

@router.get("/tiktok", response_class=HTMLResponse)
async def tiktok_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/tiktok.html",
        context={
            "platform": "tiktok",
            "platform_name": "TikTok",
            "platform_icon": "/static/images/platform_logos/tiktok.png",
            "description": "Download TikTok videos"
        }
    )
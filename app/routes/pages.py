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
        name="pages/youtube.html"
    )

@router.get("/facebook", response_class=HTMLResponse)
async def facebook_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/facebook.html"
        )

@router.get("/instagram", response_class=HTMLResponse)
async def instagram_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/instagram.html"
    )

@router.get("/twitter_x", response_class=HTMLResponse)
async def twitter_x_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/twitter_x.html"
    )

@router.get("/tiktok", response_class=HTMLResponse)
async def tiktok_page(request: Request):
    return template.TemplateResponse(
        request=request,
        name="pages/tiktok.html"
    )
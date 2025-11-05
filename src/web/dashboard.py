"""
Web管理面板
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.web.templates import get_dashboard_html

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """管理面板主页"""
    return get_dashboard_html()

from fastapi import APIRouter, HTTPException
import io
import base64
from PIL import Image
from typing import List, Dict, Any
from app.schemas.screeninfo import ScreenInfoOut
from app.schemas.enums import ContextMode
from app.schemas.rect import RectRequest
import screeninfo
import pyautogui


router = APIRouter(prefix='/desktop', tags=['Desktop'])


@router.get("/screens", response_model=List[ScreenInfoOut], operation_id="get_screen_info")
async def get_screen_info() -> List[ScreenInfoOut]:
    """Get information about all connected screens/monitors.

    Returns detailed information about each connected display including position,
    resolution, and physical dimensions. This information is essential for
    determining screenshot coordinates and understanding multi-monitor layouts.

    Returns:
        List of screen objects, each containing:
        - x, y: Screen position in virtual desktop coordinates
        - width, height: Screen resolution in pixels
        - name: Display name/identifier
        - is_primary: Boolean indicating if this is the primary display
        - width_mm, height_mm: Physical dimensions in millimeters

    Example:
        For 3 horizontally aligned 1920x1080 screens:
        - Screen 1: x=0, y=0, width=1920, height=1080
        - Screen 2: x=1920, y=0, width=1920, height=1080
        - Screen 3: x=3840, y=0, width=1920, height=1080
    """

    screens = [ScreenInfoOut(**x.__dict__) for x in screeninfo.get_monitors()]

    return screens


@router.post("/screenshot", response_model=Dict[str, Any], operation_id="desktop_take_screenshot")
async def desktop_take_screenshot(rect: RectRequest, context_mode: str = "minimal") -> Dict[str, Any]:
    """Take a screenshot of a specific region across all connected screens.

    Captures a rectangular region from the virtual desktop spanning all monitors.
    Use get_screen_info() first to determine proper coordinates for targeting
    specific screens or regions. Images are automatically compressed to optimize
    for AI processing while maintaining visual clarity.

    Args:
        rect: Rectangle coordinates defining the capture area
            - x, y: Top-left corner of the region in virtual desktop coordinates
            - width, height: Dimensions of the capture region in pixels
        context_mode: Image quality/size mode (default: "minimal")
            - "minimal": 600px max, 30% quality - for basic UI detection
            - "normal": 800px max, 50% quality - for detailed UI inspection
            - "detailed": 1200px max, 70% quality - for pixel-perfect UI analysis

    Returns:
        Dictionary containing base64-encoded WEBP image data optimized for AI analysis.

    Usage Examples:
        - Single screen (1920x1080): x=0, y=0, width=1920, height=1080
        - Second screen (horizontally aligned): x=1920, y=0, width=1920, height=1080
        - Custom region: x=500, y=300, width=800, height=600

    Note:
        Coordinates are based on the virtual desktop layout returned by get_screen_info().
        For multi-monitor setups, screens may be arranged horizontally, vertically, 
        or in custom configurations affecting the coordinate system.
        Use this at minimal settings unless absolutely necessary to avoid filling the chat context.

    Raises:
        HTTPException: If screenshot capture fails or coordinates are invalid.
    """

    settings = ContextMode[context_mode.upper()].value

    try:
        region = (rect.x, rect.y, rect.width, rect.height)
        screenshot = pyautogui.screenshot(allScreens=True, region=region)

        width, height = screenshot.size
        max_dim = settings["max_dim"]

        if width > max_dim or height > max_dim:
            ratio = min(max_dim / width, max_dim / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            screenshot = screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        screenshot.save(buffer, format="WEBP", quality=settings["quality"], optimize=True, method=6)
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "context": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/webp",
                        "data": img_base64
                    }
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Screenshot capture failed: {str(e)}")
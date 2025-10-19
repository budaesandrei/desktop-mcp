# 🖥️ Desktop MCP

A Model Context Protocol (MCP) server for desktop operations, providing AI assistants with the ability to capture and analyze screen content across multi-monitor setups.

## Features

- 📸 **Multi-Monitor Screenshot Support**: Capture screenshots from any region across all connected displays
- 🖥️ **Screen Information**: Get detailed information about all connected monitors (resolution, position, dimensions)
- 🎨 **Smart Image Optimization**: Automatic compression and resizing for AI context efficiency
- 🔄 **Dual Mode Operation**: Run as an MCP server or as a standalone web API
- ⚡ **FastAPI Powered**: Built on modern, fast, and well-documented FastAPI framework

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/desktop-mcp.git
cd desktop-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### MCP Mode (Default)

Run as an MCP server for use with AI assistants like Claude Desktop:

```bash
python -m app.main
```

### Web Mode

Run as a standalone web API with interactive documentation:

```bash
python -m app.main --web
```

This will:
- Start the server at `http://localhost:8000`
- Automatically open the interactive API docs in your browser
- Enable live reload for development

## Configuration

### Adding to Claude Desktop

Add this configuration to your Claude Desktop MCP settings file (typically at `~/.cursor/mcp.json` or `%APPDATA%/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "Desktop MCP": {
      "command": "python",
      "args": ["-m", "app.main"],
      "cwd": "/path/to/desktop-mcp"
    }
  }
}
```

## API Reference

### Endpoints

#### `GET /desktop/screens`

Get information about all connected monitors.

**Response:**
```json
[
  {
    "x": 0,
    "y": 0,
    "width": 1920,
    "height": 1080,
    "name": "\\\\.\\DISPLAY1",
    "is_primary": true,
    "width_mm": 527,
    "height_mm": 296
  }
]
```

#### `POST /desktop/screenshot`

Capture a screenshot of a specific region.

**Parameters:**
- `x` (int): X coordinate of top-left corner
- `y` (int): Y coordinate of top-left corner
- `width` (int): Width of capture region
- `height` (int): Height of capture region
- `context_mode` (string, optional): Image quality mode
  - `minimal` (default): 600px max, 30% quality - for basic UI detection
  - `normal`: 800px max, 50% quality - for detailed UI inspection
  - `detailed`: 1200px max, 70% quality - for pixel-perfect UI analysis

**Request Body:**
```json
{
  "x": 0,
  "y": 0,
  "width": 1920,
  "height": 1080
}
```

**Response:**
```json
{
  "context": [
    {
      "type": "image",
      "source": {
        "type": "base64",
        "media_type": "image/webp",
        "data": "UklGRi..."
      }
    }
  ]
}
```

## Usage Examples

### Example 1: Capture Primary Monitor

```python
import requests

# Get screen info
screens = requests.get("http://localhost:8000/desktop/screens").json()
primary = next(s for s in screens if s["is_primary"])

# Capture primary screen
screenshot = requests.post(
    "http://localhost:8000/desktop/screenshot",
    params={"context_mode": "normal"},
    json={
        "x": primary["x"],
        "y": primary["y"],
        "width": primary["width"],
        "height": primary["height"]
    }
).json()
```

### Example 2: Capture Specific Region

```python
# Capture a 800x600 region starting at position (100, 100)
screenshot = requests.post(
    "http://localhost:8000/desktop/screenshot",
    params={"context_mode": "minimal"},
    json={
        "x": 100,
        "y": 100,
        "width": 800,
        "height": 600
    }
).json()
```

### Example 3: Multi-Monitor Setup

```python
# For a 3-monitor horizontal setup (each 1920x1080):
# Left monitor: x=0, y=0
# Center monitor: x=1920, y=0
# Right monitor: x=3840, y=0

# Capture right monitor
screenshot = requests.post(
    "http://localhost:8000/desktop/screenshot",
    params={"context_mode": "detailed"},
    json={
        "x": 3840,
        "y": 0,
        "width": 1920,
        "height": 1080
    }
).json()
```

## Use Cases with AI Assistants

When integrated with AI assistants like Claude:

- **Visual Debugging**: "Can you see what error message is on my screen?"
- **UI/UX Analysis**: "What do you think of this design layout?"
- **Tutorial Assistance**: "I'm stuck on this step, can you see what I'm doing wrong?"
- **Code Review**: "Can you review the code visible on my screen?"
- **Accessibility Testing**: "Is this UI accessible and well-organized?"

## Development

### Project Structure

```
desktop-mcp/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── desktop.py       # Desktop API routes
│   └── schemas/
│       ├── __init__.py
│       ├── enums.py         # Context mode enums
│       ├── rect.py          # Rectangle schema
│       └── screeninfo.py    # Screen info schema
├── requirements.txt
└── README.md
```

### Running Tests

```bash
# Run the server in web mode for testing
python -m app.main --web

# Visit http://localhost:8000/docs to test endpoints
```

## Requirements

- `fastapi` - Modern web framework
- `fastmcp` - MCP protocol implementation
- `uvicorn` - ASGI server
- `screeninfo` - Monitor information retrieval
- `pyautogui` - Screenshot capture
- `pillow` - Image processing
- `pydantic` - Data validation

## Security Considerations

⚠️ **Important**: This tool provides direct access to screen content. When deploying:

- Only expose to trusted networks
- Consider authentication mechanisms for production use
- Be mindful of sensitive information in screenshots
- Use appropriate context modes to minimize data transfer

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Troubleshooting

### Screenshot Capture Fails

- **Linux**: Ensure you have the required X11 libraries installed
- **macOS**: Grant screen recording permissions in System Preferences
- **Windows**: Run with appropriate privileges if capturing protected content

### Multi-Monitor Issues

- Use `GET /desktop/screens` first to verify monitor coordinates
- Remember that coordinates are based on virtual desktop layout
- Monitors may be arranged horizontally, vertically, or in custom configurations

### Performance Optimization

- Use `minimal` context mode for frequent captures
- Capture only the necessary region instead of full screens
- Consider caching screen information instead of querying repeatedly

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for enhancing AI assistant capabilities
